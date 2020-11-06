import json
import threading
import geopy.distance
import requests
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

with open('data_to_process') as json_file:
    data = json.load(json_file)
token = ""
arestas = []
linkmultiplecordenate = "https://www.google.com/maps/dir/-8.061036099999999,-34.871297/-8.086053999999999,-34.8947486/-8.037011099999999,-34.9125792"

i = 0
def capture_data(arestas, origin, dest):
    pass
i = 0
for each in data:

    model = [each['lat'], each['lng']]
    for cada in data:
        tocheck = [cada['lat'], cada['lng']]
        if (cada != each):
            dist = distance(model, tocheck)
            #dist = geopy.distance.distance(model, tocheck).km
            if(dist < 3):
                i += 1
                link = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + str(each['lat']) + ',' + str(each['lng']) + "&destinations=" + str(cada['lat']) + ',' + str(cada['lng']) + "&key="+token
                response = requests.get(link)
                dados = response.json()
                linkdist = dados['rows'][0]['elements'][0]['distance']['value']
                obj = {'origin': each['id'],
                       'dest': cada['id'],
                       'geometry_distance': dist,
                       'dist': linkdist}
                print(obj)
                arestas.append(obj)

print(i)
print(i)
with open('database3', 'w') as outfile:
    json.dump(arestas, outfile)
