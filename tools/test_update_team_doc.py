import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import update_team_doc


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
                {"display_name": "Mod", "username": "mod", "user_id": "10"},
                # deckt HTML-Escaping und UTF-8 ab
                {"display_name": "Zoé<x>&", "username": "zoe<x>", "user_id": "13"},
            ],
            community_moderators=[
                {"display_name": "Com", "username": "com", "user_id": "11"}
            ],
            coaches=[
                {"display_name": "Leo", "username": "leo", "user_id": update_team_doc.LEO_ID},
                {"display_name": "Nani", "username": "earlysalty", "user_id": update_team_doc.NANI_ID},
                {"display_name": "Coach", "username": "coach", "user_id": "12"},
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
        self.assertIn('<meta name="tags" content="discord-server, team, support">', rendered)
        self.assertIn('<meta name="stand" content="2026-07-07">', rendered)
        self.assertIn('<meta name="quelle" content="Discord-Rollenabfrage">', rendered)

    def test_exactly_one_main_and_one_h1(self):
        rendered = self.render()
        self.assertEqual(rendered.count("<main>"), 1)
        self.assertEqual(rendered.count("</main>"), 1)
        self.assertEqual(rendered.count("<h1>"), 1)

    def test_discord_display_names_are_escaped(self):
        rendered = self.render()
        # Rohtext darf nicht als Markup landen
        self.assertNotIn("Zoé<x>&", rendered)
        self.assertNotIn("zoe<x>", rendered)
        # escaped Variante muss vorhanden sein
        self.assertIn("Zoé&lt;x&gt;&amp;", rendered)
        self.assertIn("zoe&lt;x&gt;", rendered)

    def test_filters_nani_and_marks_leo(self):
        rendered = self.render()
        self.assertIn("Mod", rendered)
        self.assertIn("Com", rendered)
        self.assertIn("Leo", rendered)
        self.assertIn("organisiert auch die Scrims", rendered)
        self.assertIn("Coach", rendered)
        coaches_section = rendered.split(">Coaches<", 1)[1]
        self.assertNotIn("earlysalty", coaches_section)

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

    def test_content_change_counts_as_changed(self):
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
        self.assertNotEqual(
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

    def test_unchanged_skips_commit_deploy_reload(self):
        manager = Mock()
        rendered = update_team_doc.render_document(
            "2026-07-07", moderators=[], community_moderators=[], coaches=[]
        )
        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "team.html"
            doc.write_text(rendered, encoding="utf-8")
            with patch.object(update_team_doc, "DOC_PATH", doc), patch.object(
                update_team_doc, "render_from_discord", return_value=rendered
            ), patch.object(update_team_doc, "run") as run_mock, patch.object(
                update_team_doc, "reload_knowledge"
            ) as reload_mock:
                rc = update_team_doc.main([])
        self.assertEqual(rc, 0)
        run_mock.assert_not_called()
        reload_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
