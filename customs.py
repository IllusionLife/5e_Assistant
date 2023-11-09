import json

def add_new_proficiency(new_prof_name = "New Test"):
    json_file = None
    with open("Data/Sources/proficiencies.json", "r") as file:
        json_file = json.load(file)

    new_prof_id = new_prof_name.replace(" ", "_").lower()
    prof_data = {"id": new_prof_id,
                 "name": new_prof_name}

    print(json_file)
    if not any(profs.get('id') == new_prof_id for profs in json_file["proficiencies"]):
        json_file["proficiencies"].append(prof_data)
    else:
        print("Nope")
    print(json_file)

    with open("Data/Sources/proficiencies.json", "w") as outfile:
        json.dump(json_file, outfile, indent=2)
