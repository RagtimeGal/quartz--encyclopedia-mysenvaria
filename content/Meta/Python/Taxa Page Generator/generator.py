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
def process_entry(entry, template, output_dir, all_entries, root_ancestors, predecessor=None):
    # Determine if this entry should generate a page
    generate = entry.get('generate', True)

    if generate:
        # Determine the tag for the current entry
        tag = determine_tag(entry)

        # Prepare the data for rendering
        data = entry.copy()
        data['tags'] = tag if tag else None

        # Set the extinct field to false if not specified
        if 'extinct' not in data:
            data['extinct'] = False

        # Set the predecessor
        data['predecessor'] = predecessor

        # Determine the root ancestor
        root_ancestor = find_root_ancestor(entry['name'], root_ancestors, all_entries)
        data['root_ancestor'] = root_ancestor

        # Render the template with the entry data
        rendered_content = template.render(data)

        # Create a file name based on the entry name
        file_name = f"{entry['name'].replace(' ', '_')}.md"
        output_path = os.path.join(output_dir, file_name)

        # Write the rendered content to the file
        with open(output_path, 'w') as output_file:
            output_file.write(rendered_content)

    # Process any successors recursively
    if 'successors' in entry:
        for successor in entry['successors']:
            process_entry(successor, template, output_dir, all_entries, root_ancestors, predecessor=entry['name'])

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
    template_file = 'template.md'  # Replace with your template file name
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    # Create an output directory if it doesn't exist
    output_dir = 'C:\\Users\\Terra\\Documents\\Worldbuilding\\Mysenvar_Branch\\Mysenvar\\Meta\\Python\\Taxa Page Generator\\Taxa'  # Replace with your desired output directory
    os.makedirs(output_dir, exist_ok=True)

    # Process the JSON data and generate output files
    process_entry(data, template, output_dir, all_entries, root_ancestors)

if __name__ == '__main__':
    main()
