from typing import Dict
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
    return { "error": "No se pudo registrar" }, 400
  
  @staticmethod
  def create_one_driver():
    created_by = request.json.get("created_by")

    admin = AdminModel().get_by_username(created_by).get("data")
    if not admin:
      return { "error": "admin username no existe" }
    
    username = request.json.get("username")

    driver = DriverModel().get_by_username(username).get("data")
    if driver:
      return { "error": "username ya existe" }

    default_status = "inactivo"
    password = request.json.get("password")
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    hashed_pass = bcrypt.generate_password_hash(password)

    response = DriverModel().post_one_driver(username, hashed_pass, first_name, last_name, default_status, admin["id_admin"])

    if response:
      return response
    return { "error": "no se pudo crear al driver" }
  
  @staticmethod
  def update_status_by_driver():
    username = request.json.get("username")
    status = request.json.get("status")

    response = DriverModel().update_status_by_username(status, username)

    if response["row_count"] > 0:
      return response
    return { "error": "no se actualizo el estado de ningun driver" }
  
  @staticmethod
  def create_clients():
    clients = request.json.get("clients")

    if not clients:
      return { "error": "no se enviaron clientes" }, 400
    
    place_name = "San Juan de Lurigancho, Perú"
    G = ox.graph_from_place(place_name, network_type="drive")
    
    for client in clients:
      response_client = ClientModel().post_one_client(client["name"], client["latitud"], client["longitud"])
      # print(client["latitud"], client["longitud"])
      node = ox.nearest_nodes(G, X=client["longitud"], Y=client["latitud"])
      # print(node)
      response_c_e = ClientExactModel().post_one_client_exact(response_client["last_row_id"], node)

    return { "last_row_id_client": response_client["last_row_id"], "row_count": len(clients), "last_row_id_ce": response_c_e["last_row_id"] }
  
  @staticmethod
  def rand_clients():
    origen = 10735206149
    clients = ClientExactModel().get_all_clients_coords()[0].get("data")
    data_drivers = DriverModel().get_all_actives_status()[0].get("data")
    
    if not data_drivers:
      return { "error": "no hay drivers para hacer la reparticion de rutas" }, 404
    
    if not clients:
      return { "error": "no hay clientes para generar las rutas" }, 404
    
    # eliminar registro anteriores de rutas para regenerarlas
    
    PointModel().delete_all()
    RouteModel().delete_all()

    print("Eliminé la ruta anterior")

    # continuar

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

    print("Terminé de ejecutar dijkstra para todos los clientes")


    # divide clients number by drivers number
    quantitys = [0] * drivers
    for i in range(len(clients)):
      quantitys[i % drivers] += 1
    # quantitys = quantitys[::-1] if comment = no reverse
    
    print("Terminé de repartir la cantidad de clientes a los conductores.")
    print(quantitys)

    #TODO refactor. Demora mucho.

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

    print("Terminé de repartir los clientes")

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
      response, _ = RouteModel().post_one_route(distance_driver, id_driver)
      id_route = response.get("last_row_id")
      for point in driver_path:
        PointModel().post_one_point(point, id_route)

      index = index + 1

    return { "exito": "Rutas generadas con exitosamente" }, 200

  @staticmethod
  def get_all_drivers():
    response = DriverModel().get_all_without_password()
    if response[0]["data"]:
      return response
    return { "error": "No se pudo obtener a los conductores" }, 400

  @staticmethod
  def get_all_clients():
    response = ClientModel().get_all_clients()
    if response[0]["data"]:
      return response
    return { "error": "No se pudo obtener a los clientes" }, 400
  
  @staticmethod
  def delete_driver_by_id(id_driver):
    response = DriverModel().delete_by_id(id_driver)
    return response
  
  @staticmethod
  def get_all_routes():
    drivers = DriverModel().get_all_without_password()[0]["data"]

    response: list[Dict] = []

    for driver in drivers:
      route = RouteModel().get_by_id_driver(driver["id_driver"])[0]["data"]
      route_segment = {}
      if route:
        route_segment["route"] = route[0]
        route_segment["route"]["driver"] = driver
        points = PointModel().get_by_id_route(route[0]["id_route"])[0]["data"]
        route_segment["route"]["points"] = points
        response.append(route_segment)

    return { "data": response }
  
  @staticmethod
  def get_info_admin_by_id(id_admin):
    response = AdminModel().get_by_id(id_admin)
    print(response)
    if not response["data"]:
      return { "error": "no se encuentra al usuario administrador" }, 404
    return { "data": response }, 200
  
  @staticmethod
  def rand():
    origen = 10735206149
    clients = ClientExactModel().get_all_clients_coords()[0].get("data")
    data_drivers = DriverModel().get_all_actives_status()[0].get("data")
    
    if not data_drivers:
      return { "error": "no hay drivers para hacer la reparticion de rutas" }, 404
    
    if not clients:
      return { "error": "no hay clientes para generar las rutas" }, 404
    
    PointModel().delete_all()
    RouteModel().delete_all()
    
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


    quantitys = [0] * drivers
    for i in range(len(clients)):
      quantitys[i % drivers] += 1

    all_distances = { node: {} for node in all_nodes}

    # create all_distances
    for i in range(0, len(all_nodes)):
      for j in range(0, len(all_nodes)):
        if all_nodes[i] != all_nodes[j]:
          dict_distances = all_distances_by_nodes[all_nodes[i]][1]
          distance = dict_distances[all_nodes[j]]
          all_distances[all_nodes[i]][all_nodes[j]] = distance
          all_distances[all_nodes[j]][all_nodes[i]] = distance

    # eliminar la distancia a origen desde cualquier nodo cliente
    for c in client_nodes:
      if origen in all_distances[c]:
        del all_distances[c][origen]

    # calcular la distancia mínima eligiendo el nodo más cercano en cada iteración
    path_results = []
    visited = set()
    for q in quantitys:
      all_d = all_distances.copy()
      partial_path = [origen]
      current_node = origen
      for i in range(0, q):
        # delete visited nodes from all_d
        for node in visited:
          if node in all_d[current_node]:
            del all_d[current_node][node]
        # select the min distance node
        if not all_d[current_node]:
          partial_path.append(current_node)
          break
        point = min(all_d[current_node], key=all_d[current_node].get)
        partial_path.append(point)
        visited.add(point)
        current_node = point

      partial_path.append(origen)
      path_results.append(partial_path)

    # reconstruir los caminos
    all_full_paths = []
    for path in path_results:
      p = []
      p.append(origen)
      distance = 0
      for i in range(0, len(path) - 1):
        previous_nodes, _ = all_distances_by_nodes[path[i]]
        path_segment = GraphRoad.reconstruct_path(previous_nodes, path[i + 1])[1:]
        for point in path_segment:
          p.append(point)
        distance += all_distances_by_nodes[path[i]][1][path[i + 1]]
      distance += all_distances_by_nodes[path[-2]][1][origen]
      all_full_paths.append((p, distance))

    # agregar a la base de datos
    index = 0
    for driver_path, distance_driver in all_full_paths:
      id_driver = data_drivers[index]["id_driver"]
      response, _ = RouteModel().post_one_route(distance_driver, id_driver)
      id_route = response.get("last_row_id")
      for point in driver_path:
        PointModel().post_one_point(point, id_route)

      index = index + 1
    print(quantitys)
    return { "message": "Hello World" }