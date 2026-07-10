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
        # gültiges internes Ziel anlegen, damit die Broken-Link-Prüfung NICHT
        # feuert und wir wirklich die Inhaltsgrenze prüfen
        write(self.root, "internal/geheim.html", CANONICAL)
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><a href="../../internal/geheim.html">x</a></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("öffentliche Referenz auf internal/", self.joined())

    def test_rejects_public_reference_to_internal_uppercase(self):
        write(self.root, "internal/geheim.html", CANONICAL)
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><a href="../../INTERNAL/geheim.html">x</a></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("öffentliche Referenz auf internal/", self.joined())

    def test_rejects_public_reference_to_internal_entity_encoded(self):
        broken = CANONICAL.replace(
            "<p>Text</p>", "<p>siehe internal&#47;geheim</p>"
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("öffentliche Referenz auf internal/", self.joined())

    def test_rejects_missing_doctype(self):
        broken = CANONICAL.replace("<!doctype html>\n", "")
        write(self.root, "public/a.html", broken)
        self.assertIn("doctype", self.joined().lower())

    def test_rejects_wrong_html_lang(self):
        broken = CANONICAL.replace('<html lang="de">', '<html lang="en">')
        write(self.root, "public/a.html", broken)
        self.assertIn("lang", self.joined().lower())

    def test_rejects_missing_head(self):
        broken = CANONICAL.replace("<head>", "").replace("</head>", "")
        write(self.root, "public/a.html", broken)
        self.assertIn("head", self.joined().lower())

    def test_rejects_missing_body(self):
        broken = CANONICAL.replace("<body>", "").replace("</body>", "")
        write(self.root, "public/a.html", broken)
        self.assertIn("body", self.joined().lower())

    def test_rejects_missing_charset(self):
        broken = CANONICAL.replace('<meta charset="utf-8">\n', "")
        write(self.root, "public/a.html", broken)
        self.assertIn("charset", self.joined().lower())

    def test_rejects_two_main(self):
        broken = CANONICAL.replace("</main>", "</main><main></main>")
        write(self.root, "public/a.html", broken)
        self.assertIn("main", self.joined().lower())

    def test_rejects_two_h1(self):
        broken = CANONICAL.replace("<h1>Titel</h1>", "<h1>Titel</h1><h1>Zwei</h1>")
        write(self.root, "public/a.html", broken)
        self.assertIn("h1", self.joined().lower())

    def test_rejects_h1_outside_main(self):
        broken = CANONICAL.replace(
            "<body><main>\n  <h1>Titel</h1>",
            "<body>\n  <h1>Titel</h1><main>",
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(any("main" in e.lower() and "h1" in e.lower()
                            for e in self.errors()), self.joined())

    def test_accepts_external_anchor(self):
        page = CANONICAL.replace(
            "<p>Text</p>",
            '<p>Quelle: <a href="https://example.com/quelle">Beleg</a></p>',
        )
        write(self.root, "public/a.html", page)
        self.assertEqual(self.errors(), [])

    def test_rejects_javascript_anchor(self):
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><a href="javascript:alert(1)">x</a></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_data_uri_anchor(self):
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><a href="data:text/html,<b>x</b>">x</a></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_data_uri_image(self):
        broken = CANONICAL.replace(
            "<p>Text</p>",
            '<p><img src="data:image/png;base64,AAAA"></p>',
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_external_srcset(self):
        broken = CANONICAL.replace(
            "<p>Text</p>",
            '<p><img srcset="https://cdn.example/x.png 1x, y.png 2x"></p>',
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_external_xlink_href(self):
        broken = CANONICAL.replace(
            "<p>Text</p>",
            '<p><svg><use xlink:href="https://evil.example/s.svg#i"/></svg></p>',
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_meta_refresh(self):
        broken = CANONICAL.replace(
            "</head>",
            '<meta http-equiv="refresh" content="0; url=https://evil.example/"></head>',
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("refresh", self.joined().lower())

    def test_rejects_css_import(self):
        broken = CANONICAL.replace(
            "</head>",
            '<style>@import url("https://evil.example/x.css");</style></head>',
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("import", self.joined().lower())

    def test_rejects_css_external_url(self):
        broken = CANONICAL.replace(
            "</head>",
            "<style>body{background:url(https://evil.example/bg.png)}</style></head>",
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_inline_style_external_url(self):
        broken = CANONICAL.replace(
            "<p>Text</p>",
            '<p style="background:url(https://evil.example/bg.png)">x</p>',
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_symlink_page(self):
        write(self.root, "public/x.html", CANONICAL)
        (Path(self.root) / "internal").mkdir(parents=True, exist_ok=True)
        (Path(self.root) / "internal" / "geheim.html").write_text(CANONICAL, encoding="utf-8")
        link = Path(self.root) / "public" / "evil.html"
        link.symlink_to("../internal/geheim.html")
        self.assertIn("symlink", self.joined().lower())

    def test_rejects_dir_symlink(self):
        write(self.root, "public/x.html", CANONICAL)
        (Path(self.root) / "internal").mkdir(parents=True, exist_ok=True)
        link = Path(self.root) / "public" / "sub"
        link.symlink_to("../internal")
        self.assertIn("symlink", self.joined().lower())

    def test_rejects_relative_path_escape(self):
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><a href="../../../etc/passwd">x</a></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_two_titles(self):
        broken = CANONICAL.replace(
            "<title>Titel</title>", "<title>Titel</title><title>Zwei</title>"
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("title", self.joined().lower())

    def test_rejects_two_charset_metas(self):
        broken = CANONICAL.replace(
            '<meta charset="utf-8">', '<meta charset="utf-8"><meta charset="utf-8">'
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("charset", self.joined().lower())

    def test_rejects_duplicate_required_meta(self):
        broken = CANONICAL.replace(
            '<meta name="tags" content="discord-server, test">',
            '<meta name="tags" content="discord-server, test">'
            '<meta name="tags" content="x">',
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("tags", self.joined().lower())

    def test_rejects_empty_tags(self):
        broken = CANONICAL.replace(
            'content="discord-server, test"', 'content=", ,"'
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("tags", self.joined().lower())

    def test_rejects_nested_h1(self):
        # h1 muss direktes Kind von main sein, nicht bloß irgendwo darin
        broken = CANONICAL.replace(
            "<h1>Titel</h1>", "<div><h1>Titel</h1></div>"
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(
            any("h1" in e.lower() and "main" in e.lower() for e in self.errors()),
            self.joined(),
        )

    def test_rejects_section_without_heading_or_id(self):
        broken = CANONICAL.replace(
            '<section id="s1"><h2>Abschnitt</h2><p>Text</p></section>',
            "<section><p>Text</p></section>",
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("section", self.joined().lower())

    def test_rejects_misnested_shell(self):
        # falsch verschachtelte Hülle <body><head> muss auffallen
        broken = (
            "<!doctype html>\n"
            '<html lang="de"><body><head>\n'
            '  <meta charset="utf-8">\n'
            "  <title>Titel</title>\n"
            '  <meta name="tags" content="discord-server, test">\n'
            '  <meta name="stand" content="2026-07-10">\n'
            '  <meta name="quelle" content="Test">\n'
            "</head><main>\n"
            "  <h1>Titel</h1>\n"
            '  <section id="s1"><h2>Abschnitt</h2><p>Text</p></section>\n'
            "</main></body></html>\n"
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("head", self.joined().lower())

    def test_rejects_form_action_javascript(self):
        broken = CANONICAL.replace(
            "<p>Text</p>",
            '<form action="javascript:alert(1)"><button>x</button></form>',
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_css_missing_local_target(self):
        broken = CANONICAL.replace(
            "</head>", "<style>body{background:url(fehlt.png)}</style></head>"
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_css_local_path_escape(self):
        broken = CANONICAL.replace(
            "</head>",
            "<style>body{background:url(../../../etc/passwd)}</style></head>",
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_htm_page(self):
        write(self.root, "public/a.html", CANONICAL)
        write(self.root, "public/alt.htm", CANONICAL)
        self.assertIn("alt.htm", self.joined())

    def test_rejects_ftp_anchor(self):
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><a href="ftp://host/datei">x</a></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

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

    # --- doppelte Attribute (HTML5: erstes gewinnt, Validator-Dict: letztes) ---

    def test_rejects_duplicate_url_attribute(self):
        # Decoy-Ziel darf die externe Erst-URL nicht verdecken: der HTML5-Baum
        # lädt src="https://evil...", nur das Duplikat muss den Fund auslösen
        write(self.root, "public/ok.png", "decoy")
        broken = CANONICAL.replace(
            "<p>Text</p>",
            '<p><img src="https://evil.example/x.png" src="ok.png"></p>',
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("attribut", self.joined().lower())

    def test_rejects_duplicate_meta_attribute(self):
        # Validator-Dict sähe name="tags"; die Runtime sieht name="wrong"
        broken = CANONICAL.replace(
            '<meta name="tags" content="discord-server, test">',
            '<meta name="wrong" name="tags" content="discord-server, test">',
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("attribut", self.joined().lower())

    # --- URL-Scheme-Fläche schließen (imagesrcset, ftp/file trotz Decoy) ---

    def test_rejects_external_imagesrcset(self):
        write(self.root, "public/ok.png", "decoy")
        broken = CANONICAL.replace(
            "</head>",
            '<link rel="preload" as="image" href="ok.png" '
            'imagesrcset="https://evil.example/x.png 1x"></head>',
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_ftp_anchor_even_with_local_decoy(self):
        # Decoy an genau der Stelle, auf die der frühere lokale Fallback zeigte;
        # der Scheme-Wert darf nicht mehr in die Meldung geleakt werden.
        write(self.root, "public/ftp:/host/datei", "decoy")
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><a href="ftp://host/datei">x</a></p>'
        )
        write(self.root, "public/a.html", broken)
        joined = self.joined()
        self.assertIn("navigation", joined.lower())
        self.assertNotIn("ftp", joined.lower())

    def test_rejects_file_scheme_asset_even_with_local_decoy(self):
        write(self.root, "public/file:/decoy/x.png", "decoy")
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><img src="file://decoy/x.png"></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    # --- Runtime-Vertrag: sichtbarer h1-Text, nichtleere Section, exakte Endung ---

    def test_rejects_whitespace_only_h1(self):
        broken = CANONICAL.replace("<h1>Titel</h1>", "<h1>   </h1>")
        write(self.root, "public/a.html", broken)
        self.assertTrue(any("h1" in e.lower() for e in self.errors()), self.joined())

    def test_rejects_empty_direct_main_section(self):
        # id und h2 vorhanden, aber ohne sichtbaren Inhalt: Runtime verwirft das
        broken = CANONICAL.replace(
            '<section id="s1"><h2>Abschnitt</h2><p>Text</p></section>',
            '<section id="s1"><h2></h2></section>',
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("section", self.joined().lower())

    def test_rejects_uppercase_html_suffix(self):
        # Rust-Collector nimmt nur exakt .html; .HTML würde stumm nicht indexiert
        write(self.root, "public/seite.HTML", CANONICAL)
        self.assertIn("seite.HTML", self.joined())

    # --- Browser-nahe URL-Klassifikation: protokoll-relativ/Backslash/C0 ---

    def test_rejects_protocol_relative_navigation(self):
        # Browser navigiert //host extern; früher fälschlich als sichere
        # Navigation erlaubt. Nur http/https/mailto/tel bleiben zulässig.
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><a href="//evil.example/x">x</a></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_backslash_asset_with_local_decoy(self):
        # \\evil\x.png normalisiert der Browser zu //evil/x.png (extern); ein
        # lokaler Decoy an der Backslash-Pfadstelle darf den Fund nicht verdecken
        write(self.root, r"public/\\evil.example\x.png", "decoy")
        broken = CANONICAL.replace(
            "<p>Text</p>", r'<p><img src="\\evil.example\x.png"></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_c0_prefixed_protocol_relative_asset_with_decoy(self):
        # Browser entfernt führende C0-Steuerzeichen: \x01//evil wird //evil
        # (extern). Decoy am buggy aufgelösten Pfad darf den Fund nicht verdecken.
        write(self.root, "public/\x01/evil.example/x.png", "decoy")
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><img src="\x01//evil.example/x.png"></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_backslash_srcset_with_local_decoy(self):
        # gleiche Normalisierung muss im srcset-Pfad greifen (keine Kategorie-Drift)
        write(self.root, r"public/\\evil.example\x.png", "decoy")
        broken = CANONICAL.replace(
            "<p>Text</p>", r'<p><img srcset="\\evil.example\x.png 1x"></p>'
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_c0_css_url_with_local_decoy(self):
        # gleiche Normalisierung muss im CSS-url()-Pfad greifen
        write(self.root, "public/\x01/evil.example/bg.png", "decoy")
        broken = CANONICAL.replace(
            "</head>",
            "<style>body{background:url(\x01//evil.example/bg.png)}</style></head>",
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_dead_link_error_does_not_leak_query(self):
        # Fehlermeldungen dürfen keine URL-/Query-Werte (z. B. Tokens) preisgeben
        broken = CANONICAL.replace(
            "<p>Text</p>",
            '<p><a href="missing.png?access_token=CANARY_SECRET">x</a></p>',
        )
        write(self.root, "public/a.html", broken)
        joined = self.joined()
        self.assertTrue(self.errors())
        self.assertNotIn("CANARY_SECRET", joined)

    # --- HTML5-Parität: h1 nimmt nur Inline-Phrasing-Inhalt auf ---

    def test_rejects_h1_with_nested_h2(self):
        # HTML5/Rust repariert <h2> aus <h1> heraus; Python-HTMLParser zählt den
        # h2-Text fälschlich als h1-Text -> Paritätslücke, muss abgelehnt werden
        broken = CANONICAL.replace("<h1>Titel</h1>", "<h1><h2>Titel</h2></h1>")
        write(self.root, "public/a.html", broken)
        self.assertTrue(any("h1" in e.lower() for e in self.errors()), self.joined())

    def test_rejects_h1_with_block_descendant(self):
        # auch tiefer verschachtelte Block-Nachfahren werden abgelehnt
        broken = CANONICAL.replace(
            "<h1>Titel</h1>", "<h1><span><div>Titel</div></span></h1>"
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(any("h1" in e.lower() for e in self.errors()), self.joined())

    def test_accepts_inline_phrasing_in_h1(self):
        # Inline-Phrasing bleibt unterstützt (a/span/code/em/strong/br)
        page = CANONICAL.replace(
            "<h1>Titel</h1>",
            '<h1>Team <span>Deadlock</span> <code>v2</code> <em>neu</em> '
            '<strong>wow</strong><br><a href="b.html">mehr</a></h1>',
        )
        write(self.root, "public/a.html", page)
        write(self.root, "public/b.html", CANONICAL)
        self.assertEqual(self.errors(), [])

    # --- Task 1: CSS-Backslash-Escapes, ping-Telemetrie, urlparse-Fehler ---

    def test_rejects_css_function_escape(self):
        # CSS-Escape u\72l(...) ist für den Browser url(...); die Regex sieht kein
        # literales "url(" und würde das externe Ziel durchlassen. Jeder Backslash
        # in Style-Blöcken/-Attributen wird als kanonischer Vertrag abgelehnt.
        broken = CANONICAL.replace(
            "</head>",
            "<style>body{background:u\\72l(https://evil.example/bg.png)}</style></head>",
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("backslash", self.joined().lower())

    def test_rejects_css_escaped_colon_url_with_decoy(self):
        # url(http\00003a//...) versteckt den Doppelpunkt als CSS-Escape; nach der
        # Backslash->Slash-Normalisierung sieht der Klassifikator ein lokales Ziel.
        # Decoy am buggy aufgelösten Pfad darf den Fund nicht verdecken.
        write(self.root, "public/http/00003a/evil.example/bg.png", "decoy")
        broken = CANONICAL.replace(
            "<p>Text</p>",
            '<p style="background:url(http\\00003a//evil.example/bg.png)">x</p>',
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("backslash", self.joined().lower())

    def test_rejects_nonempty_ping_multiple_targets(self):
        # ping ist eine Whitespace-Liste von Beacon-Zielen; der Browser pingt jedes
        # einzeln. Der Einzel-String-Klassifikator hält "track https://evil" für
        # lokal (Decoy existiert) und übersieht den Tracker. Aktive Telemetrie ist
        # unnötig: jedes nichtleere ping-Attribut wird rundheraus abgelehnt.
        write(self.root, "public/track https:/evil.example/beacon", "decoy")
        write(self.root, "public/b.html", CANONICAL)
        broken = CANONICAL.replace(
            "<p>Text</p>",
            '<p><a href="b.html" ping="track https://evil.example/beacon">x</a></p>',
        )
        write(self.root, "public/a.html", broken)
        self.assertIn("ping", self.joined().lower())

    def test_rejects_nfkc_invalid_netloc_url(self):
        # urlparse wirft bei NFKC-invalider netloc (U+2100 -> "a/c") ValueError.
        # Die Validierung muss eine stabile Kategorie-Meldung liefern, nie werfen
        # und weder den Wert noch die netloc spiegeln.
        broken = CANONICAL.replace(
            "<p>Text</p>", '<p><img src="http://exa℀mple.com/x.png"></p>'
        )
        write(self.root, "public/a.html", broken)
        joined = self.joined()  # darf nicht werfen
        self.assertTrue(self.errors())
        self.assertNotIn("℀", joined)
        self.assertNotIn("mple.com", joined)

    # --- Task 2: strikte kanonische Verschachtelung ---

    def test_rejects_h1_with_unmatched_h2_close(self):
        # HTML5 schließt <h1> beim </h2> und lässt ein LEERES h1 zurück; der
        # tolerante Parser hält h1 offen und zählt "Titel" fälschlich als h1-Text.
        # Fehlerhafte Verschachtelung muss abgelehnt werden.
        broken = CANONICAL.replace("<h1>Titel</h1>", "<h1></h2>Titel</h1>")
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_misnested_inline(self):
        # <b><i>x</b></i> ist misnested; tolerantes Reparieren würde es verschlucken
        broken = CANONICAL.replace(
            "<p>Text</p>", "<p><b><i>x</b></i></p>"
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_unclosed_span(self):
        # <span> ohne schließendes Tag: das folgende </section> schließt es tolerant
        broken = CANONICAL.replace(
            "<p>Text</p>", "<p>Text</p><span>offen"
        )
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    def test_rejects_unclosed_document(self):
        # Dokument endet mit offenen Elementen (kein </main></body></html>)
        broken = CANONICAL.replace("</main></body></html>", "")
        write(self.root, "public/a.html", broken)
        self.assertTrue(self.errors())

    # --- Task 2: vollständige sichere H1-Phrasing-Allowlist ---

    def test_accepts_abbr_in_h1(self):
        # normales Text-Formatting (abbr) ist erlaubtes Inline-Phrasing im h1
        page = CANONICAL.replace(
            "<h1>Titel</h1>",
            '<h1><abbr title="Deadlock">DL</abbr> Team</h1>',
        )
        write(self.root, "public/a.html", page)
        self.assertEqual(self.errors(), [])

    # --- Task 1 Fix 6: Slash-Selbstschluss nur für Void-Elemente ---

    def test_rejects_nonvoid_self_closing_tag(self):
        # <style/> ist kein Void-Element: HTML5 ignoriert den Slash und hält
        # <style> offen (schluckt Folgeinhalt als CSS), Python-HTMLParser
        # behandelt es als selbstschließend. Diese Paritätslücke muss fail-closed
        # als fehlerhafte Verschachtelung abgelehnt werden.
        broken = CANONICAL.replace("</main>", "<style/></main>")
        write(self.root, "public/a.html", broken)
        self.assertIn("verschachtelung", self.joined().lower())

    def test_accepts_void_self_closing_tag(self):
        # kanonischer Void-Selbstschluss <br/> bleibt zulässig – nur Void-Elemente
        # dürfen den Slash tragen
        page = CANONICAL.replace("<p>Text</p>", "<p>Zeile<br/>Zwei</p>")
        write(self.root, "public/a.html", page)
        self.assertEqual(self.errors(), [])


if __name__ == "__main__":
    unittest.main()
