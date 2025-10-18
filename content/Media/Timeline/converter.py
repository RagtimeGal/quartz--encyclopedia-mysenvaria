import xml.etree.ElementTree as ET

def get_text(element, tag):
    child = element.find(tag)
    return child.text if child is not None else ''

def convert_timeline_to_mermaid(xml_file, mermaid_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    events = []

    # Parse events
    for event in root.find('events'):
        start = get_text(event, 'start')
        title = get_text(event, 'text')
        
        # Adding event to the list
        events.append(f'    {start} : {title}')

    # Create Mermaid timeline syntax
    mermaid_data = "%%{init: { 'logLevel': 'debug', 'theme': 'neutral' } }%%\n"
    mermaid_data += "timeline\n"
    for event in events:
        mermaid_data += f'{event}\n'

    # Write to Mermaid file
    with open(mermaid_file, 'w') as f:
        f.write(mermaid_data)

# Use raw strings (prefix with r) or double backslashes for file paths
convert_timeline_to_mermaid(r'C:\Users\Terra\Documents\Worldbuilding\Mysenvar_Branch\Mysenvar\Meta\Timeline\Mysenvarn.timeline', 
                            r'C:\Users\Terra\Documents\Worldbuilding\Mysenvar_Branch\Mysenvar\Meta\Timeline\Mysenvarn.mermaid')
