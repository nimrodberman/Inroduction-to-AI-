from typing import List, Dict
from typing import List


class WorldVertex:
    def __init__(self, v_id):
        self.v_id = v_id
        self.neighbors: List[List[int, int]] = []

    def add_neighbor(self, v_id, weight):
        self.neighbors.append([v_id, weight])

    def __str__(self):
        return str(self.v_id) + " " + str(self.neighbors)


class WorldGraph:
    def __init__(self):
        self.vertices: Dict = {}
        self.edges: Dict = {}

    def add_vertex(self, vertex):
        self.vertices[vertex.v_id] = vertex

    def get_vertex(self, v_id):
        if int(v_id) in list(self.vertices.keys()):
            return self.vertices[v_id]

    def from_edges_to_vertices(self, edges_path):
        vertices = []
        for i in range(len(edges_path)):
            if i == len(edges_path) - 1:
                e = self.edges[int(edges_path[i])]
                vertices.append(e[0])
                vertices.append(e[1])
            else:
                e = self.edges[int(edges_path[i])]
                vertices.append(e[0])

        return vertices

    def find_all_paths(self, start: int, end: int) -> List[List[int]]:
        def dfs(vertex, end, path, visited, all_paths):
            if vertex.v_id == end:
                all_paths.append(path)
                return

            visited.add(vertex.v_id)
            for neighbor in vertex.neighbors:
                if neighbor[0] not in visited:
                    dfs(self.get_vertex(neighbor[0]), end, path + [neighbor[0]], visited, all_paths)
            visited.remove(vertex.v_id)

        all_paths = []
        dfs(self.get_vertex(start), end, [start], set(), all_paths)
        return all_paths
