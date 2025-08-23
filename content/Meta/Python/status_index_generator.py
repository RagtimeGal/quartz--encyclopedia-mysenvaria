# build_status_index.py
import re
import pathlib
from collections import defaultdict
from typing import Optional, Tuple

# ===================== CONFIG =====================
ROOT = pathlib.Path(r"C:\Users\Terra\Desktop\Github Folders\quartz--encyclopedia-mysenvaria\content")  # <-- set your vault root
OUTPUT = ROOT / "Meta" / "Index of Articles by Status.md"  # where to write the report

INTRO_TEXT = """\
---
title: Index of Articles by Status
enableToc: true
tags:
  - topic/meta
type: index
---

> [!abstract] [[Meta/Meta|Meta]]
> *This article is part of a series on the encyclopedia's [[Meta/Writing Guidelines|Writing Guidelines]]* 

The following is a list of all articles from across the Encyclopedia Mysenvaria, sorted by the article's status.
"""  # <-- customize this text

INCLUDE_UNSPECIFIED = True
UNSPECIFIED_LABEL = "Unspecified"
# Order to show sections (case-insensitive); anything else appears after, alphabetically
STATUS_ORDER = ["complete", "update", "touchup", "incomplete", "stub", "empty"]
# ==================================================

FM_RE = re.compile(r"^---\r?\n(.*?)(\r?\n)---\r?\n?", re.S)
KV_RE = re.compile(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$")

def parse_front_matter(text: str) -> Tuple[Optional[str], str]:
    m = FM_RE.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end():]

def read_file(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")

def extract_kv(fm: str, key: str) -> Optional[str]:
    """Extract a scalar YAML value on a single line like 'status: complete' or 'title: Foo'."""
    for line in fm.splitlines():
        m = KV_RE.match(line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if k == key:
            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                v = v[1:-1]
            return v
    return None

def wiki_target(root: pathlib.Path, file_path: pathlib.Path) -> str:
    """Return path without extension, POSIX-style for Obsidian wikilinks."""
    rel = file_path.relative_to(root).with_suffix("")
    return rel.as_posix()

def main():
    groups = defaultdict(list)  # status -> list[(display_text, link_target)]

    # Walk all markdown files
    for md in ROOT.rglob("*.md"):
        # Skip the output file itself
        try:
            if OUTPUT.resolve() == md.resolve():
                continue
        except Exception:
            pass

        text = read_file(md)
        fm, _ = parse_front_matter(text)
        status = None
        if fm is not None:
            status = extract_kv(fm, "status")

        norm_status = (status or "").strip().lower() or (UNSPECIFIED_LABEL if INCLUDE_UNSPECIFIED else None)
        if norm_status is None:
            continue

        target = wiki_target(ROOT, md)
        display = md.stem  # always use filename (without .md) as display text
        groups[norm_status].append((display, target))

    # Sort items in each group by display text
    for k in groups:
        groups[k].sort(key=lambda t: t[0].lower())

    # Determine section order
    found = set(groups.keys())
    ordered = [s.lower() for s in STATUS_ORDER if s.lower() in found]
    extras = sorted(found - set(ordered), key=str.lower)
    final_order = ordered + extras

    # Build markdown
    lines = []

    if INTRO_TEXT.strip():
        lines.append(INTRO_TEXT.strip())
        lines.append("")  # blank line after intro

    for status_key in final_order:
        items = groups.get(status_key, [])
        if not items:
            continue
        header = status_key if status_key != UNSPECIFIED_LABEL else UNSPECIFIED_LABEL
        lines.append(f"# {header.capitalize() if header != UNSPECIFIED_LABEL else header}")
        for display, target in items:
            # Always force [[path/filename|filename]]
            lines.append(f"- [[{target}|{display}]]")
        lines.append("")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    total = sum(len(v) for v in groups.values())
    print(f"Wrote status index with {total} links -> {OUTPUT}")

if __name__ == "__main__":
    main()
