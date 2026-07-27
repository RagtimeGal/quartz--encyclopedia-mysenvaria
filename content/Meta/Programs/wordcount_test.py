import os
import re

# Points to the Quartz content folder where the script is located
VAULT_PATH = r"C:\Users\Terra\Documents\Github Folders\quartz--encyclopedia-mysenvaria\content"

def clean_markdown_content(text):
    # 1. Remove YAML frontmatter (between triple dashes at the start)
    text = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=re.DOTALL)
    
    # 2. Remove blockquote callouts (lines starting with >)
    text = re.sub(r'^\s*>.*$', '', text, flags=re.MULTILINE)
    
    # 3. Remove inline code and code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`.*?`', '', text)
    
    # 4. Strip markdown formatting (headers, bold, italics, links)
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Keep link text, drop URL
    text = re.sub(r'[*_~]', '', text)
    
    return text

def audit_vault(vault_path):
    total_diegetic_words = 0
    total_files = 0
    
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Skip full addenda files if you want to exclude design notes entirely
                    if 'type: addenda' in content or 'topic/meta/addenda' in content or 'topic/meta' in content:
                        continue
                    
                    cleaned_text = clean_markdown_content(content)
                    words = cleaned_text.split()
                    total_diegetic_words += len(words)
                    total_files += 1

    print(f"\n--- Vault Diegetic Word Count Audit ---")
    print(f"Total Main Articles Analyzed: {total_files}")
    print(f"Total Pure Worldbuilding Words: {total_diegetic_words:,}\n")

if __name__ == "__main__":
    audit_vault(VAULT_PATH)