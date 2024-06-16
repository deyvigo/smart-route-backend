from flask import Flask, request
from flask_cors import CORS
import heapq
import networkx as nx
import osmnx as ox
from models.nodo import ModelNodo
from models.arista import ModelArista
from itertools import permutations

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from routes import admin_blueprint, driver_blueprint, login_blueprint

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "ada-smart-router"
jwt = JWTManager(app)

bcrypt = Bcrypt(app)
CORS(app)

app.register_blueprint(admin_blueprint)
app.register_blueprint(driver_blueprint)
app.register_blueprint(login_blueprint)


# #######################################################################
@app.route("/clients", methods=["POST"])
def search_clients_in_graph():
  data = request.get_json()

  return { "data": "hola" }

def dijkstra (G, origen, num_nodes, clients):
  distances = {node: float("infinity") for node in G}
  distances[origen] = 0
  priority_queue = [(0, origen)]
  visited = set()
  
  visited_clients = set()
  clients_set = set(clients)

  previous_nodes = {node: None for node in G}

  while priority_queue:
    current_distance, current_node = heapq.heappop(priority_queue)

    if current_distance > distances[current_node]:
      continue

    visited.add(current_node)

    if current_node in clients_set:
      visited_clients.add(current_node)

    # if len(visited_clients) == num_nodes + 1:
    #   break

    for neighbor, attributes in G[current_node].items():
      weight = attributes["weight"]
      distance = current_distance + weight

      if distance < distances[neighbor]:
        distances[neighbor] = distance
        previous_nodes[neighbor] = current_node
        heapq.heappush(priority_queue, (distance, neighbor))

  return distances, previous_nodes

def shortest_path(G, previous_nodes, distances, num_nodes, clients):
  valid_paths = []

  # for node, prev_node in previous_nodes.items():
  #   if prev_node is None:
  #     continue
    
  #   path = [node]
  #   current_node = node

  #   while previous_nodes[current_node] is not None:
  #     path.append(previous_nodes[current_node])
  #     current_node = previous_nodes[current_node]

  #   if len(set(path) & set(clients)) >= num_nodes:
  #     valid_paths.append((path[::-1], distances[node]))

  for node in clients:
    if node not in previous_nodes:
      continue

    path = [node]
    current_node = node

    while previous_nodes[current_node] is not None:
      path.append(previous_nodes[current_node])
      current_node = previous_nodes[current_node]

    print(node)
    for n in path:
      print({ "id": n, "x": G.nodes[n]["x"], "y": G.nodes[n]["y"] })

    if len(set(path) & set(clients)) >= num_nodes:
      valid_paths.append((path[::-1], distances[node]))

  if not valid_paths:
    return None
  
  shortest_path, _ = min(valid_paths, key=lambda x: x[1])
  return shortest_path

@app.route("/path", methods=["POST"])
def search_path():
  data = request.get_json().get("clients")
  clients = [ {"latitud": c["latitud"], "longitud": c["longitud"]} for c in data ]

  nodes = ModelNodo().get_all_nodo().get("data")
  arists = ModelArista().get_all_arists().get("data")

  place_name = "San Juan de Lurigancho, Perú"
  G = ox.graph_from_place(place_name, network_type="drive")

  client_nodes = []

  client_array = []

  for client in clients:
    client_node = ox.nearest_nodes(G, X=client["longitud"], Y=client["latitud"])
    client = {"id": client_node, "latitud": G.nodes[client_node]['y'], "longitud": G.nodes[client_node]['x']}
    client_array.append({"id": client_node, "latitud": G.nodes[client_node]['y'], "longitud": G.nodes[client_node]['x']})
    client_nodes.append(client["id"])

  print("clientes:", client_array)

  Graph = nx.Graph()

  for node in nodes:
    Graph.add_node(node["id"])

  for arist in arists:
    Graph.add_edge(arist["origen"], arist["destino"], weight=arist["distancia"])

  # TODO dividir los clientes en cantidades iguales

  d_cant = 2 # cantidad de conductores

  quantitys = [0] * d_cant
  for i in range(len(client_nodes)):
    quantitys[i % d_cant] += 1

  quantitys = quantitys[::-1]

  print(len(client_nodes))
  print(quantitys)
  print(quantitys[1])
  print("origen:", 10735206149)
  print("###############")

  # TODO calcular el camino minimo y hacer un loop hasta terminar
  distances, previous_nodes = dijkstra(Graph, 10735206149, quantitys[1], client_nodes) # Setear el origen || 3 incluye al origen
  path = shortest_path(G, previous_nodes, distances, quantitys[1], client_nodes)

  path_array = []

  if path:
    for p in path:
      path_array.append({ "id": p, "x": G.nodes[p]["x"], "y": G.nodes[p]["y"] })
    print("path:", path_array)
  else:
    print("path:", "no path")






  # G = nx.Graph()
  # G.add_node("0")
  # G.add_node("1")
  # G.add_node("2")
  # G.add_node("3")
  # G.add_node("4")
  # G.add_node("5")
  # G.add_node("6")
  # G.add_node("7")
  # G.add_node("8")

  # G.add_edge("0", "1", weight=4)
  # G.add_edge("0", "7", weight=8)
  # G.add_edge("1", "7", weight=11)
  # G.add_edge("1", "2", weight=8)
  # G.add_edge("7", "8", weight=7)
  # G.add_edge("7", "6", weight=1)
  # G.add_edge("8", "6", weight=6)
  # G.add_edge("2", "8", weight=2)
  # G.add_edge("2", "5", weight=4)
  # G.add_edge("2", "3", weight=7)
  # G.add_edge("6", "5", weight=2)
  # G.add_edge("3", "5", weight=14)
  # G.add_edge("3", "4", weight=9)
  # G.add_edge("5", "4", weight=10)

  # distances, previous_nodes = dijkstra(G, "0", 4)
  # path = shortest_path(previous_nodes, distances, 4)
  # for p in path:
  #   print(p)

  # return { "data": client_nodes }
  return { "saludo": path }
  
@app.route("/hello", methods=["GET"])
def hello():
  ModelNodo().get_all_nodo()
  return { "saludo": "Hello World" }

@app.route("/randomize", methods=["POST"])
def randomize_client():

  def dijkstra(G, origen, clients):
    distances = {node: float("infinity") for node in G}
    distances[origen] = 0
    priority_queue = [(0, origen)]
    previous_nodes = {node: None for node in G}

    clients = set(clients)
    visited_clients = set()

    while priority_queue:
      current_distance, current_node = heapq.heappop(priority_queue)
      if current_distance > distances[current_node]:
        continue

      if current_node in clients:
        visited_clients.add(current_node)

      for neighbor, attributes in G[current_node].items():
        weight = attributes["weight"]
        distance = current_distance + weight

        if distance < distances[neighbor]:
          distances[neighbor] = distance
          previous_nodes[neighbor] = current_node
          heapq.heappush(priority_queue, (distance, neighbor))

      if len(visited_clients) >= len(clients):
        break

    return previous_nodes, distances
  

  def reconstruct_path(previous_nodes, start, end):
    path = []
    current_node = end
    while current_node is not None:
      path.append(current_node)
      current_node = previous_nodes[current_node]

    path.reverse()
    return path

  def find_shortest_path_via_clients(G, origen, clients, num_clients):
    min_path = None
    min_cost = float("infinity")

    clients_permutations = permutations(clients, num_clients)

    for perm in clients_permutations:
      full_path = []
      total_cost = 0
      current_node = origen

      perm = (origen,) + perm

      for i, client in enumerate(perm):
        previous_nodes, distances = dijkstra(G, current_node, clients)
        path_segment = reconstruct_path(previous_nodes, origen, client)
        if not path_segment:
          total_cost = float("infinity")
          break

        full_path += path_segment[:-1] if i < len(perm) - 1 else path_segment
        total_cost += distances[client]
        current_node = client

      if total_cost < min_cost:
        min_cost = total_cost
        min_path = full_path

    return min_path, min_cost


    # for perm in clients_permutations:

  ###########################################################################
  data = request.get_json().get("clients")
  clients = [ {"latitud": c["latitud"], "longitud": c["longitud"]} for c in data ]

  nodes = ModelNodo().get_all_nodo().get("data")
  arists = ModelArista().get_all_arists().get("data")

  Graph = nx.Graph()

  for node in nodes:
    Graph.add_node(node["id"])

  for arist in arists:
    Graph.add_edge(arist["origen"], arist["destino"], weight=arist["distancia"])

  place_name = "San Juan de Lurigancho, Perú"
  G = ox.graph_from_place(place_name, network_type="drive")

  client_nodes = []

  for client in clients:
    client_node = ox.nearest_nodes(G, X=client["longitud"], Y=client["latitud"])
    client = {"id": client_node, "latitud": G.nodes[client_node]['y'], "longitud": G.nodes[client_node]['x']}
    client_nodes.append(client["id"])

  d_cant = 2 # cantidad de conductores

  quantitys = [0] * d_cant
  for i in range(len(client_nodes)):
    quantitys[i % d_cant] += 1

  quantitys = quantitys[::-1]

  print(quantitys)
  all_paths = []

  # {'id': 10735206149, 'x': -76.9996855, 'y': -11.981124},
  origen = 10735206149

  current_clients = client_nodes.copy()

  print("inicio: ", current_clients)

  for q in quantitys:
    path, cost = find_shortest_path_via_clients(Graph, origen, current_clients, q)
    if not path:
      break
    all_paths.append((path, cost))
    print("intermedio:", current_clients)
    visited_nodes = set(path)
    current_clients = [client for client in current_clients if client not in visited_nodes]
    print("final:", current_clients)

  print("hola")
  print(all_paths)

  for (path, cost) in all_paths:
    print("distance:", cost)
    for point in path:
      print({ "id": point, "x": G.nodes[point]["x"], "y": G.nodes[point]["y"] })

  return { "saludo": "randomize" }

if __name__ == "__main__":
  app.run(debug=True)