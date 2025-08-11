# fix_tag_period_to_slash.py
import re
import pathlib

# === CONFIG ===
ROOT = pathlib.Path(r"C:\Users\Terra\Documents\Github Folders\quartz--encyclopedia-mysenvaria\content\Encyclopedia Mysenvaria")  # <-- change this
DRY_RUN = False  # True = preview; False = write changes
# Optionally limit which tags get touched by prefix (None = touch any tag with a '.')
LIMIT_PREFIXES = {"type", "topic", "subject", "status", "future", "needs", "has"}  # or set to None
# ==============

FM_RE = re.compile(r"^---\r?\n(.*?)(\r?\n)---\r?\n?", re.S)

def parse_front_matter(text: str):
    m = FM_RE.match(text)
    if not m:
        return None, text, -1, -1
    return m.group(1), text[m.end():], m.start(), m.end()

def split_tags_block(fm: str):
    """Return (before_lines_incl_tags_key, tag_item_lines, after_lines)."""
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
    return lines, [], []  # no tags block

def convert_tag(tag: str) -> str:
    """
    Replace the FIRST '.' in the tag with '/'.
    Only do it if LIMIT_PREFIXES is None or the tag starts with one of those prefixes + '.'.
    """
    if "." not in tag:
        return tag
    if LIMIT_PREFIXES:
        for p in LIMIT_PREFIXES:
            if tag.startswith(p + "."):
                break
        else:
            return tag  # prefix not in allowlist
    idx = tag.find(".")
    return tag[:idx] + "/" + tag[idx + 1:]

def process_file(path: pathlib.Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    fm, body, start, end = parse_front_matter(text)
    if fm is None:
        return False, 0

    # Preserve original newline style
    nl = "\r\n" if "\r\n" in text else "\n"

    before, items, after = split_tags_block(fm)
    if not items:
        return False, 0

    changed = False
    count = 0
    new_items = []

    for ln in items:
        s = ln.strip()
        if not s.startswith("- "):  # blank line or non-item inside block
            new_items.append(ln)
            continue

        raw = s[2:].strip()  # tag value
        # handle optional quotes safely
        quote = ""
        val = raw
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            quote, val = val[0], val[1:-1]

        new_val = convert_tag(val)
        new_raw = f"{quote}{new_val}{quote}" if quote else new_val
        new_line = f"  - {new_raw}"

        if new_line != ln:
            changed = True
            if new_val != val:
                count += 1

        new_items.append(new_line)

    if not changed:
        return False, 0

    new_fm = "\n".join(before + new_items + ([""] if after and after[0] != "" else []) + after)
    if not new_fm.endswith("\n"):
        new_fm += "\n"  # ensure closing --- goes on its own line

    # ✅ Fixed backslash issue — precompute replacement
    fm_with_correct_nl = new_fm.replace("\n", nl)
    new_text = f"---{nl}{fm_with_correct_nl}---{nl}{body}"

    if not DRY_RUN:
        path.write_text(new_text, encoding="utf-8")
    return True, count

def main():
    examined = files = tags = 0
    for p in ROOT.rglob("*.md"):
        examined += 1
        did, n = process_file(p)
        if did:
            files += 1
            tags += n
            print(f"[UPDATED] {p} (+{n})")
    print("\nExamined:", examined)
    print("Files changed:", files)
    print("Tags converted:", tags)
    print("Mode:", "DRY RUN" if DRY_RUN else "WRITE")

if __name__ == "__main__":
    main()
