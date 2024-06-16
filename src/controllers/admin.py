from models import AdminModel, DriverModel, ClientModel, ClientExactModel, ModelArista, ModelNodo, PointModel, RouteModel
from flask import request
from flask_bcrypt import  Bcrypt
from graph.Graph import Graph as GraphRoad

import osmnx as ox
import networkx as nx
from itertools import permutations

bcrypt = Bcrypt()

class AdminController:
  @staticmethod
  def create_one_admin():
    username = request.json.get("username")
    password = request.json.get("password")
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    hashed_pass = bcrypt.generate_password_hash(password)
    response = AdminModel().post_one_admin(username, hashed_pass, first_name, last_name)
    if response:
      return response
    return { "Error": "No se pudo registrar" }, 400
  
  @staticmethod
  def create_one_driver():
    created_by = request.json.get("created_by")

    admin = AdminModel().get_by_username(created_by).get("data")
    if not admin:
      return { "Error": "admin username no existe" }
    
    username = request.json.get("username")

    driver = DriverModel().get_by_username(username).get("data")
    if driver:
      return { "Error": "username ya existe" }

    default_status = "inactivo"
    password = request.json.get("password")
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    hashed_pass = bcrypt.generate_password_hash(password)

    response = DriverModel().post_one_driver(username, hashed_pass, first_name, last_name, default_status, admin["id_admin"])

    if response:
      return response
    return { "Error": "no se pudo crear al driver" }
  
  @staticmethod
  def update_status_by_driver():
    username = request.json.get("username")
    status = request.json.get("status")

    response = DriverModel().update_status_by_username(status, username)

    if response["row_count"] > 0:
      return response
    return { "Error": "no se actualizo el estado de ningun driver" }
  
  @staticmethod
  def create_clients():
    clients = request.json.get("clients")

    if not clients:
      return { "Error": "no se enviaron clientes" }, 400
    
    place_name = "San Juan de Lurigancho, Perú"
    G = ox.graph_from_place(place_name, network_type="drive")
    
    for client in clients:
      response_client = ClientModel().post_one_client(client["name"], client["latitud"], client["longitud"])
      # print(client["latitud"], client["longitud"])
      node = ox.nearest_nodes(G, X=client["longitud"], Y=client["latitud"])
      # print(node)
      response_c_e = ClientExactModel().post_one_client_exact(response_client["last_row_id"], node)

    return { "last_row_id_client": response_client["last_row_id"], "row_count": len(clients), "last_row_id_ce": response_c_e["last_row_id"] }
  
  # @staticmethod
  # def randomize():
  #   data_clients, _ = ClientExactModel().get_all_clients_coords()
  #   clients = data_clients.get("data")
  #   if not clients:
  #     return { "Error": "No hay clientes" }, 400

  #   client_nodes = [client["id_nodo"] for client in clients]

  #   data_drivers, _ = DriverModel().get_all_actives_status()
  #   drivers = data_drivers.get("data")

  #   if not drivers:
  #     return { "Error": "No hay conductores" }, 400
    
  #   drivers_quantity = len(drivers)

  #   quantitys = [0] * drivers_quantity
  #   for i in range(len(clients)):
  #     quantitys[i % drivers_quantity] += 1

  #   quantitys = quantitys[::-1]

  #   nodes = ModelNodo().get_all_nodo().get("data")
  #   arists = ModelArista().get_all_arists().get("data")

  #   Graph = nx.Graph()

  #   for node in nodes:
  #     Graph.add_node(node["id_nodo"])

  #   for arist in arists:
  #     Graph.add_edge(arist["origen"], arist["destino"], weight=arist["distancia"])

  #   # search paths
  #   all_paths = []
  #   origen = 10735206149

  #   current_clients = client_nodes.copy()

  #   print(quantitys, current_clients)

  #   print("inicio: ", current_clients)

  #   for q in quantitys:
  #     path, cost = GraphRoad.find_shortest_path_via_clients(Graph, origen, current_clients, q)
  #     if not path:
  #       break
  #     all_paths.append((path, cost))

  #     visited_nodes = set(path)
  #     current_clients = [client for client in current_clients if client not in visited_nodes]
    
  #   print(all_paths)

  #   return { "Hola": "Hola Mundo" }
  
  @staticmethod
  def rand_clients():
    origen = 10735206149
    clients = ClientExactModel().get_all_clients_coords()[0].get("data")
    data_drivers = DriverModel().get_all_actives_status()[0].get("data")
    
    if not data_drivers:
      return { "Error": "no hay drivers para hacer la reparticion de rutas" }, 404
    
    if not clients:
      return { "Error": "no hay clientes para generar las rutas" }, 404
    
    drivers = len(data_drivers)


    client_nodes = [client["id_nodo"] for client in clients]

    # Graph
    nodes = ModelNodo().get_all_nodo().get("data")
    arists = ModelArista().get_all_arists().get("data")

    G = nx.Graph()

    for node in nodes:
      G.add_node(node["id_nodo"])

    for arist in arists:
      G.add_edge(arist["origen"], arist["destino"], weight=arist["distancia"])


    all_nodes = [origen] + client_nodes
    all_distances_by_nodes = {}

    for node in all_nodes:
      all_distances_by_nodes[node] = GraphRoad.dijkstra(G, node, client_nodes)

    # divide clients number by drivers number
    quantitys = [0] * drivers
    for i in range(len(clients)):
      quantitys[i % drivers] += 1
    quantitys = quantitys[::-1]

    all_paths = []
    all_full_paths = []
    # find min paths
    for q in quantitys:
      path, min_distance = GraphRoad.min_path_via_clients(all_distances_by_nodes, client_nodes, origen, q)
      # delete clients mapped
      for i in range (0, len(path) - 1):
        client_nodes.remove(path[i + 1])
      # add the origin to the end of the path for the return
      path = path + (origen,)
      all_paths.append((path, min_distance))

    # reconstruct paths and distances
    for path, _ in all_paths:
      p = []
      p.append(origen)
      distance = _
      for i in range (0, len(path) - 1):
        previous_nodes, _ = all_distances_by_nodes[path[i]]
        path_segment = GraphRoad.reconstruct_path(previous_nodes, path[i + 1])[1:]
        for point in path_segment:
          p.append(point)
      distance += all_distances_by_nodes[path[-2]][1][origen]
      all_full_paths.append((p, distance))

    index = 0
    for driver_path, distance_driver in all_full_paths:
      id_driver = data_drivers[index]["id_driver"]
      print(id_driver)
      response, _ = RouteModel().post_one_route(distance_driver, data_drivers[index]["id_driver"])
      id_route = response.get("last_row_id")
      for point in driver_path:
        PointModel().post_one_point(point, id_route)

      index = index + 1

    return { "Exito": "Rutas generadas con exitosamente" }, 200

  @staticmethod
  def get_all_drivers():
    response = DriverModel().get_all_without_password()
    if response[0]["data"]:
      return response
    return { "Error": "No se pudo obtener a los conductores" }, 400

  @staticmethod
  def get_all_clients():
    response = ClientModel().get_all_clients()
    if response[0]["data"]:
      return response
    return { "Error": "No se pudo obtener a los clientes" }, 400
  
  @staticmethod
  def delete_driver_by_id(id_driver):
    response = DriverModel().delete_by_id(id_driver)
    return response