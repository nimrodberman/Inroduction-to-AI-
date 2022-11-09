# env:
from typing import List

class Vertex:

    def _init_(self, id, num_rescue=0, brittle=False):
        self.num_rescue = num_rescue
        self.id = id
        self.brittle = brittle


class Edge:

    def _init_(self, weight, vert1, vert2):
        self.weight = weight
        self.vert1: Vertex = vert1
        self.vert2: Vertex = vert2
        self.broken = False

    def brittle(self):
        broken = True


class Environment:

    def _int_(self, edges, vertices):
        self.edges: List[Edge] = edges
        self.vertices: List[Vertex] = vertices

    def display(self):
        print("Environment edges:", self.edges)
        print("Environment vertices:", self.vertices)


# -----------------------------------------------------------------------------
# used for parsing- returns the array until first whitespace
def cut_list(arr):
    val = []
    for i in arr:
        if i == "":
            return val
        val.append(i)


def parse_vertex(line, verts):
    weight = 0
    vert1_id = 0
    vert2_id = 0
    comps = cut_list(line.split(separator=" "))
    return Edge()


def parse_edge(line):
    comps = cut_list(line.split(separator=" "))
    for c in comps:
        if c[0] == "V":
            id = c[0][2]
        elif c[0] == "P":
            num_rescue = c[0][2:]
        else:
            brittle = True
    return Vertex(id, num_rescue, brittle)


def parse_file(file_path):
    vertices: List[Vertex] = []
    edges: List[Edge] = []
    with open(file_path) as f:
        file_string = f.readlines()
        f.close()
    lines = file_string.split(separator="\n")
    for line in lines:
        if line[1] == "V":
            parse_vertex(line.split(separator=";"))
        elif line[1] == "E":
            parse_edge(line, vertices)
        else:
            continue
