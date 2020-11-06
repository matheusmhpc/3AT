#!/usr/bin/python3
import json
from flask_restful import Resource, Api, abort
from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from waitress import serve

app = Flask(__name__)
CORS(app)
api = Api(app)

rotas = {}

with open('database2') as json_file:
    base = json.load(json_file)

with open('mapeamento') as json_file:
    map = json.load(json_file)

infinite = 99999999999
nullobj = {"value": infinite,
           "name": None}

class minHeap:
    def __init__(self, max):
        self.max = max
        self.size = 0
        self.minheap = [nullobj] * (self.max)

    def swap(self, fpos, spos):
        self.minheap[fpos], self.minheap[spos] = self.minheap[spos], self.minheap[fpos]

    def LEFT(self, i):
        return ((i * 2))

    def RIGHT(self, i):
        return ((i * 2)+1)

    def PARENT(self, i):
        i = i - 1
        return i // 2

    def insert(self, obj):
        if self.size >= self.max:
            return

        self.minheap[self.size] = obj

        i = self.size

        self.size += 1
        while ((i != 0) and (self.minheap[i]["value"] < self.minheap[self.PARENT(i)]["value"])):
            self.swap(i, self.PARENT(i))
            i = self.PARENT(i)

    def remove(self):
        if (self.size == 0):
            return

        obj = self.minheap[0]

        self.size -= 1
        self.minheap[0] = self.minheap[self.size]
        self.minheap[self.size] = nullobj
        self.minHeapify(0)

        return obj

    def minHeapify(self, i):
        l = self.LEFT(i)
        r = self.RIGHT(i)

        if ((l <= self.size) and (self.minheap[l]["value"] < self.minheap[i]["value"])):
            menor = l
        else:
            menor = i

        if ((r <= self.size) and (self.minheap[r]["value"] < self.minheap[menor]["value"])):
            menor = r

        if (menor != i):
            self.swap(i, menor)
            self.minHeapify(menor)

    def heapifyUpdated(self, i):
        while ((i != 0) and (self.minheap[i]["value"] < self.minheap[self.PARENT(i)]["value"])):
            self.swap(i, self.PARENT(i))
            i = self.PARENT(i)

    def search(self, dest):
        i = 0
        for each in self.minheap:
            if (i >= self.size):
                return None
            if (each["name"] == dest):
                return i
            i += 1

class Data:
    def __init__(self, rotas):
        self.tam = len(rotas)
        self.antecessor = {}
        self.distancia = {}
        self.output = "inf\n"
        self.rotas = rotas

        self.heap = minHeap(self.tam)

        i = 0

        for each in rotas:
            self.distancia[each] = infinite
            self.antecessor[each] = None
            obj = {'name': each,
                   'value': infinite}
            self.heap.insert(obj)

    def djikstra(self, origin):
        self.distancia[origin] = 0

        objToInsert = {"name": origin,
                       "value": 0}

        i = self.heap.search(origin)
        self.heap.minheap[i] = objToInsert
        self.heap.heapifyUpdated(i)

        while(self.heap.size > 0):
            obj = self.heap.remove()

            name = obj['name']

            for each in self.rotas[name]:

                if ((self.distancia[name]+each["value"]) < self.distancia[each["name"]]):

                    self.distancia[each["name"]] = (self.distancia[name]+each["value"])
                    self.antecessor[each["name"]] = name

                    toUpdate = each

                    objToInsert = {"name": each["name"],
                                   "value": self.distancia[name]+each["value"]}

                    i = self.heap.search(toUpdate)
                    if (i != None):
                        self.heap.minheap[i] = objToInsert
                        self.heap.heapifyUpdated(i)


    def printroute(self, dest):

        lista = []
        distancia = self.distancia[dest]
        if (distancia == infinite):
            return {'route': None,
                   'distancia': None}

        while(dest != None):
            lista.append(dest)
            dest = self.antecessor[dest]

        i = len(lista) - 1
        j = i
        route = [None] * (len(lista))
        while(i >= 0):
            dist = 0
            if (self.distancia[lista[i]] != 0):
                dist =  self.distancia[lista[i]] - self.distancia[lista[i+1]]

            route[i] = {'name': map[lista[i]]['name'],
                        'show': map[lista[i]]['name'] + ' ('+map[lista[i]]['identificador']+')',
                        'dist': dist}
            i = i - 1
        i = j
        j = 0
        link = "https://www.google.com/maps/dir/"
        lista.reverse()
        while (j <= i):

            link = link + str(map[lista[j]]['lat']) + ',' + str(map[lista[j]]['lng']) + '/'
            j += 1
        route.reverse()
        distancia = 0
        for each in route:
            distancia += each['dist']
        retorno = {'route': route,
                   'distancia': distancia,
                   'link': link}

        return retorno

def cadAresta(base, rotas, places):
        for each in base:
            each['dist'] = each['dist'] + 1
            obj = {"name": each['dest'],
                   "value": each['dist']}

            if (each['origin'] not in places):
                places.append(each['origin'])
                rotas[each['origin']] = []

            rotas[each['origin']].append(obj)

def calcrota(rotas, origin, dest):
    grafo = Data(rotas)
    grafo.djikstra(origin)
    retorno = grafo.printroute(dest)
    return retorno

class get_options(Resource):
    def get(self):
        retorno = []
        for each in map:
            if(each != None):
                obj = {'id': each['id'],
                       'name': each['name'],
                       'show': each['name']+' ('+each['identificador']+')'}
                retorno.append(obj)
        return jsonify(retorno)

class better_route(Resource):
    def post(self):
        origin = request.json['origin']
        destination = request.json['destination']
        retorno = calcrota(rotas, origin, destination)
        return jsonify(retorno)

def main():
    global rotas
    places = []
    cadAresta(base, rotas, places)
    api.add_resource(get_options, '/options')
    api.add_resource(better_route, '/calculate')

    serve(app, host="0.0.0.0", port=8081)

if __name__ == '__main__':
    main()