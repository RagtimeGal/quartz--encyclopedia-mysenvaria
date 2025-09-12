import re
import pathlib
from typing import Any, Dict, List, Optional, Tuple

# ===================== CONFIG =====================
ROOT = pathlib.Path(r"C:\Users\Terra\Documents\Github Folders\quartz--encyclopedia-mysenvaria\content")
DRY_RUN = False           # preview only; set False to write
OVERWRITE_PROPS = False  # overwrite existing props if present?
CREATE_FRONT_MATTER_IF_MISSING = False
CASE_INSENSITIVE = False
# =================== /CONFIG ======================

# Your rules (unchanged)
RULES = [
    {"name": "Add types: article",     "when": {"tag_equals": ["type/article"]},      "add": {"type": "article"}},
    {"name": "Add types: index",       "when": {"tag_equals": ["type/index"]},        "add": {"type": "index"}},
    {"name": "Add types: table",       "when": {"tag_equals": ["type/table"]},        "add": {"type": "table"}},
    {"name": "Add types: overview",    "when": {"tag_equals": ["type/overview"]},     "add": {"type": "overview"}},
    {"name": "Add types: template",    "when": {"tag_equals": ["type/template"]},     "add": {"type": "template"}},
    {"name": "Add types: ledger",      "when": {"tag_equals": ["type/ledger"]},       "add": {"type": "ledger"}},
    {"name": "Add status: empty",      "when": {"tag_equals": ["status/empty"]},      "add": {"status": "empty"}},
    {"name": "Add status: stub",       "when": {"tag_equals": ["status/stub"]},       "add": {"status": "stub"}},
    {"name": "Add status: incomplete", "when": {"tag_equals": ["status/incomplete"]}, "add": {"status": "incomplete"}},
    {"name": "Add status: update",     "when": {"tag_equals": ["status/update"]},     "add": {"status": "update"}},
    {"name": "Add status: touchup",    "when": {"tag_equals": ["status/touchup"]},    "add": {"status": "touchup"}},
    {"name": "Add status: complete",   "when": {"tag_equals": ["status/complete"]},   "add": {"status": "complete"}},
]

# --- Internals ---
FM_RE = re.compile(r"^---\r?\n(.*?)(\r?\n)---\r?\n?", re.S)

def _norm(s: str) -> str:
    return s.lower() if CASE_INSENSITIVE else s

def parse_front_matter(text: str) -> Tuple[Optional[str], str, Optional[re.Match]]:
    m = FM_RE.match(text)
    if not m:
        return None, text, None
    return m.group(1), text[m.end():], m

def split_tags_block(fm: str) -> Tuple[List[str], List[str], List[str]]:
    lines = fm.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == "tags:":
            before = lines[: i + 1]
            i += 1
            items: List[str] = []
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
    return fm.splitlines(), [], []

def extract_tags(tag_lines: List[str]) -> List[str]:
    tags = []
    for ln in tag_lines:
        s = ln.strip()
        if s.startswith("- "):
            raw = s[2:].strip()
            if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
                raw = raw[1:-1]
            tags.append(raw)
    return tags

def match_rule(tags: List[str], rule: Dict) -> bool:
    cond = rule.get("when", {})
    eqs = cond.get("tag_equals", [])
    starts = cond.get("tag_startswith", [])
    regs = cond.get("tag_regex", [])
    tags_norm = [_norm(t) for t in tags]

    for want in eqs:
        wantn = _norm(want)
        if any(t == wantn for t in tags_norm):
            return True
    for pref in starts:
        prefn = _norm(pref)
        if any(t.startswith(prefn) for t in tags_norm):
            return True
    for pat in regs:
        r = re.compile(pat, re.I if CASE_INSENSITIVE else 0)
        if any(r.search(t) for t in tags):
            return True
    return False

def serialize_yaml_value(val: Any, indent: int = 0) -> str:
    ind = " " * indent
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        return str(val)
    if isinstance(val, (list, tuple)):
        lines = [f"{ind}- {serialize_yaml_value(item, 0)}" for item in val]
        return ("\n" + "\n".join(lines))
    s = str(val)
    needs_quotes = (":" in s) or s != s.strip() or s == "" or s.startswith("#")
    if needs_quotes:
        s = s.replace('"', '\\"')
        return f"\"{s}\""
    return s

def parse_kv_lines(fm: str) -> List[str]:
    return fm.splitlines()

def find_prop_line_indexes(lines: List[str], key: str) -> List[int]:
    key_re = re.compile(rf"^{re.escape(key)}\s*:")
    return [i for i, ln in enumerate(lines) if key_re.match(ln)]

def upsert_properties(fm: str, props: Dict[str, Any], overwrite: bool) -> Tuple[str, bool]:
    lines = parse_kv_lines(fm)
    changed = False
    for key, value in props.items():
        idxs = find_prop_line_indexes(lines, key)
        val_str = serialize_yaml_value(value)
        if isinstance(value, (list, tuple)):
            if idxs and not overwrite:
                continue
            if idxs:
                i = idxs[0]
                del lines[i]
                while i < len(lines) and (lines[i].startswith("  - ") or lines[i].strip() == ""):
                    del lines[i]
            lines.append(f"{key}:{val_str}")
            changed = True
        else:
            if idxs:
                if overwrite:
                    lines[idxs[0]] = f"{key}: {val_str}"
                    changed = True
            else:
                lines.append(f"{key}: {val_str}")
                changed = True
    return "\n".join(lines), changed

def ensure_trailing_newline(s: str) -> str:
    return s if s.endswith("\n") else s + "\n"

def process_file(path: pathlib.Path) -> Tuple[bool, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    nl = "\r\n" if "\r\n" in text else "\n"

    fm, body, m = parse_front_matter(text)
    if fm is None:
        if not CREATE_FRONT_MATTER_IF_MISSING:
            return (False, "no front matter")
        fm = ""
        body = text

    before, tag_lines, after = split_tags_block(fm)
    tags = extract_tags(tag_lines)
    if not tags:
        return (False, "no tags")

    applicable: List[Dict[str, Any]] = [r for r in RULES if match_rule(tags, r)]
    if not applicable:
        return (False, "no matching rules")

    # Merge all props from matching rules
    props_to_add: Dict[str, Any] = {}
    for rule in applicable:
        for k, v in rule.get("add", {}).items():
            if k not in props_to_add or OVERWRITE_PROPS:
                props_to_add[k] = v

    if not props_to_add:
        return (False, "nothing to add")

    new_fm, fm_changed = upsert_properties(fm, props_to_add, OVERWRITE_PROPS)
    if not fm_changed:
        return (False, "props already present")

    new_fm = ensure_trailing_newline(new_fm)
    new_fm_normalized = new_fm.replace("\n", nl)
    new_text = f"---{nl}{new_fm_normalized}---{nl}{body}"

    if not DRY_RUN:
        path.write_text(new_text, encoding="utf-8")
    return (True, f"added: {', '.join(props_to_add.keys())}")

def main():
    checked = updated = 0
    for md in ROOT.rglob("*.md"):
        checked += 1
        did, msg = process_file(md)
        if did:
            updated += 1
            print(f"[UPDATED] {md} :: {msg}")
        # else:
        #     print(f"[SKIP]   {md} :: {msg}")
    print(f"\nChecked: {checked}")
    print(f"Updated: {updated}")
    print("Mode:    {'DRY RUN' if DRY_RUN else 'WRITE'}")

if __name__ == "__main__":
    main()
