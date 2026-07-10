import os
import subprocess
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
DEPLOY_SCRIPT = TOOLS_DIR / "deploy_corpus.sh"

VALID_PAGE = """<!doctype html>
<html lang="de"><head>
  <meta charset="utf-8">
  <title>Titel</title>
  <meta name="tags" content="discord-server, test">
  <meta name="stand" content="2026-07-10">
  <meta name="quelle" content="Test">
</head><body><main>
  <h1>{h1}</h1>
  <section id="s1"><h2>Abschnitt</h2><p>Text</p></section>
</main></body></html>
"""


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )


class DeployCorpusTest(unittest.TestCase):
    def setUp(self):
        self._repo_tmp = tempfile.TemporaryDirectory()
        self._base_tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._repo_tmp.name)
        self.base = Path(self._base_tmp.name) / "dl-knowledge"
        self.addCleanup(self._repo_tmp.cleanup)
        self.addCleanup(self._base_tmp.cleanup)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "t@example.invalid")
        git(self.repo, "config", "user.name", "Test")

    def write(self, rel, content):
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def commit(self, message):
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", message)
        return git(self.repo, "rev-parse", "HEAD").stdout.strip()

    def deploy(self, ref):
        env = dict(os.environ, DL_KNOWLEDGE_HOME=str(self.base))
        return subprocess.run(
            ["bash", str(DEPLOY_SCRIPT), ref],
            cwd=str(self.repo),
            env=env,
            capture_output=True,
            text=True,
        )

    def current_target(self):
        return os.readlink(self.base / "current")

    def test_reads_committed_commit_not_dirty_worktree(self):
        self.write("public/x.html", VALID_PAGE.format(h1="Committed"))
        sha = self.commit("v1")
        # Arbeitskopie schmutzig machen, ohne zu committen
        self.write("public/x.html", VALID_PAGE.format(h1="DIRTY-UNCOMMITTED"))

        result = self.deploy("HEAD")
        self.assertEqual(result.returncode, 0, result.stderr)

        deployed = (self.base / "current" / "public" / "x.html").read_text()
        self.assertIn("Committed", deployed)
        self.assertNotIn("DIRTY-UNCOMMITTED", deployed)
        self.assertEqual(self.current_target(), sha)

    def test_never_exports_internal(self):
        self.write("public/x.html", VALID_PAGE.format(h1="Pub"))
        self.write("internal/geheim.html", VALID_PAGE.format(h1="Intern"))
        self.commit("mit internal")

        result = self.deploy("HEAD")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.base / "current" / "public" / "x.html").exists())
        self.assertFalse((self.base / "current" / "internal").exists())

    def test_retains_older_snapshot(self):
        self.write("public/x.html", VALID_PAGE.format(h1="A"))
        sha_a = self.commit("A")
        self.assertEqual(self.deploy("HEAD").returncode, 0)

        self.write("public/x.html", VALID_PAGE.format(h1="B"))
        sha_b = self.commit("B")
        self.assertEqual(self.deploy("HEAD").returncode, 0)

        self.assertTrue((self.base / sha_a).is_dir(), "alter Snapshot fehlt")
        self.assertTrue((self.base / sha_b).is_dir())
        self.assertEqual(self.current_target(), sha_b)

    def test_updates_current_to_requested_sha(self):
        self.write("public/x.html", VALID_PAGE.format(h1="A"))
        sha_a = self.commit("A")
        self.write("public/x.html", VALID_PAGE.format(h1="B"))
        self.commit("B")

        # gezielt den aelteren Commit deployen
        result = self.deploy(sha_a)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.current_target(), sha_a)
        self.assertIn("A", (self.base / "current" / "public" / "x.html").read_text())

    def test_refuses_commit_without_public_html(self):
        self.write("public/nur-notiz.md", "# markdown")
        self.commit("kein html")

        result = self.deploy("HEAD")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(os.path.lexists(self.base / "current"))

    def test_refuses_invalid_public_html(self):
        # Seite ohne <h1> -> Validator lehnt ab -> current bleibt aus
        self.write("public/x.html", VALID_PAGE.format(h1="X").replace("<h1>X</h1>", ""))
        self.commit("invalid")

        result = self.deploy("HEAD")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(os.path.lexists(self.base / "current"))


if __name__ == "__main__":
    unittest.main()
