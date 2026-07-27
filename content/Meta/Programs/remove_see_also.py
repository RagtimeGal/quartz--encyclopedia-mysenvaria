import os
import re

# ==================== CONFIGURATION ====================
# Path to your Markdown folder or Obsidian vault directory
VAULT_PATH = r"C:\Users\Terra\Documents\Github Folders\quartz--encyclopedia-mysenvaria\content"

# Set DRY_RUN = False when you're ready to actually overwrite the files
DRY_RUN = True
# =======================================================


def remove_see_also_section(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex breakdown:
    # (?m)          -> Multiline mode (makes ^ match start of line)
    # ^#{1,6}\s+    -> Matches 1 to 6 '#' symbols followed by spaces (any header level)
    # See Also\s*   -> Matches "See Also" case-insensitively
    # \n            -> Captures the newline after header
    # (?:[\s\S]*?)  -> Non-greedily captures all content under the header
    # (?=\n#{1,6}\s|\Z) -> Stops before the next header OR end of file (\Z)
    pattern = r"(?mi)^#{1,6}\s+See Also\s*\n(?:[\s\S]*?)(?=\n#{1,6}\s|\Z)"

    # Check if pattern exists in file
    if re.search(pattern, content):
        new_content = re.sub(pattern, "", content)

        # Clean up any trailing blank lines left behind at the end of the file/section
        new_content = re.sub(r"\n{3,}$", "\n\n", new_content)

        if not DRY_RUN:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[MODIFIED] {os.path.basename(file_path)}")
        else:
            print(f"[WOULD MODIFY] {os.path.basename(file_path)}")
        return True

    return False


def main():
    print(
        f"--- Starting Cleanup {'(DRY RUN - No files will be changed)' if DRY_RUN else '(LIVE RUN)'} ---"
    )

    modified_count = 0
    total_files = 0

    for root, _, files in os.walk(VAULT_PATH):
        for file in files:
            if file.endswith(".md"):
                total_files += 1
                file_path = os.path.join(root, file)
                if remove_see_also_section(file_path):
                    modified_count += 1

    print("\n--- Summary ---")
    print(f"Total .md files scanned: {total_files}")
    print(f"Files containing '# See Also': {modified_count}")

    if DRY_RUN and modified_count > 0:
        print(
            "\nTo apply these changes, set 'DRY_RUN = False' at the top of the script and run it again!"
        )


if __name__ == "__main__":
    main()