import json
with open('details.json') as json_data_file:
    data = json.load(json_data_file)
print(type(data))
print(data['devashish']["username"])
print(data['devashish']["pass"])
