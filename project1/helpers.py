import copy
from typing import Dict, List

from project1.Agents import HumanAgent, StupidGreedyAgent, SaboteurAgent
from project1.Enviroment import Vertex, Edge, Graph


class Parser:

    def __init__(self):
        pass

    def parse_vertex(self, line):
        try:
            line.index('P')
            people = int(line.split(' ')[1][1:].replace('\n', ''))
        except Exception as e:
            people = 0

        try:
            brittle = line.index('B') != -1

        except Exception as e:
            brittle = False

        vertex_id = line.split(' ')[0][2:].replace('\n', '')

        return int(vertex_id), int(people), brittle

    def parse_edge(self, line):
        edge_index = line.split(' ')[0][2:]
        weight = int(line.split(' ')[3][1:].replace('\n', ''))
        # set the edge to the vertexes
        vertex_1 = int(line.split(' ')[1])
        vertex_2 = int(line.split(' ')[2])

        return int(edge_index), int(vertex_1), int(vertex_2), int(weight)

    def parse_file_to_graph(self, file_path):
        # set the graph components
        g = Graph()

        vertices: Dict[int: Vertex] = {}
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
                vertex_id, people, brittle = self.parse_vertex(line)
                g.add_vertex(vertex_id, people, brittle)
            elif line[1] == "E":
                edge_index, vertex_1, vertex_2, weight = self.parse_edge(line)
                g.add_edge(edge_index, vertex_1, vertex_2, weight)
            else:
                continue

        g.original_graph = copy.deepcopy(g)
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
            "Enter {} agent desired vertex location: ".format(i)))
        if agent_type == 0:
            agents.append(HumanAgent(i, agent_desired_location))
        elif agent_type == 1:
            agents.append(StupidGreedyAgent(i, agent_desired_location))
        elif agent_type == 2:
            agents.append(SaboteurAgent(i, agent_desired_location))
        else:
            print("Error: invalid agent type")
            exit(1)

    return agents
