from p3.Helpers import VertexTypes, WeatherTypes


class Vertex:
    def __init__(self, v_id, prob_table):
        self.v_id = v_id
        self.prob_table = prob_table


class BayesianNetwork:
    def __init__(self):
        self.vertices: dict = {}
        self.parents_vertices: dict = {}
        self.children_vertices: dict = {}
        self.world_vertices_num = 0

    def add_causal_edge(self, parent_v, child_v):
        if parent_v.v_id in self.parents_vertices.keys():
            self.parents_vertices[parent_v.v_id].append(child_v.v_id)
        else:
            self.parents_vertices[parent_v.v_id] = [child_v.v_id]

        if child_v.v_id in self.children_vertices.keys():
            self.children_vertices[child_v.v_id].append(parent_v.v_id)
        else:
            self.children_vertices[child_v.v_id] = [parent_v.v_id]

    def add_vertex(self, vertex):
        self.vertices[vertex.v_id] = vertex

    def get_vertex(self, vertex_id):
        return self.vertices[vertex_id]

    def has_children(self, vertex_id):
        return vertex_id in self.parents_vertices.keys()

    def has_parents(self, vertex_id):
        return vertex_id in self.children_vertices.keys()

    def print_network(self):
        print(self.__str__())

    def __str__(self):
        string = ""

        # print weather vertex
        string += "_______ Weather _______\n"
        w_ver = self.get_vertex(VertexTypes.WEATHER)
        string += "P(mild)={}\n".format(w_ver.prob_table[WeatherTypes.MILD])
        string += "P(stormy)={}\n".format(w_ver.prob_table[WeatherTypes.STORMY])
        string += "P(extreme)={}\n".format(w_ver.prob_table[WeatherTypes.EXTREME])

        # print vertices
        string += "_______ Vertices _______\n"
        for i in range(1, self.world_vertices_num + 1):
            string += "VERTEX " + str(i) + "\n\n"
            b_ver = self.get_vertex(VertexTypes.BLOCKAGE + str(i))
            string += "P(blocked|mild)={}\n".format(b_ver.prob_table[WeatherTypes.MILD])
            string += "P(blocked|stormy)={}\n".format(b_ver.prob_table[WeatherTypes.STORMY])
            string += "P(blocked|extreme)={}\n".format(b_ver.prob_table[WeatherTypes.EXTREME])
            string += "\n"

            # print vertices
            e_ver = self.get_vertex(VertexTypes.EVACUEES + str(i))
            lst = list(e_ver.prob_table.keys())
            lst.reverse()
            for key in lst:
                string += "P(Evacuees|{}) = {}\n".format(key, e_ver.prob_table[key])
            string += "\n"

        return string
