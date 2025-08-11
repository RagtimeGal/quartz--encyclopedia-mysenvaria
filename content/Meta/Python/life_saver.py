import pathlib
import re

# === CONFIG ===
ROOT = pathlib.Path(r"C:\Users\Terra\Documents\Github Folders\quartz--encyclopedia-mysenvaria\content\Encyclopedia Mysenvaria")  # <-- change this
DRY_RUN = False  # True = preview only, False = write changes
# ==============

FM_RE = re.compile(r"^---\r?\n(.*?)(\r?\n)---\r?\n?", re.S)

def parse_front_matter(text: str):
    m = FM_RE.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end():]

def split_tags_block(fm: str):
    """Return (before_lines_incl_tags_key, tag_item_lines, after_lines)."""
    lines = fm.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "tags:":
            before = lines[: i + 1]  # include "tags:"
            j = i + 1
            items = []
            while j < len(lines):
                s = lines[j].lstrip()
                if s.startswith("- ") or s == "":
                    items.append(lines[j])
                    j += 1
                else:
                    break
            after = lines[j:]
            return before, items, after
    return lines, [], []  # no tags block

def process_file(path: pathlib.Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    fm, body = parse_front_matter(text)
    if fm is None:
        return False  # no front matter

    nl = "\r\n" if "\r\n" in text else "\n"
    before, items, after = split_tags_block(fm)
    if not items:
        return False  # no tags

    # Extract all type/ tags
    type_tags = [line for line in items if line.strip().startswith("- type/")]
    other_tags = [line for line in items if not line.strip().startswith("- type/")]

    if not type_tags:
        # No type/ tag → add type/article at top
        type_tags = ["  - type/article"]
    else:
        # If there are multiple type/ tags, keep them all together at the top
        pass

    # Combine so that all type/ tags are first
    new_items = type_tags + other_tags

    if new_items == items:
        return False  # nothing changed

    new_fm = nl.join(before + new_items + after)
    new_text = f"---{nl}{new_fm}{nl}---{nl}{body}"

    if not DRY_RUN:
        path.write_text(new_text, encoding="utf-8")

    return True

def main():
    updated = 0
    total = 0
    for p in ROOT.rglob("*.md"):
        total += 1
        if process_file(p):
            updated += 1
            print(f"[UPDATED] {p}")
    print(f"\nChecked {total} files, updated {updated} files.")
    print("Mode:", "DRY RUN" if DRY_RUN else "WRITE")

if __name__ == "__main__":
    main()
