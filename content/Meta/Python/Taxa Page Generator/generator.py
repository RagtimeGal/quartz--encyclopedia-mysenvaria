import json
import os
from jinja2 import Environment, FileSystemLoader

# Load the JSON data from a file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Determine the appropriate tag based on the entry's position in the hierarchy
def determine_tag(entry):
    if 'successors' not in entry:
        return "species"
    elif all('successors' not in successor for successor in entry['successors']):
        return "family"
    else:
        return None

# Function to find the root ancestor
def find_root_ancestor(entry_name, root_ancestors, all_entries):
    current = all_entries.get(entry_name)
    while current:
        if current['name'] in root_ancestors:
            return current['name']
        predecessor_name = None
        # Find the predecessor by checking which entry has this entry as a successor
        for name, data in all_entries.items():
            if 'successors' in data and any(successor['name'] == current['name'] for successor in data['successors']):
                predecessor_name = name
                break
        if not predecessor_name:
            break
        current = all_entries.get(predecessor_name)
    return None

# Recursive function to collect all entries by name
def collect_entries_by_name(entry, collected):
    collected[entry['name']] = entry
    if 'successors' in entry:
        for successor in entry['successors']:
            collect_entries_by_name(successor, collected)

# Recursive function to process each entry in the JSON tree and generate a file
def process_entry(entry, template, output_dir, all_entries, root_ancestors, predecessor_link=None):
    # Prepare the data for rendering
    data = entry.copy()
    data['tags'] = determine_tag(entry) if determine_tag(entry) else None
    data['extinct'] = entry.get('extinct', False)
    data['predecessor'] = predecessor_link
    data['root_ancestor'] = find_root_ancestor(entry['name'], root_ancestors, all_entries)

    # Ensure 'link' is always present in data
    if 'link' not in data:
        if data['tags'] == "species":
            data['link'] = f"[[Encyclopedia Mysenvaria/Biology/Species/{data['name']}|{data['name']}]]"
        else:
            data['link'] = f"[[Encyclopedia Mysenvaria/Biology/Taxa/{data['name']}|{data['name']}]]"

    # Determine the predecessor link
    if not predecessor_link:
        predecessor_entry = None
        for name, potential_predecessor in all_entries.items():
            if 'successors' in potential_predecessor and any(successor['name'] == data['name'] for successor in potential_predecessor['successors']):
                predecessor_entry = potential_predecessor
                break
        if predecessor_entry:
            if 'link' in predecessor_entry:
                data['predecessor'] = predecessor_entry['link']
            elif determine_tag(predecessor_entry) == "species":
                data['predecessor'] = f"[[Encyclopedia Mysenvaria/Biology/Species/{predecessor_entry['name']}|{predecessor_entry['name']}]]"
            else:
                data['predecessor'] = f"[[Encyclopedia Mysenvaria/Biology/Taxa/{predecessor_entry['name']}|{predecessor_entry['name']}]]"
        else:
            data['predecessor'] = None

    # Set tags for successors before rendering
    if 'successors' in entry:
        for successor in entry['successors']:
            successor['tags'] = determine_tag(successor)

    # Print the data passed to the template for debugging
    print(f"Processing {data['name']}:")
    for key, value in data.items():
        print(f"  {key}: {value} (Type: {type(value)})")

    # Determine if this entry should generate a page
    generate = entry.get('generate', True)
    if generate:
        # Render the template with the entry data
        rendered_content = template.render(data)

        # Create a file name based on the entry name
        folder = "Species" if data['tags'] == "species" else "Taxa"
        file_name = f"{data['name']}.md"
        output_path = os.path.join(output_dir, folder, file_name)

        # Create the folder if it doesn't exist
        os.makedirs(os.path.join(output_dir, folder), exist_ok=True)

        # Write the rendered content to the file
        with open(output_path, 'w') as output_file:
            output_file.write(rendered_content)

    # Process any successors recursively
    if 'successors' in entry:
        for successor in entry['successors']:
            successor_link = f"[[Encyclopedia Mysenvaria/Biology/Taxa/{successor['name']}|{successor['name']}]]"
            if successor.get('link'):
                successor_link = successor['link']
            process_entry(successor, template, output_dir, all_entries, root_ancestors, predecessor_link=data['link'])

def main():
    # Load the JSON file
    json_file_path = 'C:\\Users\\Terra\\Documents\\Worldbuilding\\Mysenvar_Branch\\Mysenvar\\Meta\\Python\\Taxa Page Generator\\taxonomy.json'  # Replace with your JSON file path
    data = load_json(json_file_path)

    # Collect all entries by name
    all_entries = {}
    collect_entries_by_name(data, all_entries)

    # Define root ancestors
    root_ancestors = {"Animal", "Plant"}

    # Load the Jinja2 template
    template_dir = 'C:\\Users\\Terra\\Documents\\Worldbuilding\\Mysenvar_Branch\\Mysenvar\\Meta\\Python\\Taxa Page Generator'  # Replace with your template directory
    template_file = 'template.txt'  # Replace with your template file name
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    # Create an output directory if it doesn't exist
    output_dir = 'C:\\Users\\Terra\\Documents\\Worldbuilding\\Mysenvar_Branch\\Mysenvar\\Meta\\Python\\Taxa Page Generator\\Output'  # Replace with your desired output directory
    os.makedirs(output_dir, exist_ok=True)

    # Process the JSON data and generate output files
    process_entry(data, template, output_dir, all_entries, root_ancestors)

if __name__ == '__main__':
    main()
