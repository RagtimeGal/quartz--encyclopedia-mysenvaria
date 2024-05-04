import os

def find_predecessor(entry, index, input_list):
    for i in range(index-1, -1, -1):
        current_indent = len(entry.split(';')[0]) - len(entry.split(';')[0].lstrip())
        predecessor_indent = len(input_list[i].split(';')[0]) - len(input_list[i].split(';')[0].lstrip())
        if predecessor_indent < current_indent:
            return input_list[i].split('; ')[0].strip()  # Strip leading spaces
    return None

def find_successors(entry, index, input_list):
    successors = []
    current_indent = len(entry.split(';')[0]) - len(entry.split(';')[0].lstrip())
    for i in range(index+1, len(input_list)):
        successor_indent = len(input_list[i].split(';')[0]) - len(input_list[i].split(';')[0].lstrip())
        if successor_indent == current_indent + 1:
            successors.append(input_list[i].split('; ')[0].strip())  # Strip leading spaces
        elif successor_indent <= current_indent:
            break
    return successors

def find_animal_or_plant_entry(entry, index, input_list, is_extinct, is_domestic):
    for i in range(index-1, -1, -1):
        current_entry = input_list[i]
        name, _, _ = current_entry.split('; ')
        if is_extinct:
            if "Animal" in name:
                return "- [[Encyclopedia Mysenvaria/Indexes/Biology/Animals/List of Extinct Animals|List of Extinct Animals]]", "- biology/animal/extinct"
            elif "Plant" in name:
                return "- [[Encyclopedia Mysenvaria/Indexes/Biology/Plants/List of Extinct Plants|List of Extinct Plants]]", "- biology/plant/extinct"
        elif is_domestic:
            if "Animal" in name:
                return "- [[Encyclopedia Mysenvaria/Indexes/Biology/Animals/List of Domesticated Animals|List of Domesticated Animals]]", "- biology/animal/domestic"
            elif "Plant" in name:
                return "- [[Encyclopedia Mysenvaria/Indexes/Biology/Plants/List of Domesticated Plants|List of Domesticated Plants]]", "- biology/plant/domestic"
        else:
            if "Animal" in name:
                return "- [[Encyclopedia Mysenvaria/Indexes/Biology/Animals/Lists of Animals|Lists of Animals]]", "- biology/animal"
            elif "Plant" in name:
                return "- [[Encyclopedia Mysenvaria/Indexes/Biology/Plants/Lists of Plants|Lists of Plants]]", "- biology/plant"
    return None, None

def generate_files_from_list(input_list, template_file, output_directory):
    with open(template_file, 'r') as f:
        template_content = f.read()

    for index, entry in enumerate(input_list):
        name, year, description = entry.split('; ')
        
        predecessors = find_predecessor(entry, index, input_list)
        successors = find_successors(entry, index, input_list)

        # Determine if the entry is a living or extinct species
        is_species = name.strip().startswith("s. ")
        is_extinct = name.strip().startswith("e. ")
        is_domestic = name.strip().startswith("d. ")

        # Remove "s. " prefix from the name if it's a species
        if is_species or is_extinct or is_domestic:
            name = name.strip()[3:]

        # Format predecessors and successors
        formatted_predecessors = format_links(predecessors)
        formatted_successors = format_links(successors)

        # Replace placeholders with entry details
        entry_content = template_content.replace('{name}', name.strip())\
                                         .replace('{year}', year.strip())\
                                         .replace('{description}', description.strip())\
                                         .replace('{predecessors}', formatted_predecessors)\
                                         .replace('{successors}', formatted_successors)

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Determine the appropriate subfolder for species entries
        if is_species:
            species_folder = os.path.join(output_directory, "Species")
            if not os.path.exists(species_folder):
                os.makedirs(species_folder)
            filepath = os.path.join(species_folder, name.strip() + '.md')
        elif is_extinct:
            extinct_folder = os.path.join(output_directory, "Species/Extinct")
            if not os.path.exists(extinct_folder):
                os.makedirs(extinct_folder)
            filepath = os.path.join(extinct_folder, name.strip() + '.md')
        elif is_domestic:
            domestic_folder = os.path.join(output_directory, "Species/Domestic")
            if not os.path.exists(domestic_folder):
                os.makedirs(domestic_folder)
            filepath = os.path.join(domestic_folder, name.strip() + '.md')
        else:
            filepath = os.path.join(output_directory, name.strip() + '.md')

        with open(filepath, 'w') as f_out:
            f_out.write(entry_content)
            
        # Find if the entry is related to "Animal" or "Plant"
        end_line, replace_line = find_animal_or_plant_entry(entry, index, input_list, is_extinct, is_domestic)

        if end_line:
            with open(filepath, 'a') as f_out:
                f_out.write(f"\n{end_line}")

        # If it's a species, replace occurrences of "- biology/taxa" with appropriate replacement
        if any([is_species, is_extinct, is_domestic]) and replace_line:
            replace_biology_taxa(filepath, replace_line)

        # If the entry has successors, update successor links to remove "s. " prefix from species names
        if successors:
            update_successor_links(filepath, successors)

def update_successor_links(filepath, successors):
    with open(filepath, 'r') as f:
        content = f.read()

    for successor in successors:
        if any(prefix in successor for prefix in ["s. ", "e. ", "d. "]):
            updated_successor = successor[3:]  # Remove "s. " prefix
            content = content.replace(successor, updated_successor)

    # If the entry is a species, replace "- biology/taxa" with appropriate replacement
    if "s. " or "e. " or "d. " in filepath:
        if "- biology/taxa" in content:
            if "animal" in content:
                content = content.replace("- biology/taxa", "- biology/animal")
            elif "plant" in content:
                content = content.replace("- biology/taxa", "- biology/plant")

    # Add a line at the end of the file for lists of families if a species successor exists
    if any("s. " or "e. " or "d. " in successor for successor in successors):
        content += "\n- [[Encyclopedia Mysenvaria/Indexes/Biology/Taxa/List of Families|List of Families]]"

    # Add a line after "- biology/taxa" for family classification if a species successor exists
    if "- biology/taxa" in content and any("s. " or "e. " or "d. " in successor for successor in successors):
        content = content.replace("- biology/taxa", "- biology/taxa/family\n  - biology/taxa")

    # Write the updated content back to the file
    with open(filepath, 'w') as f:
        f.write(content)

def replace_biology_taxa(filepath, replacement):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace occurrences of "- biology/taxa" with appropriate replacement
    if "- biology/taxa" in content:
        content = content.replace("- biology/taxa", replacement)
    
    # Write the updated content back to the file
    with open(filepath, 'w') as f:
        f.write(content)

def format_links(entries):
    if entries is None:
        return 'None'
    elif not entries:
        return 'None'
    else:
        if isinstance(entries, str):
            if entries.startswith("s. "):
                formatted_entry = f"[[Encyclopedia Mysenvaria/Biology/Taxa/Species/{entries[3:]}|{entries[3:]}]]"
            elif entries.startswith("e. "):
                formatted_entry = f"[[Encyclopedia Mysenvaria/Biology/Taxa/Species/Extinct/{entries[3:]}|{entries[3:]}]]"
            elif entries.startswith("d. "):
                formatted_entry = f"[[Encyclopedia Mysenvaria/Biology/Taxa/Species/Domestic/{entries[3:]}|{entries[3:]}]]"
            else:
                formatted_entry = f"[[Encyclopedia Mysenvaria/Biology/Taxa/{entries}|{entries}]]"
            return formatted_entry
        elif isinstance(entries, list):
            formatted_entries = []
            for entry in entries:
                if entry.startswith("s. "):
                    formatted_entry = f"[[Encyclopedia Mysenvaria/Biology/Taxa/Species/{entry[3:]}|{entry[3:]}]]"
                elif entry.startswith("e. "):
                    formatted_entry = f"[[Encyclopedia Mysenvaria/Biology/Taxa/Species/Extinct/{entry[3:]}|{entry[3:]}]]"
                elif entry.startswith("d. "):
                    formatted_entry = f"[[Encyclopedia Mysenvaria/Biology/Taxa/Species/Domestic/{entry[3:]}|{entry[3:]}]]"
                else:
                    formatted_entry = f"[[Encyclopedia Mysenvaria/Biology/Taxa/{entry}|{entry}]]"
                formatted_entries.append(formatted_entry)
            return ', '.join(formatted_entries)
        else:
            return 'Invalid input'

# Example usage
directory = r'c:\Users\Terra\Desktop\Worldbuilding\Mysenvar_Branch\Mysenvar\Meta\Python\Taxa Page Generator\\'
template_file = os.path.join(directory, "template.md")
output_directory = os.path.join(directory, "Taxa")

# Read the input list from list.txt file
input_list = []
with open(os.path.join(directory, 'list.txt'), 'r') as file:
    input_list = file.readlines()

generate_files_from_list(input_list, template_file, output_directory)