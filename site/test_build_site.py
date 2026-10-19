import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_site as b

SENTINEL = "PRIVATE-SENTINEL-8841"


def copy_skill(dst):
    src = b.SKILL
    dst = Path(dst)
    for rel in ["SKILL.md", "references", "design", "site/content", "site/pictures", "site/forbidden.txt"]:
        s = src / rel
        if not s.exists():
            continue
        t = dst / rel
        t.parent.mkdir(parents=True, exist_ok=True)
        if s.is_dir():
            shutil.copytree(s, t)
        else:
            shutil.copyfile(s, t)
    (dst / "references" / "local.md").write_text("# Private\n\n%s\n" % SENTINEL, encoding="utf-8")
    return dst


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.skill = copy_skill(self.tmp / "skill")

    def test_table_has_16_rows(self):
        rows = b.parse_elements((b.SKILL / "SKILL.md").read_text(encoding="utf-8"))
        self.assertEqual(len(rows), 16)
        self.assertEqual([r["num"] for r in rows], list(range(1, 17)))
        self.assertTrue(all(r["ref"].startswith("references/") for r in rows))

    def test_names_file_must_have_16_ordered_rows(self):
        p = self.skill / "site/content/element-names.md"
        good = p.read_text(encoding="utf-8")
        lines = good.rstrip("\n").split("\n")
        for bad in ["\n".join(lines[:-1]) + "\n",
                    "\n".join(lines[:3] + lines[4:]) + "\n",
                    "\n".join(lines[:2] + [lines[3], lines[2]] + lines[4:]) + "\n"]:
            p.write_text(bad, encoding="utf-8")
            with self.assertRaises(b.BuildError):
                b.build(self.skill, self.tmp / "bad")
        p.write_text(good, encoding="utf-8")
        b.build(self.skill, self.tmp / "good")

    def test_plain_names_used(self):
        b.build(self.skill, self.tmp / "o")
        idx = (self.tmp / "o/index.html").read_text(encoding="utf-8")
        self.assertIn("What it means for you", idx)
        self.assertIn('href="elements/command-palette.html"', idx)
        self.assertIn('href="settings.html"', idx)
        self.assertNotIn("chord", idx.lower())
        self.assertNotIn("Switcher ,", idx)
        page = (self.tmp / "o/elements/command-palette.html").read_text(encoding="utf-8")
        self.assertIn("The rule in detail", page)

    def test_local_md_never_appears(self):
        out = self.tmp / "out"
        b.build(self.skill, out)
        for p in out.rglob("*"):
            if p.is_file():
                self.assertNotIn(SENTINEL, p.read_text(encoding="utf-8", errors="ignore"), p)
                self.assertNotIn("local.md", p.read_text(encoding="utf-8", errors="ignore"), p)

    def test_forbidden_string_fails_build(self):
        forbidden = b.load_forbidden(self.skill / 'site' / 'forbidden.txt')
        if forbidden is None:
            self.skipTest("site/forbidden.txt absent (public repo)")
        for bad in ["see %s" % f for f in forbidden] + [f.upper() for f in forbidden]:
            (self.skill / "site/content/home.md").write_text("# Home\n\n%s\n" % bad, encoding="utf-8")
            with self.assertRaises(b.BuildError, msg=bad):
                b.build(self.skill, self.tmp / "out2")

    def test_deterministic(self):
        a, c = self.tmp / "a", self.tmp / "c"
        b.build(self.skill, a)
        b.build(self.skill, c)
        fa = sorted(p.relative_to(a) for p in a.rglob("*") if p.is_file())
        fc = sorted(p.relative_to(c) for p in c.rglob("*") if p.is_file())
        self.assertEqual(fa, fc)
        for rel in fa:
            self.assertEqual((a / rel).read_bytes(), (c / rel).read_bytes(), rel)

    def test_missing_content_gets_placeholder(self):
        (self.skill / "site/content/home.md").unlink()
        b.build(self.skill, self.tmp / "o")
        self.assertIn("has not been written yet", (self.tmp / "o/index.html").read_text(encoding="utf-8"))

    def test_nojekyll_and_pages(self):
        b.build(self.skill, self.tmp / "o")
        o = self.tmp / "o"
        self.assertTrue((o / ".nojekyll").exists())
        for n in ["index.html", "settings.html", "settings-mockup.html", "skill.html",
                  "use-with-your-agent.html", "style.css"]:
            self.assertTrue((o / n).exists(), n)
        self.assertEqual(len(list((o / "elements").glob("*.html"))), 15)

    def test_settings_history_page_and_images(self):
        out = self.tmp / "o"
        b.build(self.skill, out)
        page = out / "settings-history.html"
        self.assertTrue(page.exists())
        imgs = re.findall(r'<img src="([^"]+)"', page.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(imgs), 4)
        for i in imgs:
            self.assertTrue((out / i).is_file(), i)
        self.assertIn("settings-history.html", (out / "settings.html").read_text(encoding="utf-8"))
        self.assertIn("settings-history.html", (out / "index.html").read_text(encoding="utf-8"))

    def test_every_img_resolves_inside_docs(self):
        out = self.tmp / "o"
        b.build(self.skill, out)
        root = out.resolve()
        for p in out.rglob("*.html"):
            for src in re.findall(r'<img[^>]*\ssrc="([^"]+)"', p.read_text(encoding="utf-8")):
                target = (p.parent / src).resolve()
                self.assertTrue(target.is_file(), "%s -> %s" % (p, src))
                self.assertTrue(root in target.parents, "%s -> %s" % (p, src))


if __name__ == "__main__":
    unittest.main()
