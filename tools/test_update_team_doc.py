import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import update_team_doc

PUBLIC_TEAM_DOC = (
    Path(__file__).resolve().parents[1]
    / "public"
    / "discord-server"
    / "team-und-ansprechpartner.html"
)


class ExtractMembersTest(unittest.TestCase):
    def test_extract_members_prefers_nick_then_global_name(self):
        response = {
            "members": [
                {
                    "member": {
                        "nick": "Nick",
                        "user": {"global_name": "Global", "username": "user1", "id": "1"},
                    }
                },
                {
                    "member": {
                        "nick": None,
                        "user": {"global_name": "Global", "username": "user2", "id": "2"},
                    }
                },
                {
                    "member": {
                        "user": {"global_name": None, "username": "user3", "id": "3"},
                    }
                },
            ]
        }

        self.assertEqual(
            update_team_doc.extract_members(response, "Testrolle"),
            [
                {"display_name": "Global", "username": "user2", "user_id": "2"},
                {"display_name": "Nick", "username": "user1", "user_id": "1"},
                {"display_name": "user3", "username": "user3", "user_id": "3"},
            ],
        )

    def test_extract_members_rejects_empty_role(self):
        with self.assertRaisesRegex(ValueError, "Testrolle"):
            update_team_doc.extract_members({"members": []}, "Testrolle")


class RenderHtmlTest(unittest.TestCase):
    def render(self):
        return update_team_doc.render_document(
            "2026-07-07",
            moderators=[
                {
                    "display_name": "Private Modperson",
                    "username": "private_mod_user",
                    "user_id": "10",
                },
                {"display_name": "Zoé<x>&", "username": "zoe<x>", "user_id": "13"},
            ],
            community_moderators=[
                {
                    "display_name": "Private Communityperson",
                    "username": "private_community_user",
                    "user_id": "11",
                }
            ],
            coaches=[
                {
                    "display_name": "Private Leorolle",
                    "username": "private_leo_user",
                    "user_id": update_team_doc.LEO_ID,
                },
                {
                    "display_name": "Private Nanirolle",
                    "username": "private_nani_user",
                    "user_id": update_team_doc.NANI_ID,
                },
                {
                    "display_name": "Private Coachperson",
                    "username": "private_coach_user",
                    "user_id": "12",
                },
            ],
        )

    def test_is_semantic_html_document(self):
        rendered = self.render()
        self.assertTrue(rendered.lstrip().lower().startswith("<!doctype html>"))
        self.assertIn('<html lang="de">', rendered)

    def test_required_metadata_present(self):
        rendered = self.render()
        self.assertIn('<meta charset="utf-8">', rendered)
        self.assertIn("<title>Team und Ansprechpartner</title>", rendered)
        self.assertIn(
            '<meta name="tags" content="discord-server, team, support, '
            'ansprechpartner, serverproblem, hilfe">',
            rendered,
        )
        self.assertIn('<meta name="stand" content="2026-07-07">', rendered)
        self.assertIn(
            '<meta name="quelle" content="Produktdokumentation und geprüftes '
            'sichtbares Verhalten">',
            rendered,
        )

    def test_exactly_one_main_and_one_h1(self):
        rendered = self.render()
        self.assertEqual(rendered.count("<main>"), 1)
        self.assertEqual(rendered.count("</main>"), 1)
        self.assertEqual(rendered.count("<h1>"), 1)

    def test_discord_member_data_is_not_rendered(self):
        rendered = self.render()
        for private_value in (
            "Private Modperson",
            "private_mod_user",
            "Zoé&lt;x&gt;&amp;",
            "zoe&lt;x&gt;",
            "Private Communityperson",
            "private_community_user",
            "Private Leorolle",
            "private_leo_user",
            "Private Nanirolle",
            "private_nani_user",
            "Private Coachperson",
            "private_coach_user",
        ):
            self.assertNotIn(private_value, rendered)

    def test_public_contract_describes_dynamic_groups_without_people(self):
        rendered = self.render()
        self.assertIn("Owner, Moderation, Community-Moderation und Coach", rendered)
        self.assertIn("Namen und Besetzung sind dynamisch", rendered)

    def test_public_support_sentence_is_self_contained(self):
        rendered = self.render()
        self.assertIn("<strong>Kurz:</strong>", rendered)
        self.assertIn(
            "Nutze beim Abschnitt <em>Community-Team</em> in <em>Willkommen</em> "
            "den Support-Schnellzugriff — von dort kümmert sich der Support um "
            "dein Serveranliegen.",
            rendered,
        )

    def test_render_matches_committed_public_contract_except_stand(self):
        committed = PUBLIC_TEAM_DOC.read_text(encoding="utf-8")
        self.assertEqual(
            update_team_doc.without_stand_line(committed),
            update_team_doc.without_stand_line(self.render()),
        )

    def test_no_discord_snowflakes_or_channel_ids(self):
        rendered = self.render()
        # keine Kanal-Mentions/Snowflakes im öffentlichen Text
        self.assertNotIn("<#", rendered)
        for snowflake in (
            "1459628609705738539",
            "1426220702054355077",
            "1494373349944459355",
        ):
            self.assertNotIn(snowflake, rendered)
        # keine pauschal verfügbare Concierge-DM behaupten
        self.assertNotIn("in den DMs", rendered)
        # stattdessen sichtbare, stabile Wege
        self.assertIn("Support-Schnellzugriff", rendered)
        self.assertIn("Willkommen", rendered)
        self.assertIn("/faq", rendered)

    def test_rendered_output_passes_validator(self):
        # lokaler Import: koppelt die Testmodule nicht beim Sammeln
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import validate_corpus

        rendered = self.render()
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "public" / "discord-server" / "team.html"
            page.parent.mkdir(parents=True)
            page.write_text(rendered, encoding="utf-8")
            self.assertEqual(validate_corpus.validate_root(tmp), [])


class UnchangedDetectionTest(unittest.TestCase):
    def test_only_stand_change_counts_as_unchanged(self):
        alt = update_team_doc.render_document(
            "2026-07-07", moderators=[], community_moderators=[], coaches=[]
        )
        neu = update_team_doc.render_document(
            "2026-07-08", moderators=[], community_moderators=[], coaches=[]
        )
        self.assertNotEqual(alt, neu)
        self.assertEqual(
            update_team_doc.without_stand_line(alt),
            update_team_doc.without_stand_line(neu),
        )

    def test_roster_change_does_not_change_public_render(self):
        alt = update_team_doc.render_document(
            "2026-07-07",
            moderators=[{"display_name": "A", "username": "a", "user_id": "1"}],
            community_moderators=[],
            coaches=[],
        )
        neu = update_team_doc.render_document(
            "2026-07-07",
            moderators=[{"display_name": "B", "username": "b", "user_id": "2"}],
            community_moderators=[],
            coaches=[],
        )
        self.assertEqual(
            update_team_doc.without_stand_line(alt),
            update_team_doc.without_stand_line(neu),
        )


class MainWiringTest(unittest.TestCase):
    def run_main(self):
        manager = Mock()
        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "team.html"
            doc.write_text("ALT", encoding="utf-8")
            with patch.object(update_team_doc, "DOC_PATH", doc), patch.object(
                update_team_doc, "render_from_discord", return_value="<!doctype html>NEU"
            ), patch.object(update_team_doc, "run") as run_mock, patch.object(
                update_team_doc, "reload_knowledge"
            ) as reload_mock:
                manager.attach_mock(run_mock, "run")
                manager.attach_mock(reload_mock, "reload")
                rc = update_team_doc.main([])
        return rc, manager.mock_calls

    def test_commit_push_deploy_reload_order(self):
        rc, calls = self.run_main()
        self.assertEqual(rc, 0)

        def index(pred):
            for i, c in enumerate(calls):
                if pred(c):
                    return i
            return -1

        push_i = index(lambda c: c[0] == "run" and list(c[1][0]) == ["git", "push"])
        deploy_i = index(
            lambda c: c[0] == "run"
            and str(c[1][0][0]).endswith("deploy_corpus.sh")
        )
        reload_i = index(lambda c: c[0] == "reload")

        self.assertNotEqual(push_i, -1, "git push wurde nicht aufgerufen")
        self.assertNotEqual(deploy_i, -1, "deploy_corpus.sh wurde nicht aufgerufen")
        self.assertNotEqual(reload_i, -1, "reload wurde nicht aufgerufen")
        self.assertLess(push_i, deploy_i, "Deploy muss nach dem Push laufen")
        self.assertLess(deploy_i, reload_i, "Reload muss nach dem Deploy laufen")

    def test_deploy_called_with_head(self):
        _, calls = self.run_main()
        deploy_calls = [
            c for c in calls
            if c[0] == "run" and str(c[1][0][0]).endswith("deploy_corpus.sh")
        ]
        self.assertEqual(len(deploy_calls), 1)
        self.assertEqual(list(deploy_calls[0][1][0]), [str(update_team_doc.DEPLOY_SCRIPT), "HEAD"])

    def test_unchanged_converges_without_new_commit(self):
        # Unverändertes Dokument darf keinen neuen Commit erzeugen, muss aber den
        # bestehenden HEAD über Push -> idempotenten Deploy -> Reload konvergieren
        # lassen (sonst hängt ein nach transientem Fehler alter Snapshot fest).
        rendered = update_team_doc.render_document(
            "2026-07-07", moderators=[], community_moderators=[], coaches=[]
        )
        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "team.html"
            doc.write_text(rendered, encoding="utf-8")
            with patch.object(update_team_doc, "DOC_PATH", doc), patch.object(
                update_team_doc, "render_from_discord", return_value=rendered
            ), patch.object(
                update_team_doc, "committed_doc", return_value=rendered
            ), patch.object(update_team_doc, "run") as run_mock, patch.object(
                update_team_doc, "deploy_corpus"
            ) as deploy_mock, patch.object(
                update_team_doc, "reload_knowledge"
            ) as reload_mock:
                rc = update_team_doc.main([])
        self.assertEqual(rc, 0)
        # kein neuer Commit
        committed = any(
            c[0] == "" and "commit" in list(c[1][0]) for c in run_mock.mock_calls
        )
        self.assertFalse(committed, "unverändert darf nicht committen")
        # aber Konvergenz: Push + idempotenter Deploy(HEAD) + Reload
        pushed = any(
            c[0] == "" and list(c[1][0]) == ["git", "push"] for c in run_mock.mock_calls
        )
        self.assertTrue(pushed, "Push muss zur Konvergenz laufen")
        deploy_mock.assert_called_once_with("HEAD")
        reload_mock.assert_called_once()

    def test_fail_then_retry_converges(self):
        # Lauf 1: Push ok, Deploy scheitert transient -> Reload nie erreicht.
        # Lauf 2: Dokument unverändert -> muss trotzdem Deploy+Reload nachholen.
        rendered = "<!doctype html>NEU"
        deploy = Mock(side_effect=[RuntimeError("deploy transient kaputt"), None])
        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "team.html"
            doc.write_text("ALT", encoding="utf-8")
            with patch.object(update_team_doc, "DOC_PATH", doc), patch.object(
                update_team_doc, "render_from_discord", return_value=rendered
            ), patch.object(
                # Lauf 1: noch nicht committet; Lauf 2: Commit ist am HEAD
                update_team_doc, "committed_doc", side_effect=["", rendered]
            ), patch.object(update_team_doc, "run") as run_mock, patch.object(
                update_team_doc, "deploy_corpus", deploy
            ), patch.object(update_team_doc, "reload_knowledge") as reload_mock:
                with self.assertRaises(RuntimeError):
                    update_team_doc.main([])
                self.assertEqual(doc.read_text(), rendered, "Doc vor Deploy geschrieben")
                reload_mock.assert_not_called()

                run_mock.reset_mock()
                rc = update_team_doc.main([])

        self.assertEqual(rc, 0)
        self.assertEqual(deploy.call_count, 2, "Deploy muss im Retry nachgeholt werden")
        reload_mock.assert_called_once()
        # Lauf 2 pusht (konvergiert einen ggf. zuvor fehlgeschlagenen Push), committet aber nicht
        pushed = any(
            c[0] == "" and list(c[1][0]) == ["git", "push"] for c in run_mock.mock_calls
        )
        committed = any(
            c[0] == "" and "commit" in list(c[1][0]) for c in run_mock.mock_calls
        )
        self.assertTrue(pushed)
        self.assertFalse(committed)

    def test_commit_fail_then_retry_recommits(self):
        # Lauf 1: write_text/add ok, aber git commit scheitert transient.
        # Lauf 2: Arbeitsdatei == Render, doch der HEAD kennt den Commit nie ->
        # der Retry darf nicht in den Unchanged-Zweig fallen und den alten HEAD
        # deployen, sondern muss erneut committen.
        rendered = "<!doctype html>NEU"
        commit_state = {"n": 0}

        def run_side(cmd, *a, **k):
            if list(cmd[:2]) == ["git", "commit"]:
                commit_state["n"] += 1
                if commit_state["n"] == 1:
                    raise RuntimeError("commit transient kaputt")

        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "team.html"
            doc.write_text("ALT", encoding="utf-8")
            with patch.object(update_team_doc, "DOC_PATH", doc), patch.object(
                update_team_doc, "render_from_discord", return_value=rendered
            ), patch.object(
                update_team_doc, "run", side_effect=run_side
            ) as run_mock, patch.object(
                update_team_doc, "deploy_corpus"
            ) as deploy_mock, patch.object(
                update_team_doc, "reload_knowledge"
            ) as reload_mock:
                with self.assertRaises(RuntimeError):
                    update_team_doc.main([])
                self.assertEqual(doc.read_text(), rendered, "Doc vor Commit geschrieben")
                deploy_mock.assert_not_called()
                reload_mock.assert_not_called()

                rc = update_team_doc.main([])

        self.assertEqual(rc, 0)
        self.assertEqual(commit_state["n"], 2, "Retry muss erneut committen")
        deploy_mock.assert_called_once_with("HEAD")
        reload_mock.assert_called_once()
        commits = [
            c for c in run_mock.mock_calls if list(c.args[0][:2]) == ["git", "commit"]
        ]
        self.assertEqual(len(commits), 2)


if __name__ == "__main__":
    unittest.main()
