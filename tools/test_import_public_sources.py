import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

from import_public_sources import import_sources


PAGE = '''<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>Öffentliche Hilfe</title><meta name="tags" content="hilfe">
<meta name="stand" content="2026-09-20"><meta name="quelle" content="Nutzerhilfe">
</head><body><main><h1>Öffentliche Hilfe</h1><section id="hilfe"><h2>Wie geht das?</h2>
<p>Öffne die Hilfe im Dashboard.</p></section></main></body></html>'''


class ImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.git('init', '-q')
        self.raw = '---\naudience: public\n---\n# Hilfe\n\nÖffne das Dashboard.\n'
        (self.repo / 'help.md').write_text(self.raw)
        (self.repo / 'code.rs').write_text('fn main() {}')
        self.commit()
        self.revision = self.git('rev-parse', 'HEAD').strip()
        self.source = {'id': 'test', 'label': 'Nutzerhilfe', 'path': str(self.repo), 'ref': 'HEAD',
                       'public': [{'glob': 'help.md', 'target': 'help.html', 'use_curated': True,
                                   'require_audience': True, 'evidence': 'Ausdrückliche öffentliche Nutzerhilfe'}],
                       'reviews': {'help.md': {'source_sha256': hashlib.sha256(self.raw.encode()).hexdigest(),
                                               'content_sha256': hashlib.sha256(PAGE.encode()).hexdigest(),
                                               'verified_at': '2026-09-20', 'code': [
                                                   {'repository': 'test', 'revision': self.revision, 'paths': ['code.rs']} ]}}}
        self.config = {'managed_targets': ['help.html'], 'repositories': [self.source]}

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], stderr=subprocess.DEVNULL).decode()

    def commit(self):
        self.git('add', '.')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'Fixture')

    def run_import(self, page=PAGE):
        target = self.root / 'export' / 'public' / 'help.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page)
        report = import_sources(self.config, target.parent.parent)
        return report, target.read_text() if target.exists() else ''

    def test_curated_markup_is_preserved_exactly(self):
        report, output = self.run_import()
        self.assertEqual(report['imported'], 1)
        self.assertEqual(output, PAGE)

    def test_relative_help_link_does_not_require_importing_its_target(self):
        page = PAGE.replace('Öffne die Hilfe im Dashboard.',
                            '<a href="other.html">Weitere Hilfe</a>')
        self.source['reviews']['help.md']['content_sha256'] = hashlib.sha256(page.encode()).hexdigest()
        report, output = self.run_import(page)
        self.assertEqual(report['imported'], 1)
        self.assertEqual(output, page)

    def test_isolated_validation_still_rejects_path_escape(self):
        page = PAGE.replace('Öffne die Hilfe im Dashboard.',
                            '<a href="../outside.html">Weitere Hilfe</a>')
        self.source['reviews']['help.md']['content_sha256'] = hashlib.sha256(page.encode()).hexdigest()
        report, output = self.run_import(page)
        self.assertEqual(report['imported'], 0)
        self.assertEqual(output, '')

    def test_audience_withdrawal_removes_old_public_content(self):
        (self.repo / 'help.md').write_text(self.raw.replace('audience: public', 'audience: public\nvisibility: private'))
        self.commit()
        report, output = self.run_import()
        self.assertEqual(report['imported'], 0)
        self.assertNotIn('Öffne die Hilfe', output)

    def test_deletion_removes_old_public_content_even_when_corpus_becomes_empty(self):
        (self.repo / 'help.md').unlink()
        self.commit()
        report, output = self.run_import()
        self.assertEqual(report['imported'], 0)
        self.assertNotIn('Öffne die Hilfe', output)

    def test_unreviewed_editorial_change_and_code_change_are_not_imported(self):
        report, output = self.run_import(PAGE.replace('Öffne die Hilfe', 'Automatisch alles erledigt'))
        self.assertEqual(report['imported'], 0)
        self.assertNotIn('Automatisch alles', output)
        (self.repo / 'code.rs').write_text('fn main() { changed(); }')
        self.commit()
        report, output = self.run_import()
        self.assertEqual(report['imported'], 0)
        self.assertEqual(report['repositories'][0]['pending_review'], 1)


if __name__ == '__main__':
    unittest.main()
