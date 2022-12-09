import copy
import heapq
from enum import Enum
from typing import Dict, List


class AgentType(Enum):
    MAX = 1
    MIN = 2


class Vertex:
    def __init__(self, index, num_rescue, is_brittle, is_broken=False):
        self.index = index
        self.num_rescue = num_rescue
        self.is_brittle = is_brittle
        self.is_broken = is_broken


class Edge:
    def __init__(self, index, vertex1_index, vertex2_index, weight):
        self.index = index
        self.vertex1_index = min(vertex1_index, vertex2_index)
        self.vertex2_index = max(vertex1_index, vertex2_index)
        self.weight = weight


class Path:
    def __init__(self, destination_vertex):
        self.dst_vertex = destination_vertex
        self.org_vertex = None
        self.path = []
        self.prev_vertex = None
        self.distance = float('inf')

    def get_next_step(self):
        cur_path = self
        prev_path = self.prev_vertex
        while prev_path.distance != 0:
            cur_path = prev_path
            prev_path = prev_path.prev_vertex
        return cur_path.dst_vertex

    def __lt__(self, other):
        if self.distance == other.distance:
            return self.dst_vertex < other.dst_vertex
        return self.distance < other.distance


class Graph:
    def __init__(self):
        self.vertices: Dict[int: Vertex] = {}
        self.edges: Dict[(int, int): Edge] = {}
        self.max_loc = -1
        self.min_loc = -1
        self.max_score = 0
        self.min_score = 0

    def all_ppl_saved(self):
        for vertex in self.vertices.values():
            if vertex.num_rescue > 0:
                return False
        return True

    def get_vertex(self, vertex_index):
        return self.vertices[vertex_index]

    def get_edge(self, vertex1_index, vertex2_index):
        min_index = min(vertex1_index, vertex2_index)
        max_index = max(vertex1_index, vertex2_index)
        return self.edges[(min_index, max_index)]

    def add_edge(self, index, vertex1_index, vertex2_index, weight):
        min_index = min(vertex1_index, vertex2_index)
        max_index = max(vertex1_index, vertex2_index)
        self.edges[(min_index, max_index)] = Edge(index, min_index, max_index, weight)

    def add_vertex(self, index, num_rescue, is_brittle):
        self.vertices[index] = Vertex(index, num_rescue, is_brittle)

    def remove_edge(self, vertex1_index, vertex2_index):
        self.edges.pop((vertex1_index, vertex2_index))

        # check if there a lonely vertex and delete it if do
        if not self.get_vertex_neighbours_indexes(vertex1_index):
            self.remove_vertex(vertex1_index)
        if not self.get_vertex_neighbours_indexes(vertex2_index):
            self.remove_vertex(vertex1_index)

    def remove_vertex(self, vertex_index):
        self.vertices.pop(vertex_index)
        # remove all the edges comes from this vertex
        to_remove = []
        for edge in self.edges.values():
            if edge.vertex1_index == vertex_index or edge.vertex2_index == vertex_index:
                to_remove.append(edge)

        for edge in to_remove:
            self.edges.pop((edge.vertex1_index, edge.vertex2_index))

    def get_vertex_neighbours_indexes(self, vertex_index: int):
        """returns the vertexes that has edges with the given vertex"""
        neighbours_indexes = []
        for edge in self.edges.values():
            if edge.vertex1_index == vertex_index:
                neighbours_indexes.append(edge.vertex2_index)
            elif edge.vertex2_index == vertex_index:
                neighbours_indexes.append(edge.vertex1_index)
        return neighbours_indexes

    def get_vertex_other_end(self, edge, vertex_index):
        if edge.vertex1_index == vertex_index:
            return edge.vertex2_index
        else:
            return edge.vertex1_index

    def is_edge_exist(self, vertex1_index, vertex2_index):
        min_index = min(vertex1_index, vertex2_index)
        max_index = max(vertex1_index, vertex2_index)
        return (min_index, max_index) in self.edges

    def update_vertex_visit(self, vertex_index, arrival, agent_type):
        if arrival:
            # update graph
            if agent_type == AgentType.MAX:
                self.max_score += self.vertices[vertex_index].num_rescue
            else:
                self.min_score += self.vertices[vertex_index].num_rescue

            self.vertices[vertex_index].num_rescue = 0
        # remove the vertex if is brittle
        else:
            if self.vertices[vertex_index].is_brittle:
                self.vertices[vertex_index].is_broken = True

    def print_graph(self):
        print("\n Graph: \n")
        for k, v in self.vertices.items():
            print("index={}, num_people_to_rescue={}, is_brittle={}, is_broken={}".format(v.index,
                                                                                          v.num_rescue,
                                                                                          v.is_brittle,
                                                                                          v.is_broken))

        for e in self.edges:
            print(
                "index={}, {} <-> {}, weight={}".format(self.edges[e].index,
                                                        self.edges[e].vertex1_index,
                                                        self.edges[e].vertex2_index,
                                                        self.edges[e].weight))
        print("")

    def expansion(self, agent_type: AgentType):
        if agent_type == AgentType.MIN:
            return self.min_next_expansion()
        elif agent_type == AgentType.MAX:
            return self.max_next_expansion()
        else:
            raise Exception("Invalid agent type")

    def max_next_expansion(self):
        curr_vertex_index = self.max_loc
        sim_states = []
        # expand the node
        for neighbour in self.get_vertex_neighbours_indexes(curr_vertex_index):
            if not self.get_vertex(neighbour).is_broken:
                next_loc = neighbour
                ns = copy.deepcopy(self)
                ns.max_loc = next_loc
                # make a simulated move
                ns.update_vertex_visit(curr_vertex_index, False, AgentType.MAX)
                ns.update_vertex_visit(next_loc, True, AgentType.MAX)
                sim_states.append(ns)

        return sim_states

    def min_next_expansion(self):
        curr_vertex_index = self.min_loc
        sim_states = []
        # expand the node
        for neighbour in self.get_vertex_neighbours_indexes(curr_vertex_index):
            if not self.get_vertex(neighbour).is_broken:
                next_loc = neighbour
                ns = copy.deepcopy(self)
                ns.min_loc = next_loc
                # make a simulated move
                ns.update_vertex_visit(curr_vertex_index, False, AgentType.MIN)
                ns.update_vertex_visit(next_loc, True, AgentType.MIN)
                sim_states.append(ns)

        return sim_states

    def get_number_of_people_to_save(self):
        # return the number of people to rescure
        num_left_to_save = 0
        for v in self.vertices.values():
            num_left_to_save += v.num_rescue
        return num_left_to_save

    def get_broken_vertices(self) -> List[int]:
        broken_vertices = []
        for vertex in self.vertices.values():
            if vertex.is_broken:
                broken_vertices.append(vertex.index)
        return broken_vertices

    def get_agents_locations(self):
        return self.min_loc, self.max_loc
