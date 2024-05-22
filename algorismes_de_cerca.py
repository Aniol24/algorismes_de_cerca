import json
import math
from heapq import heappush, heappop

with open('2324_GI004_CA5_Cerca_dades_rutes_1.json', 'r') as file:
    data = json.load(file)

cities = {city['name']: (city['latitude'], city['longitude']) for city in data['cities']}
connections = data['connections']

graph = {city: [] for city in cities}
for conn in connections:
    graph[conn['from']].append((conn['to'], conn['distance'], conn['duration']))

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

        for neighbor, distance, duration in graph[current]:
            temp_g_score = g_score[current] + distance
            if temp_g_score < g_score[neighbor]:
                g_score[neighbor] = temp_g_score
                f_score = temp_g_score + euclidean(*cities[current], *cities[neighbor])
                heappush(open_set, (f_score, neighbor, path + [current]))
    
    return []

# RESTRICCIONES
MAX_DISTANCE = 200000
MAX_DURATION_STAGE = 10400

# h1
def select_most_constraining_variable(unassigned_vars):
    # Nosotros entendemos como variable más restringida la variable no visitada con el menor
    # número de vecinos.
    return min(unassigned_vars, key=lambda var: len(graph.get(var, [])))
# h2
def select_least_constraining_value(var):
    # Para encontrar la variable menos restringida,
    # hemos ordenado las variables de menor a mayor según el número de restricciones que cumplen.
    return sorted(graph.get(var, []), key=lambda x: len(graph.get(x[0], [])))

def is_valid_route(route):
    total_distance = 0
    for i in range(len(route) - 1):
        for neighbor in graph[route[i]]:
            if neighbor[0] == route[i + 1]:
                total_distance += neighbor[1]
                if total_distance > MAX_DISTANCE or neighbor[2] > MAX_DURATION_STAGE:
                    return False
    return True

def backtracking(current_route, end, unassigned_vars):
    current_city = current_route[-1]
    if current_city == end:
        return current_route

    if current_city in unassigned_vars:
        unassigned_vars.remove(current_city)

    if unassigned_vars:
        next_city = select_most_constraining_variable(unassigned_vars)
        possible_values = select_least_constraining_value(next_city)

        for value in possible_values:
            if value[0] not in current_route:
                next_route = current_route + [value[0]]
                if is_valid_route(next_route):
                    result = backtracking(next_route, end, unassigned_vars)
                    if result:
                        return result

    if current_city not in unassigned_vars:
        unassigned_vars.add(current_city)
    return None

def csp(start, end):
    unassigned_vars = set(cities.keys())
    unassigned_vars.remove(start)
    return backtracking([start], end, unassigned_vars)

def calculate_total_distance_and_duration(route):
    total_distance = 0
    total_duration = 0
    for i in range(len(route) - 1):
        for neighbor in graph[route[i]]:
            if neighbor[0] == route[i + 1]:
                total_distance += neighbor[1]
                total_duration += neighbor[2]
    print(f"Distancia total: {total_distance}, Duración total: {total_duration}")

# A*

origin = "Sort"
destination = "L'Hospitalet de Llobregat"
shortest_path = a_star(graph, origin, destination)
print("Shortest path from", origin, "to", destination, ":", shortest_path)

# CSP

start_city = "Sort"
end_city = "L'Hospitalet de Llobregat"
solution = csp(start_city, end_city)

if solution:
    print(f"Ruta encontrada de {start_city} a {end_city}: {solution}")
    calculate_total_distance_and_duration(solution)
else:
    print(f"No se encontró ninguna ruta de {start_city} a {end_city} que cumpla con las restricciones.")