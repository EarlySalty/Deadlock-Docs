import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate_corpus

CANONICAL = """<!doctype html>
<html lang="de"><head>
  <meta charset="utf-8">
  <title>Titel</title>
  <meta name="tags" content="discord-server, test">
  <meta name="stand" content="2026-07-10">
  <meta name="quelle" content="Test">
</head><body><main>
  <h1>Titel</h1>
  <section id="s1"><h2>Abschnitt</h2><p>Text</p></section>
</main></body></html>
"""


def write(root, rel, content):
    path = Path(root) / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


class ValidateCorpusTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.addCleanup(self._tmp.cleanup)

    def errors(self):
        return validate_corpus.validate_root(self.root)

    def joined(self):
        return "\n".join(self.errors())

    def test_accepts_minimal_canonical_page(self):
        write(self.root, "public/discord-server/team.html", CANONICAL)
        self.assertEqual(self.errors(), [])

    def test_accepts_valid_relative_link(self):
        write(self.root, "public/a.html", CANONICAL.replace(
            "<p>Text</p>", '<p>Text <a href="b.html">B</a></p>'
        ))
        write(self.root, "public/b.html", CANONICAL)
        self.assertEqual(self.errors(), [])

    def test_rejects_missing_metadata(self):
        broken = CANONICAL.replace(
            '<meta name="quelle" content="Test">', ""
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("quelle", self.joined())

    def test_rejects_missing_title(self):
        broken = CANONICAL.replace("<title>Titel</title>", "")
        write(self.root, "public/a.html", broken)
        self.assertIn("title", self.joined().lower())

    def test_rejects_missing_main(self):
        broken = CANONICAL.replace("<main>", "").replace("</main>", "")
        write(self.root, "public/a.html", broken)
        self.assertIn("main", self.joined().lower())

    def test_rejects_missing_h1(self):
        broken = CANONICAL.replace("<h1>Titel</h1>", "")
        write(self.root, "public/a.html", broken)
        self.assertIn("h1", self.joined().lower())

    def test_rejects_duplicate_ids(self):
        broken = CANONICAL.replace(
            '<section id="s1"><h2>Abschnitt</h2><p>Text</p></section>',
            '<section id="s1"><h2>A</h2></section><section id="s1"><h2>B</h2></section>',
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("id", self.joined().lower())

    def test_rejects_script(self):
        broken = CANONICAL.replace(
            "</main>", "<script>alert(1)</script></main>"
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("script", self.joined().lower())

    def test_rejects_external_stylesheet(self):
        broken = CANONICAL.replace(
            "</head>", '<link rel="stylesheet" href="https://cdn.example/x.css"></head>'
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_external_image(self):
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><img src="https://example.com/x.png"></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_broken_relative_link(self):
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><a href="fehlt.html">tot</a></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_markdown_knowledge_page(self):
        write(self.root, "public/a.html", CANONICAL)
        write(self.root, "public/alt.md", "# markdown")
        self.assertIn("alt.md", self.joined())

    def test_rejects_internal_markdown_page(self):
        write(self.root, "internal/x.md", "# markdown")
        self.assertIn("x.md", self.joined())

    def test_rejects_public_reference_to_internal(self):
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><a href="../../internal/geheim.html">x</a></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("internal", self.joined().lower())

    def test_root_level_markdown_is_allowed(self):
        # README/PLAN/CHANGELOG bleiben Markdown und sind keine Wissensseiten
        write(self.root, "public/a.html", CANONICAL)
        write(self.root, "README.md", "# readme")
        write(self.root, "PLAN.md", "# plan")
        self.assertEqual(self.errors(), [])

    def test_binary_evidence_asset_is_allowed(self):
        write(self.root, "internal/x.html", CANONICAL)
        (Path(self.root) / "internal" / "beweis.pdf").write_bytes(b"%PDF-1.4 fake")
        self.assertEqual(self.errors(), [])

    def test_cli_returns_nonzero_on_violation(self):
        write(self.root, "public/alt.md", "# markdown")
        self.assertEqual(validate_corpus.main([self.root]), 1)

    def test_cli_returns_zero_on_valid(self):
        write(self.root, "public/a.html", CANONICAL)
        self.assertEqual(validate_corpus.main([self.root]), 0)


if __name__ == "__main__":
    unittest.main()
