# status_index_generator.py
import os
import re
import pathlib
from collections import defaultdict
from typing import Optional, Tuple, Iterable

# ===================== CONFIG =====================
# Name of your content folder at repo root
CONTENT_DIRNAME = "content"

# Folders inside content/ to skip entirely (adjust as needed)
EXCLUDE_DIRS = {
    ".git", ".github", ".obsidian", ".quartz", "public", "node_modules", ".vitepress",
    ".docusaurus", "dist", "build"
}

INTRO_TEXT = """\
---
title: "Index of Articles by Status"
enableToc: true
tags:
  - topic/meta
type: index
status: complete
---

> [!abstract] [[Meta/Meta|Meta]]
> *This article is part of a series on the encyclopedia's [[Meta/Writing Guidelines|Writing Guidelines]]* 

The following is a list of all articles from across the Encyclopedia Mysenvaria, sorted by the article's status.
"""

INCLUDE_UNSPECIFIED = True
UNSPECIFIED_LABEL = "Unspecified"
STATUS_ORDER = ["complete", "update", "touchup", "incomplete", "stub", "empty"]
# ==================================================

FM_RE = re.compile(r"^---\r?\n(.*?)(\r?\n)---\r?\n?", re.S)
KV_RE = re.compile(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$")


def find_content_root() -> pathlib.Path:
    """
    Resolve the repo workspace and return <workspace>/content.
    Priority: GITHUB_WORKSPACE -> walk up from this file -> CWD fallback.
    """
    candidates = []
    ws = os.getenv("GITHUB_WORKSPACE")
    if ws:
        candidates.append(pathlib.Path(ws))

    here = pathlib.Path(__file__).resolve()
    candidates.extend(here.parents)
    candidates.append(pathlib.Path.cwd())

    for base in candidates:
        p = base / CONTENT_DIRNAME
        if p.is_dir():
            return p

    # Last-resort fallback to ./content relative to the script
    return here.parent / CONTENT_DIRNAME


ROOT = find_content_root()
OUTPUT = ROOT / "Meta" / "Index of Articles by Status.md"


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


def iter_markdown_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    """
    Yield *.md files under root, skipping EXCLUDE_DIRS and the OUTPUT file itself.
    We manually walk so we can prune excluded directories efficiently.
    """
    out_abs = OUTPUT.resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        # prune excluded dirs
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in filenames:
            if not fname.lower().endswith(".md"):
                continue
            p = pathlib.Path(dirpath) / fname
            try:
                if p.resolve() == out_abs:
                    continue
            except Exception:
                pass
            yield p


def main():
    groups = defaultdict(list)  # status -> list[(display_text, link_target)]

    for md in iter_markdown_files(ROOT):
        text = read_file(md)
        fm, _ = parse_front_matter(text)
        status = title = None
        if fm is not None:
            status = extract_kv(fm, "status")
            title = extract_kv(fm, "title")

        norm_status = (status or "").strip().lower() or (UNSPECIFIED_LABEL if INCLUDE_UNSPECIFIED else None)
        if norm_status is None:
            continue

        target = wiki_target(ROOT, md)
        display = title.strip() if title else md.stem  # <- use title if present, else filename
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
        lines.append("")

    for status_key in final_order:
        items = groups.get(status_key, [])
        if not items:
            continue
        header = status_key if status_key != UNSPECIFIED_LABEL else UNSPECIFIED_LABEL
        lines.append(f"# {header.capitalize() if header != UNSPECIFIED_LABEL else header}")
        for display, target in items:
            # Always write explicit [[path|display]]
            lines.append(f"- [[{target}|{display}]]")
        lines.append("")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    total = sum(len(v) for v in groups.values())
    print(f"Wrote status index with {total} links -> {OUTPUT}")


if __name__ == "__main__":
    main()
