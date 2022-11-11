import heapq
from typing import Dict, List


class Path:
    def __init__(self, vertex):
        self.vertex = vertex
        self.prev = None
        self.distance = float('inf')

    def __lt__(self, other):
        if self.distance == other.distance:
            return self.vertex.index < other.vertex.index
        return self.distance < other.distance


class Edge:
    def __init__(self, index, vertex1, vertex2, weight, blocked=False):
        self.index = index
        self.vertex2_index = max(vertex1, vertex2)
        self.vertex1_index = min(vertex1, vertex2)
        self.weight = weight
        self.blocked = blocked


class Vertex:
    def __init__(self, index, num_rescue, is_brittle, is_broken=False, time_exp=None):
        self.index = index
        self.num_rescue = num_rescue
        self.is_brittle = is_brittle
        self.time_exp = time_exp
        self.is_broken = is_broken
        self.edges = []


class Graph:
    def __init__(self):
        self.vertices: List = []
        self.edges: Dict = {}
        self.time = 0

    def add_edge(self, edge):
        vertex1 = min(edge.vertex1_index, edge.vertex2_index)
        vertex2 = max(edge.vertex1_index, edge.vertex2_index)
        self.edges[(vertex1, vertex2)] = edge

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def get_edge_by_vertices(self, vertex1, vertex2):
        """ check if a edge exist on the graph or else return it if bloacked or exists """
        vertex1_index = min(vertex1, vertex2)
        vertex2_index = max(vertex1, vertex2)
        edge = self.edges.get((vertex1_index, vertex2_index))
        if edge is None:
            return 'NO_EDGE'
        if edge.blocked:
            return 'BLOCKED'
        return edge

    def get_other_side_of_edge(self, edge, vertex):
        if edge.vertex1_index == int(vertex.index):
            return self.vertices[edge.vertex2_index - 1]
        return self.vertices[edge.vertex1_index - 1]

    def dijkstra(self, source):
        # TODO - add path a list of vertexes and that the algorithm will return it
        """ find the shortest path from source to all vertices """
        paths = []
        heap = []
        heapq.heapify(paths)
        visited_vertices = len(self.vertices) * [False]
        for v in self.vertices:
            p = Path(v)
            if int(v.index) == source:
                p.distance = 0
            heapq.heappush(heap, p)
            paths.append(p)

        while len(heap) > 0:
            u = heapq.heappop(heap)
            visited_vertices[int(u.vertex.index) - 1] = True
            for e in u.vertex.edges:
                v = self.get_other_side_of_edge(e, u.vertex)
                if not visited_vertices[int(v.index) - 1]:
                    alt = u.distance + e.weight
                    if alt < paths[int(v.index) - 1].distance:
                        paths[int(v.index) - 1].distance = alt
                        paths[int(v.index) - 1].prev = u
                        heapq.heapify(heap)
        return paths

    # def is_game_over(self, agents): TODO: implement this

    def print_graph(self):
        print("\n Graph: \n")
        for j in range(0, len(self.vertices)):
            v = self.vertices[j]
            print(
                "index={}, time_exp={}, num_people_to_rescue={}, is_brittle={}, is_broken={}".format(v.index,
                                                                                                     v.time_exp,
                                                                                                     v.num_rescue,
                                                                                                     v.is_brittle,
                                                                                                     v.is_broken))

        for e in self.edges:
            print(
                "index={}, {} <-> {}, weight={}, broken={}".format(self.edges[e].index,
                                                                   self.edges[e].vertex1_index,
                                                                   self.edges[e].vertex2_index,
                                                                   self.edges[e].weight,
                                                                   self.edges[e].blocked))
        print("time: {}".format(self.time))
        print("")


class EnvironmentSimulator:
    def __init__(self, graph, agents):
        self.graph = graph
        self.agents = agents

    def terminate_agent(self, agent):
        agent.not_active = True
        agent.update_score(graph=self.graph)

    def check_if_there_are_active_players(self):
        for agent in self.agents:
            if not agent.not_active:
                return True
        return False

    def print_agents_scores(self):
        print('\n\nThe agents scores are:')
        # print agents scores
        for agent in self.agents:
            print('Agent {} score: {}'.format(agent.index, agent.score))

    def check_if_agent_can_move(self, agent):

        # get all edges goes from the agent location:
        edges = [edge for edge in self.graph.edges.values() if
                 edge.vertex1_index == agent.location + 1 or edge.vertex2_index == agent.location + 1]
        # go over all the edges and see if there is a path to move to
        for edge in edges:
            if not edge.blocked:
                return True

        return False

    def run_simulation(self):
        while self.check_if_there_are_active_players():
            for agent in self.agents:
                # check if the agent is active
                if agent.not_active:
                    continue

                # check if the agent arrived to the destination
                if agent.on_edge == 0:
                    agent.arrived_to_destination(graph=self.graph, destination=agent.location)
                    # check that the agent have possible moves
                    if not self.check_if_agent_can_move(agent):
                        self.terminate_agent(agent)
                        print('No possible moves for agent {}'.format(agent.index))
                        continue

                # get the agent action
                action_to_take = agent.action(self.graph)

                # --- handle the action --- #
                # no operation action
                if action_to_take == 'NO-OP':
                    print('The agent {} is doing nothing'.format(agent.index))
                    continue

                # exit action
                elif action_to_take == 'EXIT':
                    self.terminate_agent(agent)
                    print('The agent {} is exiting'.format(agent.index))
                    continue

                # edge action
                elif action_to_take == 'ON-EDGE':
                    agent.on_edge = agent.on_edge - 1
                    print('The agent {} has more {} steps'.format(agent.index, agent.on_edge))
                    continue

                # traversal action
                else:
                    # take the departure and destination vertexes
                    vertex1 = agent.location
                    vertex2 = int(action_to_take) - 1  # -1 because indexes are from 0
                    # print the action intention
                    print('The agent {} is trying to move from {} to {}'.format(agent.index, vertex1 + 1, vertex2 + 1))
                    edge = self.graph.get_edge_by_vertices(vertex1 + 1, vertex2 + 1)

                    # check the edge validity
                    if edge == 'NO_EDGE':
                        self.terminate_agent(agent)
                        print('The agent {} is trying to move from {} to {} but there is no edge between them.'
                              'Terminating the agent'.format(agent.index, vertex1 + 1, vertex2 + 1))

                    elif edge == 'BLOCKED':
                        self.terminate_agent(agent)
                        print('The agent {} is trying to move from {} to {} but the edge is blocked.'
                              'Terminating the agent'.format(agent.index, vertex1 + 1, vertex2 + 1))
                    else:
                        # take the move
                        move_result = agent.agent_move(self.graph, edge, vertex2, is_sabotage=False)

                        # report if move fails
                        if move_result is None:
                            self.terminate_agent(agent)
                            print('The agent {} is trying to move from {} to {} but the move failed.'
                                  'Terminating the agent'.format(agent.index, vertex1 + 1, vertex2 + 1))

            self.graph.time += 1

        self.print_agents_scores()
