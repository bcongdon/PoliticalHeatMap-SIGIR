import json, os

path_to_json = 'output/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

stateMap = {"Hawaii":"HI",
            "Texas":"TX",}

for js in json_files:
    with open(os.path.join(path_to_json, js)) as json_file:
        parsed = json.load(json_file)
