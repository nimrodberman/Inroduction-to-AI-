import copy
import heapq
from typing import Dict


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


class AStarPath:
    def __init__(self, destination_vertex):
        self.dst_vertex = destination_vertex
        self.org_vertex = None
        self.vertices_visited = [destination_vertex]
        self.prev_vertex = None
        self.distance = float('inf')
        self.distance_walked = 0

    def __lt__(self, other):
        if self.distance + self.distance_walked == other.distance + other.distance_walked:
            return self.dst_vertex < other.dst_vertex
        return self.distance + self.distance_walked < other.distance + other.distance_walked


class Graph:
    def __init__(self):
        self.vertices: Dict[int: Vertex] = {}
        self.edges: Dict[(int, int): Edge] = {}
        self.prt2_graph = None
        self.initial_graph = None

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

    def update_vertex_visit(self, vertex_index, arrival, agent):
        if arrival:
            return self.vertices[vertex_index].num_rescue
        else:
            self.vertices[vertex_index].num_rescue = 0
            # remove the vertex if is brittle
            if self.vertices[vertex_index].is_brittle:
                self.remove_vertex(vertex_index)

            if agent.heuristic:
                self.remove_vertex(vertex_index)

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

    def dijkstra(self, source):
        """ find the shortest path from source to all vertices """
        paths = []
        heap = []
        heapq.heapify(paths)
        visited_vertices = len(self.vertices) * [False]
        visited_vertices_map = {}
        i = 0
        for vertex in self.vertices.keys():
            visited_vertices_map[vertex] = i
            i += 1

        for v in self.vertices:
            p = Path(v)
            if v == source:
                p.distance = 0
            heapq.heappush(heap, p)
            paths.append(p)

        while len(heap) > 0:
            u = heapq.heappop(heap)
            visited_vertices[visited_vertices_map[u.dst_vertex]] = True
            u_neighbours = self.get_vertex_neighbours_indexes(u.dst_vertex)
            for e in u_neighbours:
                edge = self.get_edge(u.dst_vertex, e)
                v = e
                if not visited_vertices[visited_vertices_map[v]]:
                    alt = u.distance + edge.weight
                    if alt < paths[visited_vertices_map[v]].distance:
                        paths[visited_vertices_map[v]].distance = alt
                        paths[visited_vertices_map[v]].prev_vertex = u
                        heapq.heapify(heap)
        return paths


class HeuristicGraph(Graph):
    def __init__(self, initial_vertex_location, graph):
        super().__init__()
        self.vertices = copy.deepcopy(graph.vertices)
        self.edges = {}
        self.prt2_graph = None
        self.initial_graph = None
        self.graph_copy = copy.deepcopy(graph)

        # create a new graph were there are only vertices that people are on them and the paths are the shortest path
        # first, remove all the the vertices that don't have people on them
        vertices_to_remove = [v for v in self.vertices.values() if
                              v.num_rescue == 0 and initial_vertex_location != v.index]

        for v in vertices_to_remove:
            self.remove_vertex(v.index)

        # clear all vertices edges
        for vertex in self.vertices.values():
            vertex.is_brittle = False

        # for each vertex, calculate the shortest path to all the other vertices and add them to the graph
        i = 0
        for vertex in self.vertices:
            paths = self.graph_copy.dijkstra(vertex)
            # filter paths to vertices that were deleted
            paths = list(
                filter(lambda p: (p.dst_vertex in list(self.vertices.keys())) and p.dst_vertex != vertex, paths))
            # add edges to vertices
            for path in paths:
                self.add_edge(i, vertex, path.dst_vertex, path.distance)
                i += 1

    def a_star(self, source, limit, is_real_time=False):
        """ run a a star algorithm on the graph """
        expansions = 0
        fringe = []
        heapq.heapify(fringe)
        heapq.heappush(fringe, AStarPath(source))
        while len(fringe) > 0 and expansions < limit:
            u: AStarPath = heapq.heappop(fringe)
            # if visited in all vertices return the path
            if len(u.vertices_visited) == len(self.vertices):
                return u, expansions
            # get vertex neighbours - expansion
            vertex_neighbours = list(
                filter(lambda v: v not in u.vertices_visited, self.get_vertex_neighbours_indexes(u.dst_vertex)))
            expansions += 1

            if expansions == limit:
                if is_real_time:
                    return u, expansions
                else:
                    print("too many expansions")
                    return 'EXIT', expansions

            for neighbour in vertex_neighbours:
                p = AStarPath(neighbour)
                p.prev_vertex = source
                p.distance = self.get_edge(source, neighbour).weight
                # calculate heuristic
                p.distance_walked = p.distance_walked + p.distance
                # set a visit
                p.vertices_visited = list(set(p.vertices_visited + u.vertices_visited))
                # push to fringe
                heapq.heappush(fringe, p)

        return heapq.heappop(fringe), expansions


class EnvironmentSimulator:
    def __init__(self, graph, agents, T, prt2=False):
        if prt2:
            self.graph = HeuristicGraph(agents[0].location, graph)
        else:
            self.graph: Graph = graph
        self.agents = agents
        self.time = 0
        self.expansion_limit = 1000000
        self.T = T

    def terminate_agent(self, agent):
        agent.is_active = False
        agent.update_score(self.time)

    def check_if_there_is_an_active_player(self):
        for agent in self.agents:
            if agent.is_active and not agent.sabotage:
                return True
        return False

    def print_agents_scores(self):
        print('\n\nThe agents scores are:')
        # print agents scores
        for agent in self.agents:
            agent.update_score(self.time)
            print('Agent {} score: {}'.format(agent.index, agent.score))

    def run_simulation(self):
        while self.check_if_there_is_an_active_player():
            # iterate over the agents
            for agent in self.agents:
                # check if player active. if not continue
                if not agent.is_active:
                    continue
                # if an agent arrived to a vertex. change the vertex and player status.
                all_ppl_saved = agent.update_status_of_agent_and_graph_if_agent_arrived(agent.location, self.graph)
                if all_ppl_saved:
                    print("saved all people")
                    self.terminate_agent(agent)
                    continue

                # get the agent's next move
                action_to_take, time_taken = agent.action_to_take(graph=self.graph, limit=self.expansion_limit,
                                                                  T=self.T)

                self.time += time_taken

                # --------------------- take the actions --------------------- #
                # no moves left
                if action_to_take == 'NO-MOVES':
                    self.terminate_agent(agent)
                    print('The agent {} is exiting'.format(agent.index))
                    continue

                # agent is on edge
                elif action_to_take == 'ON-EDGE':
                    agent.on_edge -= 1
                    print('The agent {} has more {} steps'.format(agent.index, agent.on_edge))
                    continue

                # exit action
                elif action_to_take == 'EXIT':
                    self.terminate_agent(agent)
                    print('The agent {} is exiting'.format(agent.index))
                    continue

                elif action_to_take == 'NO-OP':
                    print('The agent {} is doing nothing'.format(agent.index))
                    continue

                # else if the agent picked a vertex to go to (the action is already validated)
                else:
                    destination_vertex_index = action_to_take
                    agent.move_agent_to_destination_vertex(agent.location, destination_vertex_index, self.graph, agent)

                print("time: {}".format(self.time))
            self.print_agents_scores()
