import os
import re
import json
import sys

# --- Constants & Defaults ---
DEFAULT_VALUES = {
    "type": "article",
    "status": "empty",
    "enableToc": True
}
EXCLUDE_DIRS = {".git", "node_modules", "dist", "__pycache__"}
DRY_RUN = False  # Set to True for console summary only

def get_ordinal(n):
    """Returns ordinal string for an integer (1st, 2nd, 3rd, etc)."""
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    return f"{n}" + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

def fallback_parse_yaml(text):
    """Basic YAML parser for scalars and inline lists as per Step 3."""
    data = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, val = [x.strip() for x in line.split(":", 1)]
        # Handle inline lists [a, b]
        if val.startswith("[") and val.endswith("]"):
            data[key] = [i.strip().strip("'\"") for i in val[1:-1].split(",")]
        elif val.lower() == "true": data[key] = True
        elif val.lower() == "false": data[key] = False
        elif val.replace(".", "", 1).isdigit():
            data[key] = float(val) if "." in val else int(val)
        else:
            data[key] = val.strip("'\"")
    return data

def parse_mysenvar_date(value):
    """
    Step 7: Normalise any date field.
    Calculates relative seasonal day: 1-90 (Spring), 91-180 (Summer), etc.
    """
    try:
        y, d = None, None
        
        # Format normalization
        if isinstance(value, (list, tuple)):
            y = int(value[0])
            d = int(value[1]) if len(value) > 1 else None
        elif isinstance(value, dict):
            y = int(value.get("year", 0))
            d = int(value.get("day")) if "day" in value else None
        elif isinstance(value, (int, float)):
            y = int(value)
        elif isinstance(value, str):
            clean = str(value).strip("'\" []")
            parts = re.split(r'[,\-]', clean)
            y = int(parts[0].strip())
            if len(parts) > 1:
                d = int(parts[1].strip())

        suffix = "AT" if y >= 0 else "BT"
        abs_y = abs(y)

        if d is not None:
            if not (1 <= d <= 360):
                return None # Invalid day
            
            # 0: Spring, 1: Summer, 2: Autumn, 3: Winter
            season_idx = (d - 1) // 90
            season_names = ["Spring", "Summer", "Autumn", "Winter"]
            season_name = season_names[season_idx]
            
            # Relative day in season: e.g. 186 -> (186 - (2*90)) = 6
            relative_day = d - (season_idx * 90)
            
            formal = f"{get_ordinal(relative_day)} of {season_name}, {abs_y}{suffix}"
            informal = f"{y}-{d}"
            return {"original": value, "formal": formal, "informal": informal}
        
        # Year only
        return {"original": value, "formal": f"{abs_y}{suffix}", "informal": f"{y}"}
    except:
        return None

class MetadataAggregator:
    def __init__(self):
        self.warnings = []
        self.pages = []
        self.file_count = 0

    def log_warning(self, msg):
        self.warnings.append(msg)

    def find_root(self):
        """Step 1: Locate the vault."""
        root_env = os.environ.get("METADATA_AGG_CONTENT_ROOT")
        if root_env and os.path.isdir(root_env):
            return os.path.abspath(root_env)
        
        heuristics = [
            os.path.join(os.environ.get("GITHUB_WORKSPACE", ""), "content"),
            os.path.join(os.path.dirname(__file__), "content"),
            os.path.join(os.getcwd(), "content")
        ]
        
        for p in heuristics:
            if os.path.isdir(p):
                return os.path.dirname(os.path.abspath(p))
        
        curr = os.path.abspath(os.getcwd())
        for _ in range(5):
            check = os.path.join(curr, "content")
            if os.path.isdir(check):
                return curr
            curr = os.path.dirname(curr)
            
        return None

    def recursive_resolve(self, node, clean_defs):
        """Recursively walks through dicts and lists to resolve string values."""
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, str):
                    stripped_v = v.strip("'\" ")
                    if stripped_v in clean_defs:
                        node[k] = clean_defs[stripped_v]
                elif isinstance(v, (dict, list)):
                    self.recursive_resolve(v, clean_defs)
        elif isinstance(node, list):
            for i, item in enumerate(node):
                if isinstance(item, str):
                    stripped_v = item.strip("'\" ")
                    if stripped_v in clean_defs:
                        node[i] = clean_defs[stripped_v]
                elif isinstance(item, (dict, list)):
                    self.recursive_resolve(item, clean_defs)

    def process_metadata_node(self, data, definitions, src_id, is_subpage=False, parent_link=None, rel_path=""):
        """Steps 5 through 9: Enrich a metadata dictionary."""
        
        # Step 5: Apply default keys
        for k, v in DEFAULT_VALUES.items():
            if k not in data:
                data[k] = v
                self.log_warning(f"{src_id}: missing key `{k}` added with default value `{v}`.")

        # Ensure title exists for link generation
        if "title" not in data:
             data["title"] = os.path.splitext(os.path.basename(rel_path))[0]

        # Step 6: Resolve string values recursively via the comment block
        clean_defs = {str(dk).strip("'\" "): str(dv).strip("'\" ") for dk, dv in definitions.items()}
        self.recursive_resolve(data, clean_defs)

        # Step 7: Normalise any date fields (search recursively for 'date' in keys)
        def resolve_dates_recursive(node):
            if isinstance(node, dict):
                for k in list(node.keys()):
                    if isinstance(node[k], (dict, list)):
                        resolve_dates_recursive(node[k])
                    if "date" in k.lower():
                        norm = parse_mysenvar_date(node[k])
                        if norm:
                            node[k] = norm
            elif isinstance(node, list):
                for item in node:
                    resolve_dates_recursive(item)

        resolve_dates_recursive(data)

        # Step 8 & 9: Ensure a link exists (Moved inside metadata)
        if "link" not in data:
            title = data["title"]
            if is_subpage:
                slug = title.lower().replace(" ", "-")
                data["link"] = f"{parent_link}#{slug}"
            else:
                path_no_ext = os.path.splitext(rel_path)[0]
                normalized_path = path_no_ext.replace("\\", "/")
                data["link"] = f"[[{normalized_path}|{title}]]"
        
        return data

    def process_file(self, full_path, rel_path):
        """Step 2, 3, 4, and 10."""
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Step 3: Read front-matter
        fm_dict, body_text = {}, content
        parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) >= 3:
            fm_text = parts[1]
            body_text = parts[2]
            try:
                import yaml
                fm_dict = yaml.safe_load(fm_text) or {}
            except (ImportError, Exception):
                fm_dict = fallback_parse_yaml(fm_text)

        # Step 4: Parse the %% … %% comment block
        definitions = {}
        comment_match = re.search(r'%%\s*$(.*?)\s*%%', body_text, re.MULTILINE | re.DOTALL)
        if comment_match:
            block_content = comment_match.group(1).strip()
            for line in block_content.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    definitions[k.strip()] = v.strip()

        # Step 10: Build main page record
        clean_rel_path = rel_path.replace("\\", "/")
        fm_dict = self.process_metadata_node(fm_dict, definitions, clean_rel_path, rel_path=clean_rel_path)
        
        main_page = {
            "src_rel": clean_rel_path,
            "definitions": definitions,
            "metadata": fm_dict
        }
        self.pages.append(main_page)

        # Step 9: Handle subpage entries
        if "subpage" in fm_dict and isinstance(fm_dict["subpage"], list):
            for i, sub_fm in enumerate(fm_dict["subpage"]):
                if not isinstance(sub_fm, dict):
                    self.log_warning(f"{clean_rel_path}: malformed subpage entry at index {i}.")
                    continue
                
                sub_src_rel = f"{clean_rel_path}::subpage[{i}]"
                processed_sub = self.process_metadata_node(
                    sub_fm, 
                    definitions, 
                    sub_src_rel, 
                    is_subpage=True, 
                    parent_link=fm_dict.get("link")
                )
                
                sub_page = {
                    "src_rel": sub_src_rel,
                    "definitions": definitions,
                    "metadata": processed_sub,
                    "parent": clean_rel_path
                }
                self.pages.append(sub_page)

    def run(self):
        root = self.find_root()
        if not root:
            print("Error: Could not find 'content' folder via env var or heuristics.")
            sys.exit(1)

        content_root = os.path.join(root, "content")
        print(f"Aggregating metadata from: {content_root}")
        
        for dirpath, dirnames, filenames in os.walk(content_root):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            
            for filename in filenames:
                if filename.lower().endswith(".md"):
                    self.file_count += 1
                    full_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(full_path, content_root)
                    
                    try:
                        self.process_file(full_path, rel_path)
                    except Exception as e:
                        self.log_warning(f"{rel_path}: Unexpected exception: {str(e)}")

        # Final Output Path
        output_dir = os.path.join(root, "content", "Meta", "Programs", "debug", "metadata_aggregator")
        
        json_payload = {
            "meta": {
                "total_markdown_files": self.file_count,
                "pages_extracted": len(self.pages),
                "warnings": len(self.warnings),
                "working_directory": os.getcwd()
            },
            "pages": self.pages
        }

        if DRY_RUN:
            print(f"DRY RUN - Found {len(self.pages)} entries.")
        else:
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, "extracted_metadata.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_payload, f, indent=4, ensure_ascii=False)
            print(f"SUCCESS: Metadata written to {output_file}")
            
            with open(os.path.join(output_dir, "metadata_warnings.txt"), 'w', encoding='utf-8') as f:
                if not self.warnings:
                    f.write("_No warnings_")
                else:
                    f.write("# Metadata Aggregator Warnings\n\n## Issues detected\n")
                    for w in self.warnings:
                        f.write(f"- {w}\n")

if __name__ == "__main__":
    MetadataAggregator().run()