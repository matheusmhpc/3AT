import json
from math import sin, cos, sqrt, atan2, radians


def distance(p1, p2):
    # Raio aproximado da terra
    R = 6371.0

    lat1 = radians(p1[0])
    lon1 = radians(p1[1])
    lat2 = radians(p2[0])
    lon2 = radians(p2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

with open('cordenates') as json_file:
    data = json.load(json_file)

model = [data[0]['lat'], data[0]['lng']]
print(data[0])

tosave = []

for each in data:
    """tocheck = [each['lat'], each['lng']]
    dist = distance(model, tocheck)
    if (dist > 200):
        print(each)"""
    idf2 = ""
    for cada in each['address_components']:
        if ('sublocality_level_1' in cada['types']):
            idf2 = cada['long_name']

    obj = {'lat': each['lat'],
           'lng': each['lng'],
           'id': each['id'],
           'identificador': idf2}
    tosave.append(obj)

with open('data_to_process', 'w') as outfile:
    json.dump(tosave, outfile)
