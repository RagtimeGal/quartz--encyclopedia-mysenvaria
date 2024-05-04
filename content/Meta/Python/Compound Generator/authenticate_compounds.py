import json
import pubchempy as pcp

def read_compounds_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            compounds = data.get("compounds", [])
        return compounds
    except Exception as e:
        print(f"Error reading compounds from JSON: {e}")
        return []

def check_compounds(compounds):
    missing_compounds = []
    for compound in compounds:
        # Check if the compound exists in PubChem
        result = pcp.get_compounds(compound, 'name')
        if not result:
            missing_compounds.append(compound)
    return missing_compounds

def main():
    # Directory and file name for the JSON file
    file_path = 'c:\\Users\\Terra\\Desktop\\Worldbuilding\\Mysenvar_Branch\\Mysenvar\\Meta\\Python\\Compound Generator\\library.json'

    # Read compounds from JSON file
    compounds_to_check = read_compounds_from_json(file_path)

    # Check compounds
    missing = check_compounds(compounds_to_check)

    if missing:
        print("The following compounds are missing from PubChem:")
        for compound in missing:
            print(compound)
    else:
        print("All compounds are present in PubChem!")

if __name__ == "__main__":
    main()
