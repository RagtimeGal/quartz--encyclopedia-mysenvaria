# decade_article_generator.py
# Rebuilds extracted_data.json, then generates ALL decade pages from -180 to +1499.
import os
import re
import json
import pathlib
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Optional

# ===================== CONFIG =====================
CONTENT_DIRNAME = "content"

# Extraction outputs
DERIVED_DIR_REL = pathlib.Path("Meta/Programs/debug/decade_article_generator")
EXTRACTED_JSON = "extracted_data.json"
WARNINGS_MD  = "extraction_warnings.md"

# Where to write decades (final location)
DECADES_DIR_REL   = pathlib.Path("Encyclopedia Mysenvaria/Indexes/History/Decades")
CENTURIES_DIR_REL = pathlib.Path("Encyclopedia Mysenvaria/Indexes/History/Centuries")

# Year bounds (inclusive)
START_YEAR = -180   # 180 BT
END_YEAR   = 1499   # 1499 AT (will produce up to the 1490s AT page)

# Decade template (if None, uses the built-in default below)
DECADE_TEMPLATE_PATH: Optional[pathlib.Path] = None

# Write mode
DRY_RUN = False

# Skip scanning these dirs during extraction
EXCLUDE_DIRS = {
    ".git", ".github", ".obsidian", ".quartz", "public",
    "node_modules", ".vitepress", ".docusaurus", "dist", "build"
}
# ==================================================

# Optional explicit override (great for CI)
# Set DECADE_GEN_CONTENT_ROOT to an absolute path ending with .../content
ENV_CONTENT_ROOT = os.getenv("DECADE_GEN_CONTENT_ROOT")

def find_content_root() -> pathlib.Path:
    if ENV_CONTENT_ROOT:
        p = pathlib.Path(ENV_CONTENT_ROOT)
        print(f"[ROOT] Using ENV DECADE_GEN_CONTENT_ROOT = {p}")
        return p

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
            print(f"[ROOT] Using discovered content root: {p}")
            return p

    fallback = here.parent / CONTENT_DIRNAME
    print(f"[ROOT] Fallback content root: {fallback}")
    return fallback

# ----------------- Extraction -----------------
FM_RE   = re.compile(r"^---\r?\n(.*?)(?:\r?\n)---\r?\n?", re.S)
DATE_RE = re.compile(r"^\s*([+-]?\d+)(?:-([0-9]{1,3}))?\s*$")

def try_load_yaml(text: str) -> Optional[Dict[str, Any]]:
    try:
        import yaml  # type: ignore
    except Exception:
        return None
    try:
        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else None
    except Exception:
        return None

def fallback_parse_yaml(text: str) -> Optional[Dict[str, Any]]:
    # Minimal tolerant fallback (enough for your FM blocks)
    lines = text.splitlines()
    norm = [re.sub(r"^\t+", lambda m: "  " * len(m.group(0)), ln) for ln in lines]
    i = 0
    def cast_scalar(s: str) -> Any:
        s = s.strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")): s = s[1:-1]
        if s.lower() == "true": return True
        if s.lower() == "false": return False
        try:
            if "." in s: return float(s)
            return int(s)
        except Exception:
            return s
    def parse_block(indent: int) -> Any:
        nonlocal i
        mode=None; obj={}; arr=[]
        while i < len(norm):
            line = norm[i]
            if not line.strip(): i+=1; continue
            cur_indent = len(line) - len(line.lstrip(" "))
            if cur_indent < indent: break
            if cur_indent > indent:
                if mode=="list" and arr: arr[-1]=parse_block(cur_indent); continue
                if mode=="dict" and obj: obj[list(obj)[-1]]=parse_block(cur_indent); continue
                break
            ln = line[indent:]
            if ln.startswith("- "):
                mode = "list" if mode in (None,"list") else mode
                val = ln[2:].strip()
                arr.append({} if val=="" else cast_scalar(val))
                i+=1
            else:
                if ":" in ln:
                    mode = "dict" if mode in (None,"dict") else mode
                    k,v = ln.split(":",1); key=k.strip(); val=v.strip()
                    obj[key] = {} if val=="" else cast_scalar(val)
                    i+=1
                else:
                    break
        return arr if mode=="list" else obj
    root={}
    while i < len(norm):
        line = norm[i]
        if not line.strip(): i+=1; continue
        if ":" in line:
            k,v = line.split(":",1); key=k.strip(); val=v.strip()
            i+=1
            root[key] = parse_block(len(line)-len(line.lstrip(" "))+2) if val=="" else cast_scalar(val)
        else:
            i+=1
    return root

def read_front_matter(md_path: pathlib.Path) -> Tuple[Optional[Dict[str, Any]], str, str]:
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    m = FM_RE.match(text)
    body = text[m.end():] if m else text
    fm_raw = m.group(1) if m else ""
    data = try_load_yaml(fm_raw)
    used = "pyyaml" if data is not None else "fallback"
    if data is None and fm_raw:
        data = fallback_parse_yaml(fm_raw)
    return (data if isinstance(data, dict) else None), body, used

def parse_mysenvar_date(s: Any) -> Optional[Dict[str, int]]:
    if isinstance(s, int):
        return {"year": s, "day": 0}
    if not isinstance(s, str):
        return None
    m = DATE_RE.match(s.strip())
    if not m:
        return None
    year = int(m.group(1))
    day = int(m.group(2)) if m.group(2) is not None else 0
    if day < 0 or day > 360:
        return None
    return {"year": year, "day": day}

def iter_markdown(root: pathlib.Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in filenames:
            if fname.lower().endswith(".md"):
                yield pathlib.Path(dirpath) / fname

def ensure_extracted_json(root: pathlib.Path) -> Dict[str, Any]:
    """
    Rebuild extracted_data.json with support for:
    - event: dict OR list[dict]
    - person: dict OR list[dict]
    - star:   dict OR list[dict] with publications[] and translations[]
    JSON structure:
      {
        "meta": {...},
        "event": [...],
        "person": [...],
        "star": {
          "bases": [...],          # star-level info (name, coords, desc, source)
          "publications": [...],   # per-publication rows (date, publishers, desc, major_event)
          "translations": [...]    # per-translation rows (date, translators, desc, major_event)
        }
      }
    """
    out_dir = (root / DERIVED_DIR_REL); out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / EXTRACTED_JSON
    warn_path = out_dir / WARNINGS_MD

    WRITE_JSON_WHEN_DRY = False  # set True if you want the JSON even in DRY runs

    extracted: Dict[str, List[Dict[str, Any]]] = {
        "event": [],
        "person": [],
        "star_base": [],  # star-level info
        "star_pub": [],
        "star_trn": [],
    }
    meta = {
        "front_matters": 0,
        "parsed_events": 0,
        "parsed_people": 0,
        "parsed_star_bases": 0,
        "parsed_star_publications": 0,
        "parsed_star_translations": 0,
        "yaml_loader_usage": {"pyyaml": 0, "fallback": 0},
    }

    def normalize_event_block(block: Dict[str, Any], src_rel: str) -> Optional[Dict[str, Any]]:
        # REQUIRED start date
        sd = parse_mysenvar_date(
            block.get("start_date") or block.get("start") or block.get("date") or block.get("when")
        )
        if sd is None:
            return None

        # Descriptions (new schema) + fallback for old 'desc' into start_desc
        start_desc = block.get("start_desc")
        end_desc   = block.get("end_desc")
        if not isinstance(start_desc, str) or not start_desc.strip():
            # fallback for old schema
            legacy = block.get("desc")
            start_desc = legacy if isinstance(legacy, str) else None
        if isinstance(start_desc, str):
            start_desc = start_desc.strip()
        if isinstance(end_desc, str):
            end_desc = end_desc.strip()

        # Optional end date
        ed_raw = block.get("end_date") or block.get("end")
        ed = parse_mysenvar_date(ed_raw) if ed_raw is not None else None

        return {
            "source": src_rel,
            "kind": "event",
            "start_date": sd,          # {year, day}
            "end_date": ed,            # {year, day} or None
            "start_desc": start_desc,  # str | None
            "end_desc": end_desc,      # str | None
            "major_event": bool(block.get("major_event", False)),
        }

    def normalize_person_block(block: Dict[str, Any], src_rel: str, fm_title: Optional[str]) -> Optional[Dict[str, Any]]:
        nm = block.get("name")
        if not isinstance(nm, str) or not nm.strip(): return None
        out: Dict[str, Any] = {
            "source": src_rel, "kind": "person", "name": nm.strip(),
            "major_event": bool(block.get("major_event", False)),
        }
        b = block.get("birthday")
        if b is not None:
            bp = parse_mysenvar_date(b)
            if bp is not None: out["birthday"] = bp
        d = block.get("death_date") or block.get("death")
        if d is not None:
            dp = parse_mysenvar_date(d)
            if dp is not None: out["death_date"] = dp
        if isinstance(fm_title, str) and fm_title.strip():
            out["title"] = fm_title.strip()
        return out

    def normalize_star_block(block: Dict[str, Any], src_rel: str, fm_title: Optional[str]) -> Tuple[Optional[Dict], List[Dict], List[Dict]]:
        """Return (base, pubs, trns)."""
        name = block.get("name")
        if not isinstance(name, str) or not name.strip():
            return (None, [], [])
        base = {
            "source": src_rel,
            "star_name": name.strip(),
            "coordinates": block.get("coordinates", "") if isinstance(block.get("coordinates"), str) else "",
            "desc": (block.get("desc") or "").strip(),  # star-level description
            "fm_title": fm_title,
        }
        pubs_out = []
        pubs = block.get("publications") or []
        if isinstance(pubs, dict): pubs = [pubs]
        if isinstance(pubs, list):
            for item in pubs:
                if not isinstance(item, dict): continue
                sd = parse_mysenvar_date(item.get("date"))
                if sd is None: continue
                pubs_out.append({
                    "source": src_rel,
                    "star_name": base["star_name"],
                    "date": sd,
                    "desc": (item.get("desc") or "").strip(),  # publication desc
                    "publishers": item.get("publishers"),
                    "major_event": bool(item.get("major_event", False)),
                    "fm_title": fm_title,
                })
        trn_out = []
        trns = block.get("translations") or []
        if isinstance(trns, dict): trns = [trns]
        if isinstance(trns, list):
            for item in trns:
                if not isinstance(item, dict): continue
                sd = parse_mysenvar_date(item.get("date"))
                if sd is None: continue
                trn_out.append({
                    "source": src_rel,
                    "star_name": base["star_name"],
                    "date": sd,
                    "desc": (item.get("desc") or "").strip(),  # translation desc (optional upstream)
                    "translators": item.get("translators"),
                    "major_event": bool(item.get("major_event", False)),
                    "fm_title": fm_title,
                })
        return (base, pubs_out, trn_out)

    for md in iter_markdown(root):
        fm, _, used = read_front_matter(md)
        if used in meta["yaml_loader_usage"]:
            meta["yaml_loader_usage"][used] += 1
        if not isinstance(fm, dict):
            continue
        meta["front_matters"] += 1
        src_rel = md.relative_to(root).as_posix()
        fm_title = fm.get("title") if isinstance(fm.get("title"), str) else None

        # events
        ev_block = fm.get("event")
        if isinstance(ev_block, dict):
            ev = normalize_event_block(ev_block, src_rel)
            if ev: extracted["event"].append(ev); meta["parsed_events"] += 1
        elif isinstance(ev_block, list):
            for item in ev_block:
                if isinstance(item, dict):
                    ev = normalize_event_block(item, src_rel)
                    if ev: extracted["event"].append(ev); meta["parsed_events"] += 1

        # people
        pe_block = fm.get("person")
        if isinstance(pe_block, dict):
            pe = normalize_person_block(pe_block, src_rel, fm_title)
            if pe: extracted["person"].append(pe); meta["parsed_people"] += 1
        elif isinstance(pe_block, list):
            for item in pe_block:
                if isinstance(item, dict):
                    pe = normalize_person_block(item, src_rel, fm_title)
                    if pe: extracted["person"].append(pe); meta["parsed_people"] += 1

        # stars
        st_block = fm.get("star")
        if isinstance(st_block, dict):
            base, pubs, trns = normalize_star_block(st_block, src_rel, fm_title)
            if base: extracted["star_base"].append(base); meta["parsed_star_bases"] += 1
            extracted["star_pub"].extend(pubs); meta["parsed_star_publications"] += len(pubs)
            extracted["star_trn"].extend(trns); meta["parsed_star_translations"] += len(trns)
        elif isinstance(st_block, list):
            for item in st_block:
                if isinstance(item, dict):
                    base, pubs, trns = normalize_star_block(item, src_rel, fm_title)
                    if base: extracted["star_base"].append(base); meta["parsed_star_bases"] += 1
                    extracted["star_pub"].extend(pubs); meta["parsed_star_publications"] += len(pubs)
                    extracted["star_trn"].extend(trns); meta["parsed_star_translations"] += len(trns)

    payload = {
        "meta": meta,
        "event": extracted["event"],
        "person": extracted["person"],
        "star": {
            "bases": extracted["star_base"],
            "publications": extracted["star_pub"],
            "translations": extracted["star_trn"],
        },
    }

    if DRY_RUN and not WRITE_JSON_WHEN_DRY:
        print(f"[DRY] Would write extracted JSON -> {json_path}")
        print(json.dumps(meta, indent=2))
    else:
        json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        warn_path.write_text("# Extraction Warnings\n\n_Auto-extractor run completed._\n", encoding="utf-8")
        print(f"[WROTE] {json_path} and {warn_path}")

    return payload

# ----------------- Decade/Century helpers -----------------
def ordinal(n: int) -> str:
    """Return an ordinal string for an integer day, e.g., 1 -> '1st'."""
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def decade_floor(year: int) -> int:
    # True floor-division; works for negative years (e.g., -12 -> -20)
    return (year // 10) * 10

def year_suffix(year: int) -> str:
    return f"{abs(year)}{' BT' if year < 0 else ' AT'}"

def decade_title(decade_start: int) -> str:
    # Full absolute, e.g., -170 -> "170s BT", 20 -> "20s AT"
    return f"{abs(decade_start)}s {'BT' if decade_start < 0 else 'AT'}"

def ordinal(n: int) -> str:
    if 10 <= (n % 100) <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"

def century_title_from_start(century_start: int) -> str:
    if century_start == 0:
        return "1st Century AT"
    cnum = abs(century_start) // 100 + (1 if century_start > 0 else 0)
    return f"{ordinal(cnum)} Century {'BT' if century_start < 0 else 'AT'}"

def decades_dir(root: pathlib.Path) -> pathlib.Path:
    return (root / DECADES_DIR_REL).resolve()

def centuries_dir(root: pathlib.Path) -> pathlib.Path:
    return (root / CENTURIES_DIR_REL).resolve()

def wiki_target(root: pathlib.Path, file_path: pathlib.Path) -> str:
    """
    Build a vault-style wikilink target from a filesystem path that is
    inside the vault. (Used only for decade/century link rows we generate.)
    """
    rel = file_path.resolve().relative_to(root.resolve()).with_suffix("")
    return rel.as_posix()

def wiki_target_from_source(root: pathlib.Path, source_field: str) -> str:
    """
    Convert the 'source' string saved in extracted_data into a vault-style
    wikilink target. Works even if source_field is absolute and outside root.
    """
    s = str(source_field).replace("\\", "/")
    # strip any leading .../content/ if present
    root_norm = str(root).replace("\\", "/")
    if s.lower().startswith(root_norm.lower() + "/"):
        s = s[len(root_norm) + 1:]
    if s.endswith(".md"):
        s = s[:-3]
    return s

# ----------------- Template & rendering -----------------
DEFAULT_TEMPLATE = """---
title: {{title}}
enableToc: true
tags:
  - topic/history/decade
draft: true
type: index
future: update
status: complete
---

> [!summary] {{title}}
> > [!summary] Decades
> > ... {{decade_links}} ...
> 
> 
> > [!summary] Centuries
> > ... {{century_links}} ...

{{events_block}}{{people_block}}{{stars_block}}# See Also
- [[Encyclopedia Mysenvaria/History/History|History]]
- [[Encyclopedia Mysenvaria/Indexes/History/List of Years|List of Years]]
""".strip("\n")

def load_template() -> str:
    if DECADE_TEMPLATE_PATH and DECADE_TEMPLATE_PATH.is_file():
        return DECADE_TEMPLATE_PATH.read_text(encoding="utf-8")
    return DEFAULT_TEMPLATE

def replace_placeholders(template: str, mapping: Dict[str, str]) -> str:
    out = template
    for k, v in mapping.items():
        out = out.replace(f"{{{{{k}}}}}", v)
    return out

def _alpha_key(s: str) -> str:
    """Lowercased key for alphabetical sorting; keeps wikilinks intact."""
    return s.lower()

def _sort_records(records: list, day_key: str, alpha_key: str):
    """
    Sort in-place:
      - entries with a day first (ascending day), tie-break alpha
      - then entries without a day (alpha)
    """
    def k(rec):
        day = rec.get(day_key, None)
        alpha = _alpha_key(rec.get(alpha_key, ""))
        # Put no-day at the end: (has_day_flag, day_value_or_0, alpha)
        return (0, day if day is not None else 0, alpha) if day is not None else (1, 0, alpha)
    records.sort(key=k)

# ----------------- Build data for pages -----------------
def build_events_births_deaths_and_stars(data: Dict[str, Any], root: pathlib.Path):
    """
    Build:
      events_by_decade: dict[decade] -> dict[year] -> list[{"day": int|None, "alpha": str, "text": str}]
      births_by_decade: dict[decade] -> dict[year] -> list[...]
      deaths_by_decade: dict[decade] -> dict[year] -> list[...]
      stars_by_decade:  dict[decade] -> list[{"year": int, "day": int|None, "alpha": str, "row": dict}]
    """
    events_by_decade: Dict[int, Dict[int, List[Dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    births_by_decade: Dict[int, Dict[int, List[Dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    deaths_by_decade: Dict[int, Dict[int, List[Dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    stars_by_decade:  Dict[int, List[Dict[str, Any]]] = defaultdict(list)

    # --- Normal events (major only) ---
    for ev in data.get("event", []):
        if not ev.get("major_event", False):
            continue

        # START marker
        sd = ev.get("start_date")
        sdesc = ev.get("start_desc")
        if isinstance(sd, dict) and "year" in sd and isinstance(sdesc, str) and sdesc.strip():
            y = int(sd["year"])
            d = int(sd.get("day", 0)) or None
            dstart = (y // 10) * 10
            sdesc_clean = sdesc.strip()
            events_by_decade[dstart][y].append({
                "day": d,
                "alpha": sdesc_clean,
                "text": f"- {sdesc_clean}",
            })

        # END marker (only if we have both end_date and end_desc)
        ed = ev.get("end_date")
        edesc = ev.get("end_desc")
        if isinstance(ed, dict) and "year" in ed and isinstance(edesc, str) and edesc.strip():
            y2 = int(ed["year"])
            d2 = int(ed.get("day", 0)) or None
            dstart2 = (y2 // 10) * 10
            edesc_clean = edesc.strip()
            events_by_decade[dstart2][y2].append({
                "day": d2,
                "alpha": edesc_clean,
                "text": f"- {edesc_clean}",
            })

    # --- People (major only) ---
    for pe in data.get("person", []):
        if not pe.get("major_event", False):
            continue
        title = pe.get("title") or pathlib.Path(pe["source"]).stem
        target = wiki_target_from_source(root, pe["source"])

        b = pe.get("birthday"); d = pe.get("death_date")
        by = int(b["year"]) if isinstance(b, dict) and "year" in b else None
        bd = int(b.get("day", 0)) if isinstance(b, dict) else 0
        dy = int(d["year"]) if isinstance(d, dict) and "year" in d else None
        dd = int(d.get("day", 0)) if isinstance(d, dict) else 0

        # Births
        if by is not None:
            parts = []
            if bd: parts.append(ordinal(bd))
            parts.append(f"[[{target}|{title}]]")
            if dy is not None:
                parts.append(f"(d. {year_suffix(dy)})")
            line = ", ".join([parts[0], " ".join(parts[1:])]) if bd else " ".join(parts)
            births_by_decade[(by // 10) * 10][by].append({
                "day": (bd or None),
                "alpha": title,
                "text": f"- {line}",
            })

        # Deaths
        if dy is not None:
            parts = []
            if dd: parts.append(ordinal(dd))
            parts.append(f"[[{target}|{title}]]")
            if by is not None:
                parts.append(f"(b. {year_suffix(by)})")
            line = ", ".join([parts[0], " ".join(parts[1:])]) if dd else " ".join(parts)
            deaths_by_decade[(dy // 10) * 10][dy].append({
                "day": (dd or None),
                "alpha": title,
                "text": f"- {line}",
            })

    # --- Stars ---
    star_section = data.get("star", {})
    bases = star_section.get("bases", [])
    pubs  = star_section.get("publications", [])
    trns  = star_section.get("translations", [])

    # Add MAJOR pub/trn as events (use their own desc)
    for row in pubs:
        if not row.get("major_event", False):
            continue
        desc = (row.get("desc") or "").strip()
        if not desc:
            continue
        y = int(row["date"]["year"])
        d = int(row["date"].get("day", 0)) or None
        dstart = (y // 10) * 10
        events_by_decade[dstart][y].append({
            "day": d,
            "alpha": desc,
            "text": f"- {desc}",
        })

    for row in trns:
        if not row.get("major_event", False):
            continue
        desc = (row.get("desc") or "").strip()
        if not desc:
            continue
        y = int(row["date"]["year"])
        d = int(row["date"].get("day", 0)) or None
        dstart = (y // 10) * 10
        events_by_decade[dstart][y].append({
            "day": d,
            "alpha": desc,
            "text": f"- {desc}",
        })

    # Star table rows: first publication per star (always included)
    pubs_by_star: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for p in pubs:
        key = (p.get("source", ""), p.get("star_name", ""))
        pubs_by_star[key].append(p)
    for key in pubs_by_star:
        pubs_by_star[key].sort(key=lambda r: (int(r["date"]["year"]), int(r["date"].get("day", 0))))

    for base in bases:
        key = (base.get("source", ""), base.get("star_name", ""))
        first_pub = pubs_by_star.get(key, [None])[0]
        if not first_pub:
            continue  # cannot place in a decade without a publication date

        y = int(first_pub["date"]["year"])
        d = int(first_pub["date"].get("day", 0)) or None
        dstart = (y // 10) * 10

        target = wiki_target_from_source(root, base["source"])
        name  = base.get("star_name") or pathlib.Path(base["source"]).stem
        coords = base.get("coordinates", "") or ""
        star_desc = base.get("desc", "") or ""
        actors = first_pub.get("publishers", [])
        if isinstance(actors, (str, int, float, bool)): actors = [actors]
        actors = [str(a) for a in actors] if isinstance(actors, list) else []

        stars_by_decade[dstart].append({
            "year": y,
            "day": d,
            "alpha": name,
            "row": {
                "name_link": f"[[{target}|{name}]]",
                "coordinates": coords,
                "date": year_suffix(y),
                "actors": ", ".join(actors),
                "desc": star_desc,
            }
        })

    # ---- sort per the rules ----
    for dec in list(events_by_decade.keys()):
        for year in list(events_by_decade[dec].keys()):
            _sort_records(events_by_decade[dec][year], "day", "alpha")

    for dec in list(births_by_decade.keys()):
        for year in list(births_by_decade[dec].keys()):
            _sort_records(births_by_decade[dec][year], "day", "alpha")

    for dec in list(deaths_by_decade.keys()):
        for year in list(deaths_by_decade[dec].keys()):
            _sort_records(deaths_by_decade[dec][year], "day", "alpha")

    # Stars: sort across the whole decade by (year asc, day rule, alpha)
    def star_key(rec):
        y  = rec.get("year", 0)
        d  = rec.get("day", None)
        al = _alpha_key(rec.get("alpha", ""))
        return (y, 0, d, al) if d is not None else (y, 1, 0, al)
    for dec in list(stars_by_decade.keys()):
        stars_by_decade[dec].sort(key=star_key)

    # Convert year->list of dicts into year->list of strings for renderers
    # (renderers expect "text" strings)
    events_text = {dec: {yr: [rec["text"] for rec in lst]
                         for yr, lst in years.items()}
                   for dec, years in events_by_decade.items()}
    births_text = {dec: {yr: [rec["text"] for rec in lst]
                         for yr, lst in years.items()}
                   for dec, years in births_by_decade.items()}
    deaths_text = {dec: {yr: [rec["text"] for rec in lst]
                         for yr, lst in years.items()}
                   for dec, years in deaths_by_decade.items()}

    # Stars: renderer consumes rows’ "row" dicts
    stars_rows = {dec: [rec["row"] for rec in rows] for dec, rows in stars_by_decade.items()}

    # Sort year buckets ascending
    def sort_year_keys(d: Dict[int, Any]) -> Dict[int, Any]:
        return dict(sorted(d.items(), key=lambda kv: kv[0]))

    for k in list(events_text.keys()):
        events_text[k] = sort_year_keys(events_text[k])
    for k in list(births_text.keys()):
        births_text[k] = sort_year_keys(births_text[k])
    for k in list(deaths_text.keys()):
        deaths_text[k] = sort_year_keys(deaths_text[k])

    return events_text, births_text, deaths_text, stars_rows

# ----------------- Link rows -----------------
def decade_starts_in_range() -> List[int]:
    low = (START_YEAR // 10) * 10
    high = (END_YEAR // 10) * 10
    return list(range(low, high + 1, 10))

def in_range_decade(dec_start: int) -> bool:
    low = (START_YEAR // 10) * 10
    high = (END_YEAR // 10) * 10
    return low <= dec_start <= high

def decade_links_row(root: pathlib.Path, decade_start: int) -> str:
    pieces: List[str] = []
    prev_ds = decade_start - 10
    if in_range_decade(prev_ds):
        prev_name = decade_title(prev_ds)
        prev_target = wiki_target(root, decades_dir(root) / f"{prev_name}.md")
        pieces.append(f"[[{prev_target}|{prev_name}]]")
    pieces.append(f"**{decade_title(decade_start)}**")
    next_ds = decade_start + 10
    if in_range_decade(next_ds):
        next_name = decade_title(next_ds)
        next_target = wiki_target(root, decades_dir(root) / f"{next_name}.md")
        pieces.append(f"[[{next_target}|{next_name}]]")
    return ", ".join(pieces)

def century_links_row(root: pathlib.Path, decade_start: int) -> str:
    cdir = centuries_dir(root)
    cur_century_start = (decade_start // 100) * 100
    prev_century = cur_century_start - 100
    next_century = cur_century_start + 100

    def link_if_exists(cs: int) -> Optional[str]:
        name = century_title_from_start(cs)
        p = cdir / f"{name}.md"
        if p.is_file():
            return f"[[{wiki_target(root, p)}|{name}]]"
        return None

    pieces = [x for x in (link_if_exists(prev_century),
                          link_if_exists(cur_century_start),
                          link_if_exists(next_century)) if x]
    return ", ".join(pieces)


# ----------------- Renderers -----------------
def render_events_by_year(events_for_decade: Dict[int, List[str]]) -> str:
    if not events_for_decade:
        return ""
    parts: List[str] = ["# Events"]
    for year, items in events_for_decade.items():
        parts.append(f"## {year_suffix(year)}")
        parts.extend(items)
    return "\n".join(parts) + "\n"

def render_people_grouped(births: Dict[int, List[str]], deaths: Dict[int, List[str]]) -> str:
    if not births and not deaths:
        return ""
    parts: List[str] = ["# Significant People"]
    if births:
        parts.append("## Births")
        for year, items in births.items():
            parts.append(f"### {year_suffix(year)}")
            parts.extend(items)
    if deaths:
        parts.append("## Deaths")
        for year, items in deaths.items():
            parts.append(f"### {year_suffix(year)}")
            parts.extend(items)
    return "\n".join(parts) + "\n"

def render_stars_table(rows: List[Dict[str, Any]]) -> str:
    """
    Render the Stars table at the end of a decade page.
    - Each row represents the first publication of a star.
    - Translations are not included.
    - Escapes all '|' characters so wikilinks display correctly.
    """
    if not rows:
        return ""

    def esc(s: str) -> str:
        # Escape table pipes inside wikilinks or text
        return (s or "").replace("|", r"\|")

    header = (
        "# Stars\n"
        "| Name | [[Encyclopedia Mysenvaria/Geography/Abstract Features/Altitude, Azimuth, & Elevation\\|Coordinates]] "
        "| Date | Publisher(s) | Description |\n"
        "| --- | --- | --- | --- | --- |\n"
    )

    lines = []
    for r in rows:
        # Skip translations — we only want first publications
        if "translators" in r:
            continue

        name = esc(r.get("name_link", ""))
        coords = esc(r.get("coordinates", ""))
        date = esc(r.get("date", ""))
        actors = esc(r.get("actors", ""))
        desc = esc(r.get("desc", ""))

        lines.append(f"| {name} | {coords} | {date} | {actors} | {desc} |")

    return header + "\n".join(lines) + "\n"


# ----------------- Build decade page -----------------
def load_template() -> str:
    if DECADE_TEMPLATE_PATH and DECADE_TEMPLATE_PATH.is_file():
        return DECADE_TEMPLATE_PATH.read_text(encoding="utf-8")
    return DEFAULT_TEMPLATE

def replace_placeholders(template: str, mapping: Dict[str, str]) -> str:
    out = template
    for k, v in mapping.items():
        out = out.replace(f"{{{{{k}}}}}", v)
    return out

def build_decade_page_content(root: pathlib.Path,
                              decade_start: int,
                              events_for_decade: Dict[int, List[str]],
                              births_for_decade: Dict[int, List[str]],
                              deaths_for_decade: Dict[int, List[str]],
                              stars_rows: List[Dict[str, Any]]) -> str:
    template = load_template()

    events_block = render_events_by_year(events_for_decade)
    people_block = render_people_grouped(births_for_decade, deaths_for_decade)
    stars_block  = render_stars_table(stars_rows)

    # If a block exists, prefix with a single blank line to separate from callouts
    if events_block:
        events_block = "\n" + events_block
    if people_block:
        people_block = ("\n" if not events_block else "") + people_block
    if stars_block:
        stars_block = ("\n" if not (events_block or people_block) else "") + stars_block

    mapping = {
        "title": decade_title(decade_start),
        "decade_links": decade_links_row(root, decade_start),
        "century_links": century_links_row(root, decade_start),
        "events_block": events_block,
        "people_block": people_block,
        "stars_block": stars_block,
    }
    out = replace_placeholders(template, mapping)
    return out.rstrip() + "\n"


def main():
    root = find_content_root()

    # How many markdowns are we scanning?
    md_count = sum(1 for _ in iter_markdown(root))
    print(f"[SCAN] content root = {root}")
    print(f"[SCAN] markdown files under root = {md_count}")

    # 1) Extract fresh JSON (events/people/stars, list-aware)
    data = ensure_extracted_json(root)

    # 2) Bucket parsed data
    events_by_decade, births_by_decade, deaths_by_decade, stars_by_decade = build_events_births_deaths_and_stars(data, root)

    # 3) Build ALL decades in range
    ddir = (root / DECADES_DIR_REL); ddir.mkdir(parents=True, exist_ok=True)

    wrote = 0
    low = (START_YEAR // 10) * 10
    high = (END_YEAR // 10) * 10
    for dec in range(low, high + 1, 10):
        content = build_decade_page_content(
            root,
            dec,
            events_by_decade.get(dec, {}),
            births_by_decade.get(dec, {}),
            deaths_by_decade.get(dec, {}),
            stars_by_decade.get(dec, []),
        )
        out_path = ddir / f"{decade_title(dec)}.md"
        if DRY_RUN:
            print(f"[DRY] Would write: {out_path}")
        else:
            out_path.write_text(content, encoding="utf-8")
            print(f"[WROTE] {out_path}")
        wrote += 1

    print(f"Decade pages processed: {wrote} {'(DRY RUN)' if DRY_RUN else ''}")

if __name__ == "__main__":
    main()