import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import update_team_doc


class TeamDocTest(unittest.TestCase):
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
                {"display_name": "Nick", "username": "user1", "user_id": "1"},
                {"display_name": "Global", "username": "user2", "user_id": "2"},
                {"display_name": "user3", "username": "user3", "user_id": "3"},
            ],
        )

    def test_extract_members_rejects_empty_role(self):
        with self.assertRaisesRegex(ValueError, "Testrolle"):
            update_team_doc.extract_members({"members": []}, "Testrolle")

    def test_render_document_filters_nani_and_marks_leo(self):
        rendered = update_team_doc.render_document(
            "2026-07-07",
            moderators=[{"display_name": "Mod", "username": "mod", "user_id": "10"}],
            community_moderators=[
                {"display_name": "Com", "username": "com", "user_id": "11"}
            ],
            coaches=[
                {"display_name": "Leo", "username": "leo", "user_id": "193685907071696896"},
                {"display_name": "Nani", "username": "earlysalty", "user_id": "662995601738170389"},
                {"display_name": "Coach", "username": "coach", "user_id": "12"},
            ],
        )

        self.assertIn("stand: 2026-07-07", rendered)
        self.assertIn("- **Mod** (Discord: `mod`)", rendered)
        self.assertIn("- **Com** (Discord: `com`)", rendered)
        self.assertIn(
            "- **Leo** (Discord: `leo`), organisiert auch die Scrims", rendered
        )
        self.assertIn("- **Coach** (Discord: `coach`)", rendered)
        self.assertIn("- **Nani** selbst coacht ebenfalls", rendered)
        coaches_section = rendered.split("## Coaches", 1)[1].split("## Paten", 1)[0]
        self.assertNotIn("(Discord: `earlysalty`)", coaches_section)


if __name__ == "__main__":
    unittest.main()
