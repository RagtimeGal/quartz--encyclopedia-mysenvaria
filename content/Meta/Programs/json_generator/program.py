import json
import os
import subprocess
import re

def get_git_root():
    """Finds the root directory of the current git repository."""
    try:
        root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], 
                                        stderr=subprocess.DEVNULL).decode('utf-8').strip()
        return root
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to current working directory if not in a git repo
        return os.getcwd()

def safe_replace(template, replacements):
    """
    Replaces {key} in template with values from replacements dict.
    This is safer than .format() when the string contains other braces like [[link]].
    """
    for key, value in replacements.items():
        # Replaces {lowercase} with the actual value, etc.
        template = template.replace(f"{{{key}}}", str(value))
    return template

def process_templates(custom_path=None):
    # If a path is provided, use it; otherwise, look for input.json in the specific git path
    if custom_path:
        json_filename = custom_path
    else:
        git_root = get_git_root()
        # Path: content\Meta\Programs\json_generator\input.json
        json_filename = os.path.join(git_root, 'content', 'Meta', 'Programs', 'json_generator', 'input.json')
    
    if not os.path.exists(json_filename):
        print(f"Error: Could not find '{json_filename}'.")
        return

    try:
        # Using utf-8-sig to handle files that might have a BOM (Byte Order Mark)
        with open(json_filename, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            content = content.strip()
            content = content.replace('\xa0', ' ')
            
            if not content:
                print(f"Error: The file '{json_filename}' appears to be empty.")
                return
                
            data = json.loads(content)
            
        insertions = data.get("insertions", {})
        templates = data.get("generate", [])
        
        keys = list(insertions.keys())
        if not keys:
            print("No insertion lists found in JSON.")
            return

        num_items = len(insertions[keys[0]])
        final_output_lines = []

        # Changed grouping logic: Iterate through templates first
        for template in templates:
            for i in range(num_items):
                current_replacements = {}
                for key in keys:
                    if i < len(insertions[key]):
                        current_replacements[key] = insertions[key][i]
                
                output = safe_replace(template, current_replacements)
                final_output_lines.append(output)
            
            # Separator between different template batches
            final_output_lines.append("\n" + "="*30 + "\n")

        # Join the lines for printing and saving
        full_text = "\n".join(final_output_lines)
        
        # Print to console
        print(full_text)

        # Export to TXT file
        output_txt_path = os.path.splitext(json_filename)[0] + "_output.txt"
        with open(output_txt_path, 'w', encoding='utf-8') as out_f:
            out_f.write(full_text)
        
        print(f"Success! Output also saved to: {output_txt_path}")

    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON in '{json_filename}'.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    process_templates()