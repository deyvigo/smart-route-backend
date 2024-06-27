import heapq
from itertools import permutations

class Graph:
  @staticmethod
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

      # if len(visited_clients) >= len(clients):
      #   break

    return previous_nodes, distances
  
  @staticmethod
  def reconstruct_path(previous_nodes, end):
    path = []
    current_node = end
    while current_node is not None:
      path.append(current_node)
      current_node = previous_nodes[current_node]

    path.reverse()
    return path

  @staticmethod
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
        previous_nodes, distances = Graph.dijkstra(G, current_node, clients)
        path_segment = Graph.reconstruct_path(previous_nodes, origen, client)
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
  
  @staticmethod
  def min_path_via_clients(all_distances_by_nodes, clients, origen, quantity):
    permutated_clients = permutations(clients, quantity)
    min_distance = float("infinity")

    for perm in permutated_clients:
      distance = 0
      possible_path = (origen,) + perm
      for i in range(0, len(possible_path) - 1):
        node = possible_path[i]
        next = possible_path[i + 1]
        _, distances = all_distances_by_nodes[node]
        distance += distances[next]
      
      if distance < min_distance:
        min_distance = distance
        path = possible_path

    return path, min_distance