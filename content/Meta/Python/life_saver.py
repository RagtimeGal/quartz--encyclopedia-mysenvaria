# decade_fixup.py
import re
import pathlib

# === CONFIG ===
ROOT = pathlib.Path(r"C:\Users\Terra\Documents\Github Folders\quartz--encyclopedia-mysenvaria\content\Encyclopedia Mysenvaria\Indexes\History\Decades")  # <-- change this
DRY_RUN = False  # True = preview only, False = write changes
# ==============

# YAML front matter at top
FM_RE = re.compile(r"^---\r?\n(.*?)(\r?\n)---\r?\n?", re.S)

def split_tags_block(fm: str):
    """Return (before_lines_incl_tags, tag_item_lines, after_lines)."""
    lines = fm.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == "tags:":
            before = lines[: i + 1]  # include 'tags:'
            i += 1
            items = []
            while i < len(lines):
                s = lines[i].lstrip()
                if s.startswith("- ") or s == "":
                    items.append(lines[i])
                    i += 1
                else:
                    break
            after = lines[i:]
            return before, items, after
        i += 1
    return fm.splitlines(), [], []  # no tags block

def has_decade_tag(fm: str) -> bool:
    return "topic/history/decade" in fm

# Old Stub callout (consume trailing blank lines)
STUB_BLOCK = re.compile(
    r"> \[!note\] Stub\r?\n"
    r"> This article is a \[\[Meta/Article Types\|stub\]\], meaning it is incomplete\. Help expand it by commenting or create a new \[issue\]\(https://github\.com/RagtimeGal/quartz--encyclopedia-mysenvaria/issues/new/choose\) on the git!"
    r"(?:\r?\n[ \t]*)*",
    re.M,
)

UPDATE_CALLOUT = (
    "> [!note] [[Meta/Meta|Meta]] || [[Meta/Article Types#Update|Update]]\n"
    "> This article is always growing! As the encyclopedia and setting continue to grow, so too does this page! "
    "You can help expand it by commenting or suggesting an edit through "
    "[GitHub issues](https://github.com/RagtimeGal/quartz--encyclopedia-mysenvaria/issues/new/choose)!"
)

def process_file(path: pathlib.Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    nl = "\r\n" if "\r\n" in text else "\n"

    m = FM_RE.match(text)
    if not m:
        return False, "no front matter"

    fm = m.group(1)
    body = text[m.end():]

    # Only touch decade pages
    if not has_decade_tag(fm):
        return False, "not a decade page"

    changed = False

    # 1) Remove Stub callout if present
    body_new, n_stub = STUB_BLOCK.subn("", body)
    if n_stub:
        body = body_new
        changed = True

    # 2) Ensure tags include 'has/infobox'
    before, items, after = split_tags_block(fm)
    if items:
        has_has_infobox = any(
            ln.strip().startswith("- has/infobox")
            for ln in items
            if ln.strip().startswith("- ")
        )
        if not has_has_infobox:
            items.append("  - has/infobox")
            changed = True

        # Normalize indentation to two spaces for list items; collapse extra blanks
        norm = []
        for ln in items:
            s = ln.strip()
            if s.startswith("- "):
                norm.append("  " + s)
            elif s == "":
                if not (norm and norm[-1] == ""):
                    norm.append("")
            else:
                norm.append(ln)
        fm = "\n".join(before + norm + after)
    # If no tags block, we leave FM untouched (decade pages should have it anyway)

    # 3) Append Update callout at end with exactly one blank line before it
    body_stripped = body.rstrip("\r\n \t")
    if not body_stripped.endswith(UPDATE_CALLOUT):
        body = body_stripped + nl + nl + UPDATE_CALLOUT + nl
        changed = True
    else:
        if not body.endswith(nl):
            body = body + nl

    if not changed:
        return False, "no changes"

    # ✅ Ensure FM ends with a newline before writing the closing '---'
    if not fm.endswith("\n"):
        fm += "\n"

    # Respect original newline style in FM
    fm_nl = fm.replace("\n", nl)
    new_text = f"---{nl}{fm_nl}---{nl}{body}"

    if not DRY_RUN:
        path.write_text(new_text, encoding="utf-8")
    return True, "updated"

def main():
    examined = updated = 0
    for md in ROOT.rglob("*.md"):
        examined += 1
        did, _ = process_file(md)
        if did:
            updated += 1
            print(f"[UPDATED] {md}")
    print(f"\nExamined: {examined}")
    print(f"Updated:  {updated}")
    print("Mode:", "DRY RUN" if DRY_RUN else "WRITE")

if __name__ == "__main__":
    main()
