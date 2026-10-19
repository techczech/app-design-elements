#!/usr/bin/env python3
"""Build the static public site for the app design elements skill.

Run from the skill folder:  python3 site/build_site.py
Standard library only. Output goes to docs/ and is deterministic.
Never reads references/local.md.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
REPO_URL = "https://github.com/techczech/app-design-elements"
MOCKUP_REL = "design/2026-10-19-settings-locked/settings-window-locked-mockup.html"

FORBIDDEN_FILE = SKILL / "site" / "forbidden.txt"


def load_forbidden(path=None):
    """Forbidden strings, one per line, '#' comments allowed. None if the file is absent."""
    path = Path(path) if path else FORBIDDEN_FILE
    if not path.is_file():
        return None
    out = []
    for line in path.read_text(encoding="utf-8").split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out

# Element number -> section headings to show from its reference file.
# None means the whole file.
SECTION_MAP = {
    1: ["Registry"], 2: ["Palette"], 3: ["Reserved chords"], 4: None,
    5: ["Reserved chords"], 6: ["macOS menu bar"], 7: ["Reserved chords"],
    8: ["Reserved chords"], 9: ["Reserved chords"],
    12: ["Onboarding is temporary"], 13: ["Help after onboarding"],
    14: ["Layout", "Controls", "Design rounds"], 15: ["States and errors"],
    16: ["Wording"],
}

PICTURE_APPS = {
    1: "WriteFlex", 2: "WriteFlex", 3: "TalkWeaver", 4: "WriteFlex",
    5: "TalkWeaver", 6: "SlideWell", 7: "WriteFlex", 8: "Highlight Scout",
    9: "Highlight Scout", 10: "Dev Traffic Control", 11: "Dev Traffic Control",
    12: "TalkWeaver", 13: "WriteFlex", 14: "SlideWell", 15: "Dev Traffic Control",
    16: "Highlight Scout",
}
PICTURE_WHAT = {
    1: "the palette listing commands that come from one registry",
    2: "the command palette open, each command showing its chord",
    3: "the cheat sheet with the reserved chords visible",
    4: "the shortcut rebinding row for one command",
    5: "the cheat sheet open while typing in the editor",
    6: "the menu bar with a menu open, showing effective chords",
    7: "the contextual actions list on a selection",
    8: "the switcher or inspector open",
    9: "find in document and search everything side by side",
    10: "the Settings window with the inspector showing a setting",
    11: "the settings changelog with an entry changed by an agent",
    12: "the Get started button and the example project",
    13: "the Help menu and a contextual help surface",
    14: "a main window with bounded sections and the 70/30 layout",
    15: "an empty state and an error state with a recovery action",
    16: "a screen where command and button names are plain sentences",
}


class BuildError(Exception):
    pass


# ---------------------------------------------------------------- markdown

def inline(text):
    codes = []

    def stash(m):
        codes.append("<code>%s</code>" % html.escape(m.group(1)))
        return "\x00%d\x00" % (len(codes) - 1)

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                  lambda m: '<a href="%s">%s</a>' % (html.escape(m.group(2)), m.group(1)), text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def md_to_html(md, demote=0):
    lines = md.split("\n")
    out = []
    i = 0
    para = []

    def flush():
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para)))
            para.clear()

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(buf)))
            i += 1
            continue
        m = re.match(r"^!\[([^\]]*)\]\(([^)\s]+)\)\s*$", line)
        if m:
            flush()
            out.append('<figure><img src="%s" alt="%s"><figcaption>%s</figcaption></figure>' % (
                html.escape(m.group(2)), html.escape(m.group(1)), inline(m.group(1))))
            i += 1
            continue
        m = re.match(r"(#{1,6})\s+(.*)", line)
        if m:
            flush()
            lvl = min(6, len(m.group(1)) + demote)
            out.append("<h%d>%s</h%d>" % (lvl, inline(m.group(2)), lvl))
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1]):
            flush()
            head = split_row(line)
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            t = ["<table>", "<thead><tr>%s</tr></thead>" %
                 "".join("<th>%s</th>" % inline(c) for c in head), "<tbody>"]
            for r in rows:
                t.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r))
            t.append("</tbody></table>")
            out.append("".join(t))
            continue
        m = re.match(r"^([-*])\s+(.*)", line)
        m2 = re.match(r"^\d+\.\s+(.*)", line)
        if m or m2:
            flush()
            ordered = bool(m2)
            items = []
            while i < len(lines):
                a = re.match(r"^[-*]\s+(.*)", lines[i])
                b = re.match(r"^\d+\.\s+(.*)", lines[i])
                mm = b if ordered else a
                if mm:
                    items.append([mm.group(1)])
                    i += 1
                elif lines[i].startswith("  ") and lines[i].strip() and items:
                    items[-1].append(lines[i].strip())
                    i += 1
                else:
                    break
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join(
                "<li>%s</li>" % inline(" ".join(it)) for it in items), tag))
            continue
        if not line.strip():
            flush()
            i += 1
            continue
        para.append(line.strip())
        i += 1
    flush()
    return "\n".join(out)


def strip_frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text


def sections(md):
    """Return (preamble_without_h1, {heading: body_markdown}) split on '## '."""
    parts = re.split(r"(?m)^## (.*)$", md)
    pre = re.sub(r"(?m)^# .*$", "", parts[0]).strip()
    secs = {}
    for k in range(1, len(parts), 2):
        secs[parts[k].strip()] = parts[k + 1].strip()
    return pre, secs


def drop_h1(md):
    return re.sub(r"(?m)^# .*\n?", "", md, count=1).strip()


# ---------------------------------------------------------------- parsing

def parse_elements(skill_md):
    m = re.search(r"(?ms)^## The elements\s*\n(.*?)(?=^## |\Z)", skill_md)
    if not m:
        raise BuildError("SKILL.md has no '## The elements' section")
    rows = []
    last_ref = None
    for line in m.group(1).split("\n"):
        if not line.startswith("|"):
            continue
        cells = split_row(line)
        if len(cells) < 4 or not cells[0].isdigit():
            continue
        num = int(cells[0])
        ref = cells[3].strip("`").strip()
        if ref.lower() == "same" and last_ref:
            ref = last_ref
        last_ref = ref
        rows.append({"num": num, "ref": ref})
    return rows


def parse_names(text):
    """Parse element-names.md into [{num, plain, rule, slug}]; exactly 16 rows, 1-16 in order."""
    out = []
    for line in text.split("\n"):
        if not line.startswith("|"):
            continue
        cells = split_row(line)
        if len(cells) != 3 or not cells[0].isdigit():
            continue
        name = " ".join(cells[1].split())
        slug = "-".join(re.findall(r"[a-z0-9]+", re.sub("[⌘⇧⌥⌃]+\\S*", "", name).lower()))
        if cells[0] == "10":
            slug = "settings"
        out.append({"num": int(cells[0]), "plain": name, "rule": cells[2], "slug": slug})
    nums = [r["num"] for r in out]
    if nums != list(range(1, 17)):
        raise BuildError("element-names.md must have exactly 16 rows numbered 1-16 in order; found %s" % nums)
    slugs = [r["slug"] for r in out]
    if len(set(slugs)) != 16 or "" in slugs:
        raise BuildError("element-names.md names give empty or duplicate slugs")
    return out


def sanitise_skill(md):
    """Remove mentions of the private reference file from the public rendering."""
    md = "\n".join(l for l in md.split("\n") if "references/local.md" not in l or l.startswith("- "))
    md = re.sub(r";? see `references/local\.md`[^.]*\.", ".", md)
    md = re.sub(r"\n\n\n+", "\n\n", md)
    return md


# ---------------------------------------------------------------- templates

def href(row, depth):
    pre = "../" * depth
    if row["slug"] == "settings":
        return pre + "settings.html"
    return "%selements/%s.html" % (pre, row["slug"])


def page(title, body, rows, depth, current, wide=False):
    pre = "../" * depth
    nav = ['<a href="%sindex.html"%s>Home</a>' % (pre, ' aria-current="page"' if current == "home" else "")]
    nav.append('<div class="nav-h">Elements</div>')
    for r in rows:
        cur = ' aria-current="page"' if current == r["slug"] else ""
        nav.append('<a href="%s"%s><span class="n">%d</span> %s</a>' % (
            href(r, depth), cur, r["num"], html.escape(r["plain"])))
        if r["slug"] == "settings":
            cur = ' aria-current="page"' if current == "settings-history" else ""
            nav.append('<a class="sub" href="%ssettings-history.html"%s>Settings history</a>' % (pre, cur))
    nav.append('<div class="nav-h">More</div>')
    for key, label, target in [("use", "Use with your agent", "use-with-your-agent.html"),
                               ("skill", "Read the skill", "skill.html")]:
        cur = ' aria-current="page"' if current == key else ""
        nav.append('<a href="%s%s"%s>%s</a>' % (pre, target, cur, label))
    return """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s - App design elements</title>
<link rel="stylesheet" href="%sstyle.css">
</head>
<body>
<nav class="side" aria-label="Site">
<div class="brand">App design elements</div>
%s
</nav>
<main class="%s">
%s
</main>
</body>
</html>
""" % (html.escape(title), pre, "\n".join(nav), "wide" if wide else "", body)


CSS = """\
:root { --ink:#1d2328; --muted:#5b6670; --line:#d9dee3; --bg:#ffffff; --side:#f5f7f9; --accent:#1a5fb4; --code:#eef1f4; }
* { box-sizing:border-box; }
html { font-size:16px; }
body { margin:0; display:flex; min-height:100vh; color:var(--ink); background:var(--bg);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif; line-height:1.6; }
nav.side { width:260px; flex:none; background:var(--side); border-right:1px solid var(--line);
  padding:20px 14px; position:sticky; top:0; align-self:flex-start; height:100vh; overflow-y:auto; font-size:.9rem; }
nav.side .brand { font-weight:600; margin:0 8px 14px; }
nav.side .nav-h { margin:16px 8px 4px; font-size:.75rem; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); }
nav.side a { display:block; padding:4px 8px; border-radius:5px; color:var(--ink); text-decoration:none; }
nav.side a:hover { background:#e6ebef; }
nav.side a[aria-current="page"] { background:#dce6f3; font-weight:600; }
nav.side a.sub { padding-left:2.4em; }
nav.side .n { display:inline-block; width:1.4em; color:var(--muted); }
main { flex:1; min-width:0; max-width:calc(70ch + 96px); padding:32px 48px 64px; }
main.wide { max-width:none; }
h1 { font-size:1.7rem; line-height:1.25; margin:0 0 .6em; }
h2 { font-size:1.25rem; margin:1.8em 0 .5em; }
h3 { font-size:1.05rem; margin:1.4em 0 .4em; }
p, ul, ol { margin:.7em 0; }
li { margin:.25em 0; }
a { color:var(--accent); }
code { background:var(--code); padding:.1em .35em; border-radius:4px; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.88em; }
pre { background:var(--code); padding:12px 14px; border-radius:6px; overflow-x:auto; }
pre code { background:none; padding:0; }
table { border-collapse:collapse; width:100%; margin:1em 0; font-size:.93rem; }
th, td { text-align:left; vertical-align:top; padding:8px 10px; border-bottom:1px solid var(--line); }
th { background:var(--side); border-bottom:2px solid var(--line); font-weight:600; }
td:first-child, th:first-child { white-space:nowrap; }
.rule { font-size:1.08rem; padding:10px 14px; border-left:3px solid var(--accent); background:var(--side); margin:0 0 1.2em; }
figure { margin:1.4em 0; }
figure img { max-width:100%; border:1px solid var(--line); border-radius:6px; }
figcaption { color:var(--muted); font-size:.9rem; margin-top:6px; }
.placeholder { border:1px dashed var(--line); padding:12px; color:var(--muted); }
iframe.mockup { width:100%; height:1040px; border:1px solid var(--line); border-radius:6px; background:#fff; }
h2.detail { font-size:.8rem; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); margin:2em 0 .3em; }
.note { color:var(--muted); font-size:.92rem; }
"""


# ---------------------------------------------------------------- build

def read_content(skill, name, title):
    p = skill / "site" / "content" / name
    if p.is_file():
        return md_to_html(strip_frontmatter(p.read_text(encoding="utf-8")))
    return ('<h1>%s</h1><p class="placeholder">Content for this page has not been written yet '
            '(site/content/%s).</p>' % (html.escape(title), name))


def element_body(row, rows, refs, skill_dir_pictures, captions):
    ref_path = row["ref"]
    parts = ["<h1>%d. %s</h1>" % (row["num"], inline(row["plain"])),
             '<p class="rule">%s</p>' % inline(row["rule"])]
    pic = skill_dir_pictures / ("%s.png" % row["slug"])
    if pic.is_file():
        cap = captions.get(row["slug"], "")
        parts.append('<figure><img src="%s" alt="%s">%s</figure>' % (
            ("../pictures/%s.png" % row["slug"]), html.escape(cap or row["plain"]),
            "<figcaption>%s</figcaption>" % html.escape(cap) if cap else ""))
    parts.append('<h2 class="detail">The rule in detail</h2>')
    md = refs[ref_path]
    want = SECTION_MAP.get(row["num"])
    pre, secs = sections(md)
    if want is None:
        body = drop_h1(md)
        parts.append(md_to_html(body, demote=0))
    else:
        chunks = []
        for h in want:
            key = next((k for k in secs if k == h or k.startswith(h + " ")), None)
            if key is None:
                raise BuildError("section %r missing from %s" % (h, ref_path))
            chunks.append("## %s\n\n%s" % (key, secs[key]))
        parts.append(md_to_html("\n\n".join(chunks)))
    sib = [r for r in rows if r["ref"] == ref_path and r["num"] != row["num"] and r["slug"] != "settings"]
    if sib:
        parts.append('<p class="note">Related elements from the same reference: %s.</p>' % ", ".join(
            '<a href="%s.html">%s</a>' % (r["slug"], html.escape(r["plain"])) for r in sib))
    return "\n".join(parts)


def check_forbidden(files, forbidden=None):
    """files: {relative_name: text}. Raise BuildError on any forbidden string (case-insensitive)."""
    problems = []
    for name in sorted(files):
        low = files[name].lower()
        for s in forbidden:
            if s.lower() in low:
                problems.append("%s contains %r" % (name, s))
    if problems:
        raise BuildError("Forbidden strings in generated site:\n  " + "\n  ".join(problems))


def build(skill=SKILL, out=None):
    skill = Path(skill)
    out = Path(out) if out else skill / "docs"
    skill_md = (skill / "SKILL.md").read_text(encoding="utf-8")
    rows = parse_elements(skill_md)
    if len(rows) != 16:
        raise BuildError("expected 16 elements, found %d" % len(rows))
    names_path = skill / "site" / "content" / "element-names.md"
    if not names_path.is_file():
        raise BuildError("site/content/element-names.md is missing")
    names = parse_names(strip_frontmatter(names_path.read_text(encoding="utf-8")))
    for r, n in zip(rows, names):
        r.update(n)
    refs = {}
    for r in rows:
        if r["ref"] not in refs:
            if r["ref"].endswith("local.md"):
                raise BuildError("an element points at the private reference file")
            refs[r["ref"]] = strip_frontmatter(
                (skill / r["ref"]).read_text(encoding="utf-8"))
    pic_dir = skill / "site" / "pictures"
    cap_file = pic_dir / "captions.json"
    captions = json.loads(cap_file.read_text(encoding="utf-8")) if cap_file.is_file() else {}

    files = {}   # relative path -> text
    binaries = {}  # relative path -> source Path

    files["style.css"] = CSS
    files[".nojekyll"] = ""

    # home
    home = read_content(skill, "home.md", "Home")
    table = ['<h2>The 16 elements</h2>', '<table><thead><tr><th>#</th><th>Name</th><th>What it means for you</th></tr></thead><tbody>']
    for r in rows:
        table.append('<tr><td>%d</td><td><a href="%s">%s</a></td><td>%s</td></tr>' % (
            r["num"], href(r, 0), inline(r["plain"]), inline(r["rule"])))
    table.append("</tbody></table>")
    patterns = ['<h2>Design patterns</h2>',
                '<p><a href="settings-history.html">Settings history</a>: a record of every change to a setting, with reset and undo.</p>']
    files["index.html"] = page("Home", home + "\n" + "\n".join(table) + "\n" + "\n".join(patterns), rows, 0, "home")

    mockup_src = skill / MOCKUP_REL
    for r in rows:
        body = element_body(r, rows, refs, pic_dir, captions)
        pic = pic_dir / ("%s.png" % r["slug"])
        if pic.is_file():
            binaries["pictures/%s.png" % r["slug"]] = pic
        if r["slug"] == "settings":
            body = body.replace("../pictures/", "pictures/")
            body = body.replace("</p>", '</p>\n<p>How the history of changes works: '
                                '<a href="settings-history.html">Settings history</a></p>', 1)
            body += ('\n<h2>Locked mockup</h2>\n<p class="note">The interactive mockup of the locked Settings window. '
                     '<a href="settings-mockup.html">Open it on its own</a>.</p>\n'
                     '<iframe class="mockup" src="settings-mockup.html" title="Settings window mockup"></iframe>')
            files["settings.html"] = page("Settings", body, rows, 0, "settings", wide=True)
        else:
            files["elements/%s.html" % r["slug"]] = page(
                r["plain"], body, rows, 1, r["slug"])
    files["settings-mockup.html"] = mockup_src.read_text(encoding="utf-8")

    hist_md = strip_frontmatter((skill / "site" / "content" / "settings-history.md").read_text(encoding="utf-8")) \
        if (skill / "site" / "content" / "settings-history.md").is_file() else None
    if hist_md is not None:
        shots = skill / "design" / "2026-10-19-settings-locked" / "screenshots"

        def repoint(m):
            name = Path(m.group(2)).name
            src = shots / name
            if not src.is_file():
                raise BuildError("settings-history.md image missing: %s" % name)
            binaries["images/%s" % name] = src
            return "![%s](images/%s)" % (m.group(1), name)

        hist_md = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", repoint, hist_md)
        files["settings-history.html"] = page("Settings history", md_to_html(hist_md), rows, 0, "settings-history")

    files["use-with-your-agent.html"] = page(
        "Use with your agent", read_content(skill, "use-with-your-agent.md", "Use with your agent"),
        rows, 0, "use")

    skill_html = md_to_html(sanitise_skill(strip_frontmatter(skill_md)))
    skill_html = ('<p class="note">Source and issues: <a href="%s">%s</a></p>\n' % (REPO_URL, REPO_URL)) + skill_html
    files["skill.html"] = page("Read the skill", skill_html, rows, 0, "skill")

    forb = load_forbidden(skill / "site" / "forbidden.txt")
    if forb is None:
        print("site/forbidden.txt not found: skipping the forbidden-string check")
    else:
        check_forbidden({k: v for k, v in files.items() if k != ".nojekyll"}, forb)

    if out.exists():
        shutil.rmtree(out)
    for rel in sorted(files):
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(files[rel], encoding="utf-8", newline="\n")
    for rel in sorted(binaries):
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(binaries[rel], p)

    needed = ["# Pictures needed", "",
              "Save each as `site/pictures/<slug>.png` and add a caption for it in `site/pictures/captions.json` (slug to caption text).", ""]
    for r in rows:
        needed.append("- `%s` (%d. %s): %s, from %s." % (
            r["slug"], r["num"], r["plain"], PICTURE_WHAT[r["num"]], PICTURE_APPS[r["num"]]))
    (skill / "site" / "pictures" / "NEEDED.md").write_text("\n".join(needed) + "\n", encoding="utf-8")
    return sorted(files)


def main():
    try:
        written = build()
    except BuildError as e:
        print("BUILD FAILED: %s" % e, file=sys.stderr)
        return 1
    print("Built %d files into %s" % (len(written), SKILL / "docs"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
