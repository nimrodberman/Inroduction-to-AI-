# TODO - adapt the parser to the new format
from typing import Dict, List

from p1.Agents import HumanAgent, StupidGreedyAgent, SaboteurAgent
from p1.Enviorment import Vertex, Edge, Graph


class Parser:

    def __init__(self):
        pass

    def parse_vertex(self, line):
        try:
            people = int(line[line.index('P') + 1])
        except Exception as e:
            people = 0

        try:
            brittle = line.index('B') != -1

        except Exception as e:
            brittle = False

        vertex_id = line[line.index('V') + 1]

        return Vertex(vertex_id, people, brittle)

    def parse_edge(self, line):
        edge_index = line[line.index('E') + 1]
        weight = int(line[line.index('W') + 1])
        # set the edge to the vertexes
        vertex_1 = int(line[4])
        vertex_2 = int(line[6])

        return Edge(edge_index, vertex_1, vertex_2, weight)

    def parse_file_to_graph(self, file_path):
        # set the graph components
        g = Graph()

        vertices: List = []
        edges: Dict[int: Edge] = {}

        # open the file
        with open(file_path) as f:
            file_string = f.readlines()
            f.close()

        # parse the lines
        lines = file_string
        for line in lines:
            if len(line) < 2:
                continue
            if line[1] == "V":
                g.add_vertex(self.parse_vertex(line))
            elif line[1] == "E":
                g.add_edge(self.parse_edge(line))
            else:
                continue
        return g


def get_init_user_prompt(graph):
    agents = []
    # get agents number:
    agents_number = int(input("Enter number of agents: "))

    # for each agent, get its type
    for i in range(agents_number):
        # get agent type
        agent_type = int(input("Enter {} agent type(0-human, 1-stupid greedy, 2-saboteur): ".format(i)))
        # get agent desired location
        agent_desired_location = int(input(
            "Enter {} agent desired vertex location: ".format(i))) - 1  # -1 because the vertices are starting from 0
        if agent_type == 0:
            agents.append(HumanAgent(i, agent_desired_location, graph))
        elif agent_type == 1:
            agents.append(StupidGreedyAgent())
        elif agent_type == 2:
            agents.append(SaboteurAgent())
        else:
            print("Error: invalid agent type")
            exit(1)

    return agents
