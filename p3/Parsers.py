import copy
import itertools

from p3.BayesianNetwork import BayesianNetwork, Vertex
from p3.Enviornmnet import WorldGraph, WorldVertex
from p3.Helpers import WeatherTypes, VertexTypes, noisyOr


class Parser:
    def __init__(self, path):
        self.path = path

    def parse_bayes_net(self, world: WorldGraph) -> BayesianNetwork:
        # create empty bayes network
        bayes_net = BayesianNetwork()

        # read the file
        with open(self.path, 'r') as file:
            is_first_line = True
            for l in file.readlines():
                # split each word in a line
                words = l.split(" ")

                # skip empty lines
                if words[0] != "#V" and words[0] != "#E" and words[0] != "#W" and not is_first_line:
                    continue

                # classify lines and act accordingly
                if words[0] == "#V" and not is_first_line:
                    if words[2] != 'F':
                        raise Exception("Only F is supported")

                    # vertex details
                    v_index = int(words[1])
                    v_name = VertexTypes.BLOCKAGE + words[1]
                    mild_prob = float(words[3])
                    v = Vertex(v_name, {WeatherTypes.MILD: mild_prob,
                                        WeatherTypes.STORMY: mild_prob * 2,
                                        WeatherTypes.EXTREME: mild_prob * 3})
                    bayes_net.add_vertex(v)

                    # create neighbors
                    ngb = n_create(world, v_index)
                    # create the probabilities table
                    truth_table = list(itertools.product([False, True], repeat=len(ngb)))
                    # create edge vertex
                    edge_prob_table = {}
                    for key in truth_table:
                        edge_prob_table[create_table_entry_key(key, ngb)] = noisyOr(key, ngb)

                    # add info to the bayes network
                    edge_v = Vertex(VertexTypes.EVACUEES + words[1], edge_prob_table)
                    bayes_net.add_vertex(edge_v)
                    for n in ngb:
                        neighbor_b_node = bayes_net.get_vertex(VertexTypes.BLOCKAGE + str(n[0]))
                        bayes_net.add_causal_edge(neighbor_b_node, edge_v)

                elif is_first_line:
                    weather_vertex = Vertex(VertexTypes.WEATHER, {})
                    bayes_net.add_vertex(weather_vertex)
                    vertices_num = int(words[1])
                    bayes_net.world_vertices_num = vertices_num
                    i = 1
                    while i <= vertices_num:
                        blockage_vertex = Vertex(VertexTypes.BLOCKAGE + str(i), {WeatherTypes.MILD: -1,
                                                                                 WeatherTypes.STORMY: -1,
                                                                                 WeatherTypes.EXTREME: -1})
                        bayes_net.add_vertex(blockage_vertex)
                        bayes_net.add_causal_edge(weather_vertex, blockage_vertex)
                        i += 1
                    is_first_line = False

                elif words[0] == "#W":
                    mild = float(words[1])
                    stormy = float(words[2])
                    extreme = float(words[3])

                    if mild + stormy + extreme != 1:
                        raise Exception("The probabilities must sum to 1")

                    weather_vertex = Vertex(VertexTypes.WEATHER, {WeatherTypes.MILD: mild,
                                                                  WeatherTypes.STORMY: stormy,
                                                                  WeatherTypes.EXTREME: extreme})
                    bayes_net.add_vertex(weather_vertex)

                else:
                    raise Exception("Unknown line type {}".format(words[0]))

        return bayes_net

    def parse_world(self) -> WorldGraph:
        world = WorldGraph()

        # read the file
        with open(self.path, 'r') as file:
            is_first_line = True
            for l in file.readlines():
                # skip the first line
                if is_first_line:
                    is_first_line = False
                    continue
                # split each word in a line
                words = l.split(" ")

                # skip empty lines
                if words[0] != "#V" and words[0][:2] != "#E":
                    continue

                if words[0] == "#V":
                    world.add_vertex(self.parse_vertex(words))
                else:
                    world.edges[int(words[0][2])] = [int(words[1]), int(words[2])]
                    self.parse_negihboors(words, world)

        return world

    def parse_negihboors(self, words, world: WorldGraph):
        v1 = world.get_vertex(int(words[1]))
        v2 = world.get_vertex(int(words[2]))
        w = int(words[3][1:])
        v1.add_neighbor(v2.v_id, w)
        v2.add_neighbor(v1.v_id, w)

    def parse_vertex(self, words):
        vertex_id = words[1]
        return WorldVertex(int(vertex_id))

def n_create(world, v_index):
    ngb = copy.deepcopy(world.get_vertex(v_index).neighbors)
    # add edge to the new node
    ngb.insert(0, [v_index, 0])
    ngb = sorted(ngb, key=lambda x: x[0])
    return ngb


def create_table_entry_key(key, ngb):
    final_string = []
    i = 0
    while i < len(key):
        if key[i]:
            final_string.append(str(ngb[i][0]) + " block")
        else:
            final_string.append(str(ngb[i][0]) + " not blocked")
        i += 1

    return str.join(",", final_string)
