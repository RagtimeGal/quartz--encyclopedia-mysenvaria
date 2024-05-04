import os

def check_formatting(input_list):
    issues = []
    
    for index, entry in enumerate(input_list):
        parts = entry.split('; ')
        if len(parts) != 3:
            issues.append(f"Issue in entry {index + 1}: Incorrect number of semicolons.")
        else:
            name, year, description = parts
            year = year.strip()
            if not year.startswith("c. BT ") or not year[6:].isdigit():
                issues.append(f"Issue in entry {index + 1}: Incorrect year format.")
    
    if not issues:
        print("No formatting issues found.")
    else:
        print("Formatting issues:")
        for issue in issues:
            print(issue)

# Example usage
directory = r'c:\Users\Terra\Desktop\Worldbuilding\Mysenvar_Branch\Mysenvar\Meta\Python\Taxa Page Generator\\'
input_list = []

# Read the input list from list.txt file
with open(os.path.join(directory, 'list.txt'), 'r') as file:
    input_list = file.readlines()

check_formatting(input_list)
