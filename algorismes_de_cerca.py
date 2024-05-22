import json
import math
from heapq import heappush, heappop
import networkx as nx
import matplotlib.pyplot as plt

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


def visualize_graph_with_path(path, src, dest, alg, save_path):
    G = nx.DiGraph()

    for city, coord in cities.items():
        G.add_node(city, pos=coord)
    for city, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(city, neighbor[0], weight=neighbor[1])

    pos = nx.spring_layout(G, seed=42)  # Disposición del grafo
    plt.figure(figsize=(12, 8))

    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2.5, edge_color='r')

    nx.draw_networkx_labels(G, pos, font_size=10)

    plt.title(f"Algoritmo {alg} entre {src} y {dest}")
    plt.savefig(save_path)
    plt.close()

# A*

origin = "Sort"
destination = "L'Hospitalet de Llobregat"
shortest_path = a_star(graph, origin, destination)
print("Shortest path from", origin, "to", destination, ":", shortest_path)
save_path = f"visualizacion/A_{origin}_{destination}"
visualize_graph_with_path(shortest_path, origin, destination, "A*", save_path)

# CSP

start_city = "Sort"
end_city = "L'Hospitalet de Llobregat"
solution = csp(start_city, end_city)

if solution:
    print(f"Ruta encontrada de {start_city} a {end_city}: {solution}")
    calculate_total_distance_and_duration(solution)
    save_path = f"visualizacion/csp_{start_city}_{end_city}"
    visualize_graph_with_path(solution, start_city, end_city, "CSP", save_path)
else:
    print(f"No se encontró ninguna ruta de {start_city} a {end_city} que cumpla con las restricciones.")