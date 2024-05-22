import json
import math
from heapq import heappush, heappop

with open('2324_GI004_CA5_Cerca_dades_rutes_1.json', 'r') as file:
    data = json.load(file)

cities = {city['name']: (city['latitude'], city['longitude']) for city in data['cities']}
connections = data['connections']

graph = {city: [] for city in cities}
for conn in connections:
    graph[conn['from']].append((conn['to'], conn['distance']))

def euclidean(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

def a_star(graph, start, goal):
    open_set = []
    heappush(open_set, (0, start, [])) 
    
    g_score = {city: float('inf') for city in graph}
    g_score[start] = 0
    
    while open_set:
        _, current, path = heappop(open_set)
        
        if current == goal:
            return path + [goal]
        
        for neighbor, weight in graph[current]:
            temp_g_score = g_score[current] + weight
            if temp_g_score < g_score[neighbor]:
                g_score[neighbor] = temp_g_score
                f_score = temp_g_score + euclidean(*cities[current], *cities[neighbor])
                heappush(open_set, (f_score, neighbor, path + [current]))
    
    return []  


origin = "Sort"
destination = "L'Hospitalet de Llobregat"
shortest_path = a_star(graph, origin, destination)
print("Shortest path from", origin, "to", destination, ":", shortest_path)
