#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
featured_block_generator.py

1. Loads the centralized metadata database.
2. Identifies pages with 'featured_data'.
3. Randomly selects one "Featured Article" and a pool of "Fun Facts".
4. REPLACES ONLY THE FIRST call-out box in _index.md.
"""

import os
import json
import pathlib
import random
import re
from typing import Any, Dict, List, Tuple

# --- Configuration ---
METADATA_PATH = "content/Meta/Programs/debug/metadata_aggregator/extracted_metadata.json"
HOME_PAGE_PATH = "content/_index.md"
MAX_FUN_FACTS = 5
DRY_RUN = False

def load_metadata() -> List[Dict[str, Any]]:
    """Loads the pre-aggregated metadata JSON."""
    if not os.path.exists(METADATA_PATH):
        print(f"[ERROR] Metadata file not found at {METADATA_PATH}. Run aggregator first.")
        return []
    
    with open(METADATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("pages", [])

def get_featured_pages(pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filters for pages containing 'featured_data'."""
    featured_list = []
    for p in pages:
        meta = p.get("metadata", {})
        if "featured_data" in meta:
            fd = meta["featured_data"]
            featured_list.append({
                "src_rel": p.get("src_rel"),
                "title": meta.get("title", "Untitled"),
                "desc": fd.get("featured_desc", ""),
                "image": fd.get("featured_image", ""),
                "fun_facts": fd.get("fun_facts", []) if isinstance(fd.get("fun_facts"), list) else [fd.get("fun_facts")] if fd.get("fun_facts") else []
            })
    return featured_list

def render_featured_block(featured: Dict[str, Any], facts: List[str]) -> List[str]:
    """Builds the Markdown call-out block."""
    desc = featured["desc"]
    img = str(featured["image"]).strip() if featured["image"] else ""
    chosen_facts = facts[:MAX_FUN_FACTS]

    out = [
        "> [!tip] Featured Article & Fun Facts",
        "> > [!note] Featured Article",
        "> > ",
        f"> > {desc}",
    ]

    if img:
        out.append(f"> > {img}")

    out.extend([
        ">",
        "> > [!info] Did you know...",
    ])

    for f in chosen_facts:
        out.append(f"> > - {f}")

    return out

def replace_first_callout(lines: List[str], new_block: List[str]) -> Tuple[List[str], bool]:
    """
    Finds the first callout and replaces it.
    Ensures that it does not swallow the next callout by stopping at the first sign of a new one.
    """
    start_index = None
    end_index = None
    callout_header_re = re.compile(r"^> \[!")

    for i, line in enumerate(lines):
        if callout_header_re.match(line):
            start_index = i
            
            # Find where this specific callout ends
            for j in range(i + 1, len(lines)):
                current_line = lines[j]
                
                # If we see the START of another callout, the previous one ended before this.
                if callout_header_re.match(current_line):
                    end_index = j
                    break
                
                # If the line doesn't start with '>' and isn't empty, the blockquote has ended.
                if not current_line.startswith(">") and current_line.strip() != "":
                    end_index = j
                    break
            
            if end_index is None:
                end_index = len(lines)
            break

    if start_index is None:
        return lines, False

    # To avoid merging callouts, we ensure there is an empty line between the new block
    # and the line that follows (if that line is the start of another callout).
    final_lines = lines[:start_index] + new_block
    
    # If the end_index points to a new callout, ensure we have a separator
    if end_index < len(lines) and callout_header_re.match(lines[end_index]):
        # Check if the last line of our block is already empty-ish
        if final_lines[-1].strip() != "":
            final_lines.append("")

    final_lines.extend(lines[end_index:])
    
    return final_lines, True

def main():
    pages = load_metadata()
    if not pages: return

    featured_pool = get_featured_pages(pages)
    if not featured_pool:
        print("[INFO] No featured_data found.")
        return

    all_facts = []
    for p in featured_pool:
        all_facts.extend(p["fun_facts"])
    random.shuffle(all_facts)

    eligible_articles = [p for p in featured_pool if p["desc"]]
    if not eligible_articles:
        print("[WARN] No articles with descriptions.")
        return

    selected_article = random.choice(eligible_articles)
    new_block = render_featured_block(selected_article, all_facts)

    if not os.path.exists(HOME_PAGE_PATH):
        print(f"[ERROR] {HOME_PAGE_PATH} missing.")
        return

    with open(HOME_PAGE_PATH, 'r', encoding='utf-8') as f:
        content_lines = f.read().splitlines()

    new_content_lines, changed = replace_first_callout(content_lines, new_block)

    if changed:
        if DRY_RUN:
            print(f"[DRY] Would update with: {selected_article['title']}")
        else:
            with open(HOME_PAGE_PATH, 'w', encoding='utf-8') as f:
                f.write("\n".join(new_content_lines) + "\n")
            print(f"[SUCCESS] Replaced first callout with: {selected_article['title']}")
    else:
        print("[SKIP] No callout found to replace.")

if __name__ == "__main__":
    main()