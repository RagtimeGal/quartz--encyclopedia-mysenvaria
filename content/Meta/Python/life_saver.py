# repair_front_matter_closing.py
import re, pathlib

ROOT = pathlib.Path(r"C:\Users\Terra\Documents\Github Folders\quartz--encyclopedia-mysenvaria\content\Encyclopedia Mysenvaria")  # <-- change me
DRY_RUN = True  # preview first

FM = re.compile(r"^---\r?\n(.*?)(\r?\n)---\r?\n?", re.S)

def fix(path: pathlib.Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = FM.match(text)
    if not m:
        return False
    fm = m.group(1)
    nl = "\r\n" if "\r\n" in text else "\n"

    lines = fm.splitlines()
    changed = False

    # If a tag line ends with '---', strip it off the line.
    for i, ln in enumerate(lines):
        r = ln.rstrip()
        if r.endswith("---") and r.strip() != "---":
            lines[i] = r[:-3].rstrip()
            changed = True

    # Ensure FM ends with a newline so the closing delimiter lands on its own line
    new_fm = "\n".join(lines)
    if not new_fm.endswith("\n"):
        new_fm += "\n"
        changed = True

    if not changed:
        return False

    new_text = f"---{nl}{new_fm.replace('\n', nl)}---{nl}" + text[m.end():]
    if not DRY_RUN:
        path.write_text(new_text, encoding="utf-8")
    return True

def main():
    touched = 0
    for p in ROOT.rglob("*.md"):
        if fix(p):
            touched += 1
            print("[fixed]", p)
    print("Total fixed:", touched, "| Mode:", "DRY RUN" if DRY_RUN else "WRITE")

if __name__ == "__main__":
    main()
