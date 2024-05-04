import json
import random

def load_animals(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def select_group(data):
    groups = data["group"]
    return random.choice(groups)

def select_animals_from_group(data, group):
    animals = [animal for animal in data["animals"] if group in animal["groups"]]
    return random.sample(animals, 2)

def main():
    data = load_animals("c:\\Users\\Terra\\Desktop\\Worldbuilding\\Mysenvar_Branch\\Mysenvar\\Meta\\Python\\Animal Generator\\animals.json")
    with open("c:\\Users\\Terra\\Desktop\\Worldbuilding\\Mysenvar_Branch\\Mysenvar\\Meta\\Python\\Animal Generator\\animals.txt", "w") as output_file:
        for _ in range(500):
            group = select_group(data)
            output_file.write("Selected Group: {}\n".format(group))
            animal1, animal2 = select_animals_from_group(data, group)
            output_file.write("Animal 1: {}\n".format(animal1["name"]))
            output_file.write("Animal 2: {}\n".format(animal2["name"]))
            output_file.write("\n")

if __name__ == "__main__":
    main()