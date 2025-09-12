import json

# Load JSON input
with open(r"C:\Users\Terra\Documents\Github Folders\quartz--encyclopedia-mysenvaria\content\Meta\Python\json to twine\input.json", "r") as f:
    data = json.load(f)

special_words = set(word.lower() for word in data.get("special words", []))

output = []
output.append("switch (input) {")

for context in data["contexts"]:
    context_name = context["name"]
    context_bg = context.get("background")

    for reply in context["replies"]:
        player_input = reply["player"].lower()
        response_text = reply["reply"]
        context_change = reply.get("context_change")

        # Highlight special words in the response
        # Highlight special words in the response
        words = response_text.split()
        highlighted = []
        for word in words:
            stripped = word.strip(".,!?()[]{}")
            if stripped.lower() in special_words:
                highlighted.append(f'<span style=\\"color:aqua\\">{word}</span>')
            else:
                highlighted.append(word)
        formatted_response = " ".join(highlighted)
        
        # Start case block
        output.append(f"  case \"{player_input}\":")

        # Context change
        if context_change:
            output.append(f"    SugarCube.State.variables.context = \"{context_change}\";")

        # Background change
        if context_change:
            for c in data["contexts"]:
                if c["name"] == context_change and c.get("background"):
                    output.append(f"    changeBackground(\"{c['background']}\");")
                    break

        # Context match conditional
        output.append(f"    if (context === \"{context_name}\") {{")
        output.append(f"      response = \"{formatted_response}\";");
        output.append("      break;")
        output.append("    }")
        output.append("    break;")

output.append("  default:")
output.append("    response = \"I do not understand that question.\";")
output.append("    break;")
output.append("}")

output_path = r"C:\Users\Terra\Documents\Github Folders\quartz--encyclopedia-mysenvaria\content\Meta\Python\json to twine\output.txt"

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print(f"Conversion complete! Output saved to: {output_path}")
