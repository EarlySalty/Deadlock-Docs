import hashlib
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


if __name__ == '__main__':
    unittest.main()
