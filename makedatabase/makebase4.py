import json

with open('database2') as json_file:
    data = json.load(json_file)
i = 0

for each in data:
    if(each['origin'] == 1):
        print(i, each)