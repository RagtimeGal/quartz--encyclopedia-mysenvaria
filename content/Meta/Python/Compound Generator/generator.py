import json
import pubchempy as pcp
import os
import shutil

def read_library_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            library = json.load(file)
        return library
    except Exception as e:
        print(f"Error reading library from JSON: {e}")
        return None

def get_compound_elements(compound_name):
    try:
        compound = pcp.get_compounds(compound_name, 'name')[0]  # Assuming the first result is the desired compound
        return compound.to_dict(properties=['atoms'])['atoms']
    except Exception as e:
        print(f"Error fetching compound '{compound_name}': {e}")
        return None

def write_compound_elements_to_file(compound_name, elements, output_file, element_names):
    if elements:
        # Set to store unique elements encountered
        unique_elements = set()
        with open(output_file, "a") as file:  # Open file in append mode
            for atom in elements:
                symbol = atom['element']
                if symbol not in unique_elements:
                    element_name = element_names.get(symbol, symbol)  # Get the element name from the dictionary
                    # Remove spaces from compound name
                    compound_name_no_spaces = compound_name.replace(" ", "")
                    file.write(f"{element_name}-->{compound_name_no_spaces}\n")
                    unique_elements.add(symbol)

# Directory for files
directory = 'c:\\Users\\Terra\\Desktop\\Worldbuilding\\Mysenvar_Branch\\Mysenvar\\Meta\\Python\\Compound Generator\\'

# Read library from JSON file
library = read_library_from_json(os.path.join(directory, "library.json"))
if library:
    element_names = library.get("dictionary", {})
    compounds_of_interest = library.get("compounds", [])

    # Remove duplicate entries
    compounds_of_interest = list(set(compounds_of_interest))

    # Output file to store compound elements
    output_file = os.path.join(directory, "compound_list.txt")

    # Clear contents of the output file
    with open(output_file, "w") as file:
        file.write("")  # Writing an empty string clears the file

    # Iterate over compounds of interest and fetch their elements
    for compound in compounds_of_interest:
        elements = get_compound_elements(compound)
        if elements:
            write_compound_elements_to_file(compound, elements, output_file, element_names)

    # Write compound list in alphabetical order
    with open(output_file, "a") as file:
        file.write("subgraph CompoundGods[Compound Gods]\ndirection LR\n")
        compound_list = sorted(compounds_of_interest, key=str.lower)
        for compound in compound_list:
            if " " in compound:
                no_space_name = compound.replace(" ", "")
                file.write(f"{no_space_name}[{compound}]\n ")
            else:
                file.write(f"{compound}\n ")
        file.write("end\n\n")

    # Create Templates folder if it doesn't exist
    templates_folder = os.path.join(directory, "Templates")
    if not os.path.exists(templates_folder):
        os.makedirs(templates_folder)

    # Read template file
    template_file_path = os.path.join(directory, "template.md")
    with open(template_file_path, "r") as template_file:
        template_content = template_file.read()

    # Create template for each compound
    for compound in compounds_of_interest:
        # Copy template and rename it
        new_template_path = os.path.join(templates_folder, f"God of {compound}.md")
        shutil.copyfile(template_file_path, new_template_path)

        # Replace {compound_name} with compound name in the template
        with open(new_template_path, "r+") as new_template_file:
            content = new_template_file.read().replace("{compound_name}", compound)
            new_template_file.seek(0)
            new_template_file.write(content)
            new_template_file.truncate()

        # Replace {link_to_elements} with links to elements in the template
        elements_links = set()  # Using a set to ensure uniqueness
        compound_elements = get_compound_elements(compound)
        if compound_elements:
            for atom in compound_elements:
                element_symbol = atom['element']
                element_name = element_names.get(element_symbol, element_symbol)
                elements_links.add(f"[[Encyclopedia Mysenvaria/History/Biographies/Gods/Elemental Gods/God of {element_name}|God of {element_name}]], ")

            with open(new_template_path, "r+") as new_template_file:
                content = new_template_file.read().replace("{link_to_elements}", "".join(elements_links))
                new_template_file.seek(0)
                new_template_file.write(content)
                new_template_file.truncate()
