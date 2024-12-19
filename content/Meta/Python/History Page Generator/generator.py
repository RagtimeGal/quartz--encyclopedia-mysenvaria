import os

def generate_pages(start_date, end_date, century_template_path, decade_template_path, output_dir):
    def year_suffix(year):
        return f"{abs(year)}{' BT' if year < 0 else ' AT'}"
    
    def decade_title(decade_start):
        return f"{abs(decade_start)}s {'BT' if decade_start < 0 else 'AT'}"

    def century_title(century_start):
        if century_start == 0:
            return "1st Century AT"
        century_number = abs(century_start) // 100 + (1 if century_start > 0 else 0)
        suffix = "th"
        if 10 <= century_number % 100 <= 20:
            suffix = "th"
        elif century_number % 10 == 1:
            suffix = "st"
        elif century_number % 10 == 2:
            suffix = "nd"
        elif century_number % 10 == 3:
            suffix = "rd"
        return f"{century_number}{suffix} Century {'BT' if century_start < 0 else 'AT'}"

    def generate_decade_list(decade_start):
        return "\n".join(f"## {year_suffix(year)}\n" for year in range(decade_start, decade_start + 10))
    
    def generate_century_list(century_start):
        return "\n".join(f"## {decade_title(decade)}\n" for decade in range(century_start, century_start + 100, 10))

    def generate_links(current, is_century, is_decade):
        if is_decade:
            prev_century = (current // 100) * 100 - 100
            next_century = (current // 100) * 100 + 100
            current_century = (current // 100) * 100
            
            decade_links = f"[[Encyclopedia Mysenvaria/Indexes/History/Decades/{decade_title(current - 10)}|{decade_title(current - 10)}]], **{decade_title(current)}**, [[Encyclopedia Mysenvaria/Indexes/History/Decades/{decade_title(current + 10)}|{decade_title(current + 10)}]]"
            century_links = (
                f"[[Encyclopedia Mysenvaria/Indexes/History/Centuries/{century_title(prev_century)}|{century_title(prev_century)}]], "
                f"[[Encyclopedia Mysenvaria/Indexes/History/Centuries/{century_title(current_century)}|{century_title(current_century)}]], "
                f"[[Encyclopedia Mysenvaria/Indexes/History/Centuries/{century_title(next_century)}|{century_title(next_century)}]]"
            )
        else:
            decade_links = ", ".join(
                f"[[Encyclopedia Mysenvaria/Indexes/History/Decades/{decade_title(dec)}|{decade_title(dec)}]]"
                for dec in range(current - 10, current + 100 + 10, 10)
            )
            prev_century = current - 100
            next_century = current + 100
            century_links = (
                f"[[Encyclopedia Mysenvaria/Indexes/History/Centuries/{century_title(prev_century)}|{century_title(prev_century)}]], "
                f"**{century_title(current)}**, "
                f"[[Encyclopedia Mysenvaria/Indexes/History/Centuries/{century_title(next_century)}|{century_title(next_century)}]]"
            )

        return decade_links, century_links

    def create_directory(path):
        os.makedirs(path, exist_ok=True)

    def generate_file(path, template, replacements):
        with open(template, "r") as file:
            content = file.read()
        for placeholder, replacement in replacements.items():
            content = content.replace(placeholder, replacement)
        with open(path, "w") as file:
            file.write(content)

    # Normalize the start and end to nearest decade and century
    start_decade = (start_date // 10) * 10
    start_century = (start_date // 100) * 100
    end_decade = (end_date // 10) * 10
    end_century = (end_date // 100) * 100

    # Create separate folders for centuries and decades
    century_folder = os.path.join(output_dir, "Centuries")
    decade_folder = os.path.join(output_dir, "Decades")
    create_directory(century_folder)
    create_directory(decade_folder)

    # Timeline content
    timeline_content = []

    for year in range(start_century, end_century + 1, 100):
        century_name = century_title(year)
        timeline_content.append(f"- [[Encyclopedia Mysenvaria/Indexes/History/Centuries/{century_name}|{century_name}]]")
        
        for decade in range(year, year + 100, 10):
            decade_name = decade_title(decade)
            timeline_content.append(f"  - [[Encyclopedia Mysenvaria/Indexes/History/Decades/{decade_name}|{decade_name}]]")

    for year in range(start_decade, end_decade + 1, 10):
        print(f"Generating decade page: {decade_title(year)}")
        decade_file = os.path.join(decade_folder, f"{decade_title(year)}.md")
        
        decade_links, century_links = generate_links(year, is_century=False, is_decade=True)

        replacements = {
            "{{title}}": decade_title(year),
            "{{list}}": generate_decade_list(year),
            "{{decade_links}}": decade_links,
            "{{century_links}}": century_links,
        }

        generate_file(decade_file, decade_template_path, replacements)

    for year in range(start_century, end_century + 1, 100):
        print(f"Generating century page: {century_title(year)}")
        century_file = os.path.join(century_folder, f"{century_title(year)}.md")

        decade_links, century_links = generate_links(year, is_century=True, is_decade=False)

        replacements = {
            "{{title}}": century_title(year),
            "{{list}}": generate_century_list(year),
            "{{decade_links}}": decade_links,
            "{{century_links}}": century_links,
        }

        generate_file(century_file, century_template_path, replacements)

    # Write the timeline file
    timeline_file = os.path.join(output_dir, "Timeline.md")
    with open(timeline_file, "w") as file:
        file.write("\n".join(timeline_content))
    print(f"Timeline file generated: {timeline_file}")

# Example usage
start_date = -178
end_date = 1490
century_template_path = 'C:\\Users\\Terra\\Documents\\Github Folders\\quartz--encyclopedia-mysenvaria\\content\\Meta\\Python\\History Page Generator\\Century.md'
decade_template_path = 'C:\\Users\\Terra\\Documents\\Github Folders\\quartz--encyclopedia-mysenvaria\\content\\Meta\\Python\\History Page Generator\\Decade.md'
output_dir = 'C:\\Users\\Terra\\Documents\\Github Folders\\quartz--encyclopedia-mysenvaria\\content\\Meta\\Python\\History Page Generator\\Output'

generate_pages(start_date, end_date, century_template_path, decade_template_path, output_dir)
