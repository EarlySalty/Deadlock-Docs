import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from public_code_metadata import public_code_manifest


class PublicCodeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.public = Path(self.temp.name)
        self.content = b'<main><section id="faq"><h2>FAQ</h2><p>Nutze /faq.</p></section></main>'
        (self.public / 'help.html').write_bytes(self.content)
        self.excerpt = ('"name": "faq", "description": "Öffentliche Hilfe", '
                        '"type": 1, "dm_permission": false,')
        self.blob = ('fn register() { ' + self.excerpt + ' }\n').encode()
        self.revision = 'a' * 40
        self.path = 'rust/crates/dl-community/src/faq.rs'
        self.audit = {'path': 'public/help.html', 'verified_at': '2026-09-20',
                      'code': [{'repository': 'discord', 'revision': self.revision, 'paths': [self.path]}],
                      'claims': [{'verdict': 'verified'}], 'gaps': [],
                      'content_sha256': hashlib.sha256(self.content).hexdigest()}
        self.entry = {'id': 'P1', 'title': 'Öffentliche FAQ-Hilfe', 'public_help_path': 'help.html',
                      'public_help_section': 'faq', 'source_path': self.path, 'symbol': 'register:faq',
                      'blob_sha256': hashlib.sha256(self.blob).hexdigest(), 'excerpt': self.excerpt,
                      'explanation': 'Nutze /faq auf dem Server.', 'review_status': 'verified'}
        self.policy = {'schema_version': 1, 'repository': 'discord', 'release_commit': self.revision,
                       'entries': [self.entry]}
        self.read = Mock(return_value=self.blob)

    def export(self, **overrides):
        args = {'policy_revision': 'b' * 40, 'policy': self.policy,
                'revisions': {'discord': self.revision}, 'read_blob': self.read}
        args.update(overrides)
        return public_code_manifest(self.public, [self.audit], **args)

    def test_only_exact_reviewed_release_source_is_exported(self):
        result = self.export()
        self.assertEqual(len(result['entries']), 1)
        self.assertEqual(result['entries'][0]['public_help_sha256'], hashlib.sha256(self.content).hexdigest())
        self.read.assert_called_once_with('discord', self.revision, self.path)

    def test_changed_release_never_reads_history(self):
        self.assertEqual(self.export(revisions={'discord': 'c' * 40})['entries'], [])
        self.read.assert_not_called()

    def test_unreviewed_and_withdrawn_sources_do_not_read_code(self):
        for status in ['pending', 'withdrawn', None]:
            self.entry['review_status'] = status
            self.assertEqual(self.export()['entries'], [])
        self.entry['review_status'] = 'verified'
        self.audit['gaps'] = ['Codepfad geändert']
        self.assertEqual(self.export()['entries'], [])
        self.audit['gaps'] = []
        (self.public / 'help.html').write_bytes(self.content + b'changed')
        self.assertEqual(self.export()['entries'], [])
        self.read.assert_not_called()

    def test_arbitrary_private_paths_and_policy_versions_are_rejected(self):
        for source in ['.env', '/etc/passwd', '../faq.rs', 'rust/secrets.rs']:
            self.entry['source_path'] = source
            with self.assertRaises(ValueError):
                self.export()
        self.entry['source_path'] = self.path
        for version in [0, 2, None]:
            self.policy['schema_version'] = version
            with self.assertRaises(ValueError):
                self.export()
        self.read.assert_not_called()

    def test_changed_blob_or_invented_excerpt_is_not_exported(self):
        self.read.return_value = self.blob + b'changed'
        self.assertEqual(self.export()['entries'], [])
        self.read.return_value = self.blob
        self.entry['excerpt'] = 'Nicht im Quellcode'
        self.assertEqual(self.export()['entries'], [])
        self.entry['excerpt'] = 'fn register()'
        self.assertEqual(self.export()['entries'], [])

    def test_unbound_section_and_code_path_are_not_exported(self):
        self.entry['public_help_section'] = 'missing'
        self.assertEqual(self.export()['entries'], [])
        self.entry['public_help_section'] = 'faq'
        self.audit['code'][0]['paths'] = []
        self.assertEqual(self.export()['entries'], [])
        self.read.assert_not_called()

    def test_duplicates_and_oversized_entries_are_rejected(self):
        self.policy['entries'].append(copy.deepcopy(self.entry))
        with self.assertRaises(ValueError):
            self.export()
        self.policy['entries'].pop()
        self.entry['explanation'] = '🦆' * 1000
        with self.assertRaises(ValueError):
            self.export()


if __name__ == '__main__':
    unittest.main()
