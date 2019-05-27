import json

filename = "Source_052619_000000006822_keypoints.json"

with open(filename) as json_file:  
    data = json.load(json_file)
