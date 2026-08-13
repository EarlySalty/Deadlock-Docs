import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_freshness


def git(repo, *args):
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True, capture_output=True, text=True,
    )


def commit(repo, rel, inhalt, nachricht):
    ziel = Path(repo) / rel
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(inhalt, encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-m", nachricht)
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()


class FreshnessTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.basis = Path(self._tmp.name)
        self.quelle = self.basis / "Quell-Repo"
        self.quelle.mkdir()
        git(self.quelle, "init", "-q", "-b", "main")
        git(self.quelle, "config", "user.email", "test@example.invalid")
        git(self.quelle, "config", "user.name", "Test")
        self.erste = commit(self.quelle, "src/kern.rs", "fn main() {}\n", "erster")

    def manifest(self, seiten, ausschluss=None):
        return {
            "version": 1,
            "ausschluss": ausschluss or [],
            "repos": {"Quelle": {"verzeichnis": "Quell-Repo", "branch": "main"}},
            "seiten": seiten,
        }

    def seite(self, pfade, geprueft):
        return {
            "internal/test.html": {
                "stand": "2026-07-01",
                "bindungen": [{
                    "repo": "Quelle", "pfade": pfade,
                    "geprueft": geprueft, "herkunft": "explizit",
                }],
            }
        }

    def pruefe(self, manifest):
        # Leere Doku-Wurzel: diese Faelle pruefen die Bindungen, nicht die
        # Vollstaendigkeit des Manifests.
        leer = self.basis / "Leer-Docs"
        leer.mkdir(exist_ok=True)
        return check_freshness.pruefe(manifest, self.basis, leer)

    def test_ohne_neue_commits_ist_die_seite_aktuell(self):
        [e] = self.pruefe(self.manifest(self.seite(["src"], self.erste)))
        self.assertEqual(e["status"], check_freshness.AKTUELL)
        self.assertEqual(e["commits"], 0)

    def test_commit_im_gebundenen_pfad_macht_veraltet(self):
        commit(self.quelle, "src/kern.rs", "fn main() { neu(); }\n", "zweiter")
        [e] = self.pruefe(self.manifest(self.seite(["src"], self.erste)))
        self.assertEqual(e["status"], check_freshness.VERALTET)
        self.assertEqual(e["commits"], 1)
        self.assertEqual(e["bindungen"][0]["dateien"], ["src/kern.rs"])

    def test_commit_ausserhalb_des_pfades_zaehlt_nicht(self):
        commit(self.quelle, "web/seite.ts", "export {}\n", "anderswo")
        [e] = self.pruefe(self.manifest(self.seite(["src"], self.erste)))
        self.assertEqual(e["status"], check_freshness.AKTUELL)

    def test_ausschluss_unterdrueckt_rauschpfade(self):
        commit(self.quelle, "src/logs/lauf.txt", "rauschen\n", "log")
        manifest = self.manifest(self.seite(["src"], self.erste), ausschluss=["logs"])
        [e] = self.pruefe(manifest)
        self.assertEqual(e["status"], check_freshness.AKTUELL)

    def test_fehlendes_repo_meldet_unbekannt_statt_aktuell(self):
        manifest = self.manifest(self.seite(["src"], self.erste))
        manifest["repos"]["Quelle"]["verzeichnis"] = "gibt-es-nicht"
        [e] = self.pruefe(manifest)
        self.assertEqual(e["status"], check_freshness.UNBEKANNT)
        self.assertIn("nicht gefunden", e["bindungen"][0]["hinweis"])

    def test_unbekannte_sha_meldet_unbekannt(self):
        [e] = self.pruefe(self.manifest(self.seite(["src"], "0" * 40)))
        self.assertEqual(e["status"], check_freshness.UNBEKANNT)

    def test_seite_ohne_bindung_ist_nicht_verfolgt(self):
        seiten = {"internal/notiz.html": {"stand": "2026-07-01", "bindungen": [], "grund": "kein Code"}}
        [e] = self.pruefe(self.manifest(seiten))
        self.assertEqual(e["status"], check_freshness.NICHT_VERFOLGT)

    def test_geprueft_neben_dem_branch_faellt_auf_den_vorfahr_zurueck(self):
        git(self.quelle, "checkout", "-q", "-b", "seitenzweig")
        seiten_sha = commit(self.quelle, "src/kern.rs", "// zweig\n", "auf dem Zweig")
        git(self.quelle, "checkout", "-q", "main")
        commit(self.quelle, "src/kern.rs", "// main\n", "auf main")
        [e] = self.pruefe(self.manifest(self.seite(["src"], seiten_sha)))
        self.assertEqual(e["status"], check_freshness.VERALTET)
        self.assertIn("gemeinsamem Vorfahr", e["bindungen"][0]["hinweis"])

    def test_eine_veraltete_bindung_genuegt_fuer_veraltet(self):
        zweite = self.basis / "Zweit-Repo"
        zweite.mkdir()
        git(zweite, "init", "-q", "-b", "main")
        git(zweite, "config", "user.email", "test@example.invalid")
        git(zweite, "config", "user.name", "Test")
        z_sha = commit(zweite, "a.txt", "eins\n", "erster")
        commit(zweite, "a.txt", "zwei\n", "zweiter")
        manifest = self.manifest({
            "internal/test.html": {
                "stand": "2026-07-01",
                "bindungen": [
                    {"repo": "Quelle", "pfade": ["src"], "geprueft": self.erste, "herkunft": "explizit"},
                    {"repo": "Zweit", "pfade": ["a.txt"], "geprueft": z_sha, "herkunft": "explizit"},
                ],
            }
        })
        manifest["repos"]["Zweit"] = {"verzeichnis": "Zweit-Repo", "branch": "main"}
        [e] = self.pruefe(manifest)
        self.assertEqual(e["status"], check_freshness.VERALTET)

    def test_praezision_unterscheidet_datei_von_verzeichnis(self):
        self.assertEqual(check_freshness.praezision(["src/kern.rs"]), check_freshness.GENAU)
        self.assertEqual(check_freshness.praezision(["src"]), check_freshness.GROB)
        self.assertEqual(check_freshness.praezision(["."]), check_freshness.GROB)
        self.assertEqual(check_freshness.praezision(["src/kern.rs", "web"]), check_freshness.GROB)

    def test_bericht_nennt_zahlen_und_seiten(self):
        commit(self.quelle, "src/kern.rs", "// neu\n", "zweiter")
        seiten = self.pruefe(self.manifest(self.seite(["src/kern.rs"], self.erste)))
        text = check_freshness.bericht(seiten, heute="2026-08-13")
        self.assertIn("veraltet: **1**, davon 1 mit genauer Bindung", text)
        self.assertIn("internal/test.html", text)
        self.assertIn("src/kern.rs", text)

    def test_seite_ohne_manifest_eintrag_wird_gemeldet(self):
        docs = self.basis / "Docs"
        (docs / "internal" / "neu").mkdir(parents=True)
        (docs / "internal" / "neu" / "seite.html").write_text("<h1>x</h1>", encoding="utf-8")
        manifest = self.manifest(self.seite(["src"], self.erste))
        seiten = check_freshness.pruefe(manifest, self.basis, docs)
        ungebunden = [e for e in seiten if e["status"] == check_freshness.UNGEBUNDEN]
        self.assertEqual([e["seite"] for e in ungebunden], ["internal/neu/seite.html"])

    def test_ungebundene_seite_laesst_den_lauf_auch_ohne_strict_scheitern(self):
        docs = self.basis / "Docs"
        (docs / "internal").mkdir(parents=True)
        (docs / "internal" / "seite.html").write_text("<h1>x</h1>", encoding="utf-8")
        manifest_pfad = self.basis / "quellen.json"
        manifest_pfad.write_text(json.dumps(self.manifest({})), encoding="utf-8")
        code = check_freshness.main([
            "--json", "--manifest", str(manifest_pfad),
            "--repo-basis", str(self.basis), "--docs-root", str(docs),
        ])
        self.assertEqual(code, 1)

    def test_strict_meldet_fehler_nur_bei_veralteten_seiten(self):
        manifest_pfad = self.basis / "quellen.json"
        docs = self.basis / "Docs"
        (docs / "internal").mkdir(parents=True)

        def lauf(argv):
            return check_freshness.main(argv + [
                "--manifest", str(manifest_pfad),
                "--repo-basis", str(self.basis),
                "--docs-root", str(docs),
            ])

        manifest_pfad.write_text(json.dumps(self.manifest(self.seite(["src"], self.erste))), encoding="utf-8")
        self.assertEqual(lauf(["--json", "--strict"]), 0)

        commit(self.quelle, "src/kern.rs", "// neu\n", "zweiter")
        self.assertEqual(lauf(["--json", "--strict"]), 1)
        self.assertEqual(lauf(["--json"]), 0)


if __name__ == "__main__":
    unittest.main()
