import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from knowledge_metadata import corpus_digest
from refresh_public_corpus import apply_validity_policy, atomic_json, faq_digest, refresh, summary, withdraw_invalid_audits


class FreshnessTests(unittest.TestCase):
    def test_new_public_page_without_audit_is_not_current_answer_knowledge(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / 'public/new.html'
            page.parent.mkdir()
            page.write_text('Neue ungeprüfte Behauptung')
            excluded = withdraw_invalid_audits(root, [])
            self.assertFalse(page.exists())
            self.assertEqual(excluded[0]['status'], 'pending')
            self.assertEqual((root / 'archive/public/new.html').read_text(), 'Neue ungeprüfte Behauptung')

    def test_stale_audit_withdraws_search_content_but_keeps_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'public').mkdir()
            page = root / 'public' / 'help.html'
            page.write_text('Geänderte Behauptung')
            audit = {'path': 'public/help.html', 'verified_at': '2026-09-20',
                     'content_sha256': hashlib.sha256(b'Alte Behauptung').hexdigest(),
                     'code': [{'repository': 'test'}], 'claims': [{'verdict': 'verified'}], 'gaps': []}
            excluded = withdraw_invalid_audits(root, [audit])
            self.assertFalse(page.exists())
            self.assertEqual((root / 'archive/public/help.html').read_text(), 'Geänderte Behauptung')
            self.assertEqual(excluded[0]['status'], 'pending')

    def test_conditional_verified_text_can_keep_separate_operational_gap(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'public').mkdir()
            page = root / 'public' / 'help.html'
            page.write_text('Wenn das aktive Profil VOD-Ton verlangt, benötigst du eine zusätzliche Spur.')
            audit = {'path': 'public/help.html', 'verified_at': '2026-09-20T12:00:00Z',
                     'content_sha256': hashlib.sha256(page.read_bytes()).hexdigest(),
                     'code': [{'repository': 'test'}], 'claims': [{'verdict': 'verified'}], 'gaps': [],
                     'operational_gaps': ['Dashboard und aktiver Dienst haben verschiedene Vorgaben.']}
            self.assertEqual(withdraw_invalid_audits(root, [audit]), [])
            report = {'repositories': [{'id': 'test', 'revision': 'abc', 'internal': 0,
                                       'unknown': 0, 'rejected': 0, 'documents': []}]}
            state = summary(root / 'public', report, [audit])
            self.assertEqual(state['totals']['verified_documents'], 1)
            self.assertEqual(state['repositories'][0]['last_verified_at'], audit['verified_at'])
            self.assertEqual(len(state['gaps']), 1)

    def test_historical_family_leaves_active_corpus_without_deleting_anchors(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / 'public/archive-guide/hero.html'
            page.parent.mkdir(parents=True)
            page.write_text('<section id="alter-anker">Historische Analyse</section>')
            policy = {'export_policy': [{'glob': 'archive-guide/*.html', 'status': 'historical',
                                        'reason': 'Nicht aktueller Patch'}]}
            excluded = apply_validity_policy(root, policy)
            self.assertEqual(len(excluded), 1)
            self.assertFalse(page.exists())
            self.assertIn('id="alter-anker"', (root / 'archive/public/archive-guide/hero.html').read_text())


class ActivationTests(unittest.TestCase):
    def setUp(self):
        from test_import_public_sources import ImportTests, PAGE
        self.fixture = ImportTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.page = PAGE
        self.docs = self.fixture.root / 'docs'
        self.docs.mkdir()
        self.git('init', '-q')
        (self.docs / 'public').mkdir()
        self.base = self.fixture.root / 'runtime'
        self.live_generation = 'previous'
        self.live_faq = None
        self.posts = 0
        self.fail_next = False
        self.config = {'repository': str(self.docs), 'base': str(self.base),
                       'knowledge_url': 'http://127.0.0.1:8896', 'fetch': False}
        self.commit_snapshot(self.page)

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.docs), *args], stderr=subprocess.DEVNULL).decode()

    def commit_snapshot(self, page):
        (self.docs / 'public/help.html').write_text(page)
        self.fixture.source['reviews']['help.md']['content_sha256'] = hashlib.sha256(page.encode()).hexdigest()
        self.fixture.config['audit_files'] = ['berichte/review.json']
        (self.docs / 'berichte').mkdir(exist_ok=True)
        (self.docs / 'berichte/review.json').write_text(json.dumps({'documents': [{
            'path': 'public/help.html', 'verified_at': '2026-09-20',
            'content_sha256': hashlib.sha256(page.encode()).hexdigest(),
            'code': self.fixture.source['reviews']['help.md']['code'],
            'claims': [{'verdict': 'verified'}], 'gaps': [],
        }]}))
        (self.docs / 'public-sources.json').write_text(json.dumps(self.fixture.config))
        self.git('add', '.')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'Snapshot')
        self.config['ref'] = self.git('rev-parse', 'HEAD').strip()

    def service(self, base_url, path, *, post=False):
        if post:
            self.posts += 1
            if self.fail_next:
                self.fail_next = False
                raise OSError('Fixture reload failed')
            self.live_generation = corpus_digest(self.base / 'current/public')
            self.live_faq = faq_digest((self.base / 'current').resolve())
            return {'chunks': 1}
        return {'generation': self.live_generation, 'faq_generation': self.live_faq}

    def test_activation_confirms_reader_and_unchanged_snapshot_does_not_reload(self):
        with patch('refresh_public_corpus.request', side_effect=self.service):
            state = refresh(self.config)
            self.assertEqual(state['refresh_status'], 'ok')
            self.assertEqual(self.live_generation, corpus_digest(self.base / 'current/public'))
            self.assertEqual(self.posts, 1)
            again = refresh(self.config)
            self.assertEqual(again['active_snapshot'], state['active_snapshot'])
            self.assertEqual(self.posts, 1)

    def test_failed_first_activation_removes_unconfirmed_current(self):
        self.fail_next = True
        with patch('refresh_public_corpus.request', side_effect=self.service):
            with self.assertRaises(OSError):
                refresh(self.config)
        self.assertFalse((self.base / 'current').is_symlink())
        state = json.loads((self.base / 'status-summary.json').read_text())
        self.assertNotIn('active_snapshot', state)
        self.assertEqual(state['refresh_status'], 'failed')

    def test_failed_reload_restores_and_confirms_previous_reader(self):
        with patch('refresh_public_corpus.request', side_effect=self.service):
            first = refresh(self.config)
            old = (self.base / 'current').resolve()
            self.commit_snapshot(self.page.replace('Öffne die Hilfe', 'Öffne die geprüfte Hilfe'))
            self.fail_next = True
            with self.assertRaises(OSError):
                refresh(self.config)
            self.assertEqual((self.base / 'current').resolve(), old)
            self.assertEqual(self.live_generation, corpus_digest(old / 'public'))
            state = json.loads((self.base / 'status-summary.json').read_text())
            self.assertEqual(state['active_snapshot'], first['active_snapshot'])
            self.assertEqual(state['refresh_status'], 'failed')

    def test_status_write_failure_rolls_back_confirmed_cutover(self):
        with patch('refresh_public_corpus.request', side_effect=self.service):
            first = refresh(self.config)
            old = (self.base / 'current').resolve()
            self.commit_snapshot(self.page.replace('Öffne die Hilfe', 'Öffne die aktualisierte Hilfe'))
            def fail_success_once(path, value):
                if value.get('refresh_status') == 'ok':
                    raise OSError('Fixture status write failed')
                atomic_json(path, value)
            with patch('refresh_public_corpus.atomic_json', side_effect=fail_success_once):
                with self.assertRaises(OSError):
                    refresh(self.config)
            self.assertEqual((self.base / 'current').resolve(), old)
            self.assertEqual(self.live_generation, corpus_digest(old / 'public'))
            self.assertEqual(json.loads((self.base / 'status-summary.json').read_text())['active_snapshot'], first['active_snapshot'])

    def test_html_generation_alone_cannot_confirm_wrong_faq(self):
        def stale_faq(base_url, path, *, post=False):
            result = self.service(base_url, path, post=post)
            if not post:
                result['faq_generation'] = 'stale-faq'
            return result
        with patch('refresh_public_corpus.request', side_effect=stale_faq):
            with self.assertRaisesRegex(ValueError, 'bestätigt'):
                refresh(self.config)
        self.assertFalse((self.base / 'current').is_symlink())


if __name__ == '__main__':
    unittest.main()
