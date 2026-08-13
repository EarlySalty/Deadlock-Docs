import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_referenzen

SEITE = """<!doctype html>
<html lang="de"><head>
  <meta charset="utf-8"><title>Titel</title>
  <meta name="tags" content="internal, test">
  <meta name="stand" content="2026-08-13">
  <meta name="quelle" content="Test">
</head><body><main>
  <h1>Titel</h1>
  <section id="s1"><h2>Abschnitt</h2><p>%s</p></section>
</main></body></html>
"""


class ReferenzenTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.basis = Path(self._tmp.name)
        self.repo = self.basis / "Quell-Repo"
        (self.repo / "rust" / "crates" / "dl-ding" / "src").mkdir(parents=True)
        (self.repo / "rust" / "crates" / "dl-ding" / "src" / "kern.rs").write_text("x")
        (self.repo / "scripts").mkdir()
        (self.repo / "scripts" / "run_dienst.sh").write_text("x")
        self.docs = self.basis / "Docs"
        (self.docs / "internal").mkdir(parents=True)

    def manifest(self):
        return {"version": 1, "repos": {"Quelle": {"verzeichnis": "Quell-Repo"}}, "seiten": {}}

    def seite(self, inhalt, name="internal/test.html"):
        ziel = self.docs / name
        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_text(SEITE % inhalt, encoding="utf-8")

    def pruefe(self):
        fehlend, _ = check_referenzen.pruefe(self.manifest(), self.basis, self.docs)
        return fehlend

    def test_vorhandener_pfad_wird_nicht_gemeldet(self):
        self.seite("Siehe rust/crates/dl-ding/src/kern.rs fuer Details.")
        self.assertEqual(self.pruefe(), {})

    def test_fehlender_pfad_wird_gemeldet(self):
        self.seite("Siehe rust/crates/dl-weg/src/kern.rs fuer Details.")
        self.assertEqual(self.pruefe(), {"internal/test.html": ["rust/crates/dl-weg/src/kern.rs"]})

    def test_gekuerzter_pfad_zaehlt_als_vorhanden(self):
        # Die Doku nennt oft nur den sprechenden Teil eines Pfades.
        self.seite("Der Kern liegt in src/kern.rs.")
        self.assertEqual(self.pruefe(), {})

    def test_nicht_versioniertes_skript_zaehlt_als_vorhanden(self):
        # Mehrere Repos ignorieren scripts/ bewusst; die Datei existiert trotzdem
        # und wird von systemd gestartet. Eine Git-Pruefung wuerde hier melden.
        self.seite("Start ueber scripts/run_dienst.sh.")
        self.assertEqual(self.pruefe(), {})

    def test_treffer_beginnt_nicht_mitten_im_pfad(self):
        # `dl-bot/src/kern.rs` darf nicht als fehlendes `bot/src/kern.rs`
        # gemeldet werden - der Bindestrich ist keine Wortgrenze.
        (self.repo / "rust" / "bin" / "dl-bot" / "src").mkdir(parents=True)
        (self.repo / "rust" / "bin" / "dl-bot" / "src" / "kern.rs").write_text("x")
        self.seite("Die Attribution steckt in dl-bot/src/kern.rs.")
        self.assertEqual(self.pruefe(), {})

    def test_treffer_beginnt_nicht_nach_einem_schraegstrich(self):
        # Ein laengerer Pfad darf nicht zusaetzlich sein eigenes Suffix melden.
        self.seite("Siehe rust/crates/dl-ding/src/kern.rs.")
        self.assertEqual(self.pruefe(), {})

    def test_pfad_mit_repo_praefix_wird_erkannt(self):
        self.seite("Start ueber Deadlock-Bots/scripts/run_dienst.sh.")
        self.assertEqual(self.pruefe(), {})

    def test_fehlender_pfad_mit_repo_praefix_wird_gemeldet(self):
        self.seite("Start ueber Deadlock-Bots/scripts/gibt_es_nicht.sh.")
        self.assertEqual(self.pruefe(),
                         {"internal/test.html": ["Deadlock-Bots/scripts/gibt_es_nicht.sh"]})

    def test_bauergebnisse_werden_ignoriert(self):
        self.seite("Das Bundle landet in frontend/dist und rust/target/release/dl-bot.")
        self.assertEqual(self.pruefe(), {})

    def test_shebang_pfade_werden_ignoriert(self):
        self.seite("Das Skript beginnt mit bin/bash und ruft bin/python auf.")
        self.assertEqual(self.pruefe(), {})

    def test_verweis_auf_andere_dokuseite_wird_ignoriert(self):
        self.seite("Details in bot/uebersicht.html.")
        self.assertEqual(self.pruefe(), {})

    def test_laufzeit_konfiguration_wird_ignoriert(self):
        self.seite("Die Werte stehen in bot/infisical.conf.")
        self.assertEqual(self.pruefe(), {})

    def test_mehrere_seiten_werden_getrennt_gefuehrt(self):
        self.seite("Fehlt: rust/crates/a/src/x.rs", "internal/a.html")
        self.seite("Fehlt: rust/crates/b/src/y.rs", "internal/unter/b.html")
        self.assertEqual(sorted(self.pruefe()), ["internal/a.html", "internal/unter/b.html"])

    def test_bericht_nennt_zahlen_und_pfade(self):
        self.seite("Fehlt: rust/crates/dl-weg/src/kern.rs")
        text = check_referenzen.bericht(self.pruefe(), 42, heute="2026-08-13")
        self.assertIn("fehlende Pfade: **1** auf 1 Seiten", text)
        self.assertIn("rust/crates/dl-weg/src/kern.rs", text)

    def test_bericht_ohne_treffer_sagt_das_deutlich(self):
        text = check_referenzen.bericht({}, 42, heute="2026-08-13")
        self.assertIn("Keine Treffer", text)

    def test_strict_meldet_fehler_nur_bei_treffern(self):
        pfad = self.basis / "quellen.json"
        pfad.write_text(json.dumps(self.manifest()), encoding="utf-8")

        def lauf():
            return check_referenzen.main([
                "--json", "--strict", "--manifest", str(pfad),
                "--repo-basis", str(self.basis), "--docs-root", str(self.docs),
            ])

        self.seite("Alles gut: rust/crates/dl-ding/src/kern.rs")
        self.assertEqual(lauf(), 0)
        self.seite("Kaputt: rust/crates/dl-weg/src/kern.rs")
        self.assertEqual(lauf(), 1)


if __name__ == "__main__":
    unittest.main()
