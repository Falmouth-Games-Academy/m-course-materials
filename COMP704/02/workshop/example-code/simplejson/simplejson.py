import json

name = 'dave'
score = 100

data_to_send = {"name": name, "score": score }

json_data = json.dumps(data_to_send)

print(json_data)

data_received = json.loads(json_data)

print(data_received)


list = []
list.append(5)
list.append('apple')

json_data = json.dumps(list)
print(json_data)

dict = {}
dict['apple'] = 'fruity'
dict['potato'] = 'veggie'
dict['tomato'] = 'tomatoie'

json_data = json.dumps(dict)

print(json_data)

