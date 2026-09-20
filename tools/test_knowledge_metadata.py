import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from knowledge_metadata import corpus_digest, faq_manifest


class MetadataTests(unittest.TestCase):
    def test_generation_uses_relative_paths_and_exact_file_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            public = Path(temp)
            (public / 'ä.html').write_bytes(b'one')
            (public / 'a.html').write_bytes(b'two')
            rows = b''.join(name.encode() + b'\0' + hashlib.sha256(body).hexdigest().encode() + b'\n'
                            for name, body in [('a.html', b'two'), ('ä.html', b'one')])
            self.assertEqual(corpus_digest(public), hashlib.sha256(rows).hexdigest())
            (public / 'a.html').unlink()
            self.assertNotEqual(corpus_digest(public), hashlib.sha256(rows).hexdigest())

    def test_faq_requires_review_hash_and_literal_question(self):
        with tempfile.TemporaryDirectory() as temp:
            public = Path(temp)
            content = b'<main><section id="help"><h2>Wie geht <code>!rank</code>?</h2><p>Antwort.</p></section></main>'
            (public / 'help.html').write_bytes(content)
            audit = {'path': 'public/help.html', 'verified_at': '2026-09-20',
                     'code': [{'repository': 'bot'}], 'claims': [{'verdict': 'verified'}],
                     'content_sha256': hashlib.sha256(content).hexdigest(), 'gaps': []}
            result = faq_manifest(public, [audit], policy_revision='revision')
            self.assertEqual(result['entries'][0]['question'], 'Wie geht !rank?')
            self.assertEqual(result['entries'][0]['section_id'], 'help')
            audit['gaps'] = ['Ungeprüfte Aussage']
            self.assertEqual(faq_manifest(public, [audit], policy_revision='revision')['entries'], [])
            audit['gaps'] = []
            (public / 'help.html').write_bytes(content + b'Changed')
            self.assertEqual(faq_manifest(public, [audit], policy_revision='revision')['entries'], [])
            (public / 'help.html').unlink()
            self.assertEqual(faq_manifest(public, [audit], policy_revision='revision')['entries'], [])

    def test_symlink_corpus_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            public = Path(temp)
            (public / 'real.html').write_text('Text')
            (public / 'alias.html').symlink_to(public / 'real.html')
            with self.assertRaises(ValueError):
                corpus_digest(public)

    def test_explicit_standard_answer_requires_complete_source_and_scope(self):
        with tempfile.TemporaryDirectory() as temp:
            public = Path(temp)
            content = ('<main><section id="start"><h2>Chat öffnen</h2>'
                       '<p>Nutze <code>/faq</code>.</p><p>Nur auf dem Server.</p>'
                       '</section></main>').encode()
            (public / 'help.html').write_bytes(content)
            standard = {'section_id': 'start', 'question': 'Wie öffne ich einen Fragechat?',
                        'answer': 'Nutze /faq.\n\nNur auf dem Server.',
                        'scope': 'Nur Einstieg; nicht bei Fehlern.'}
            audit = {'path': 'public/help.html', 'verified_at': '2026-09-20',
                     'code': [{'repository': 'bot'}], 'claims': [{'verdict': 'verified'}],
                     'content_sha256': hashlib.sha256(content).hexdigest(), 'gaps': [],
                     'standard_answers': [standard]}
            manifest = faq_manifest(public, [audit], policy_revision='revision')
            entry = manifest['entries'][0]
            self.assertEqual(entry['id'], 'faq:help.html#start')
            self.assertEqual(entry['standard_answer'], standard['answer'])
            self.assertEqual(entry['standard_answer_scope'], standard['scope'])
            for key, invalid in [('answer', 'Nutze /faq.'), ('scope', ''),
                                 ('section_id', 'missing'), ('question', 'Keine Frage')]:
                with self.subTest(key=key):
                    previous = standard[key]
                    standard[key] = invalid
                    with self.assertRaises(ValueError):
                        faq_manifest(public, [audit], policy_revision='revision')
                    standard[key] = previous
            audit['standard_answers'].append(dict(standard))
            with self.assertRaises(ValueError):
                faq_manifest(public, [audit], policy_revision='revision')
            audit['standard_answers'].pop()
            audit['gaps'] = ['Codepfad geändert']
            self.assertEqual(faq_manifest(public, [audit], policy_revision='revision')['entries'], [])
            audit['gaps'] = []
            (public / 'help.html').write_bytes(content + b'changed')
            self.assertEqual(faq_manifest(public, [audit], policy_revision='revision')['entries'], [])

    def test_checked_in_standard_answers_match_complete_audited_sources(self):
        root = Path(__file__).resolve().parent.parent
        policy = json.loads((root / 'public-sources.json').read_text())
        audits = [audit for file in policy['audit_files']
                  for audit in json.loads((root / file).read_text())['documents']]
        selected = [standard for audit in audits for standard in audit.get('standard_answers', [])]
        manifest = faq_manifest(root / 'public', audits, policy_revision='test')
        exported = [entry for entry in manifest['entries'] if 'standard_answer' in entry]
        self.assertGreater(len(selected), 0)
        self.assertEqual(len(selected), len(exported))
        for entry in exported:
            self.assertLessEqual(len(entry['standard_answer'].encode('utf-16-le')) // 2, 1600)


if __name__ == '__main__':
    unittest.main()
