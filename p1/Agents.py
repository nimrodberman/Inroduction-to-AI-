from typing import List


class Agent:
    def __init__(self, index, initial_location):
        self.index = index
        self.location = initial_location
        self.score = 0
        self.not_active = False
        self.ppl_saved = 0
        self.on_edge = 0

    def action(self, graph):
        pass

    def arrived_to_destination(self, graph, destination):
        pass

    def update_score(self, graph):
        # if not graph.vertices[self.location].broken: # TODO - need this ?
        self.score = self.ppl_saved * 1000 - graph.time

    def agent_move(self, graph, edge, destination, is_sabotage):
        steps = edge.weight

        # update vertex state
        location = graph.vertices[self.location]
        if location.is_brittle:
            location.is_broken = True
            # brake all edges going from this vertex
            for e in graph.edges:
                if graph.edges[e].vertex1_index == self.location + 1 \
                        or graph.edges[e].vertex2_index == self.location + 1:
                    graph.edges[e].blocked = True

        # update agent state
        self.location = destination
        self.on_edge = steps - 1

        return destination

    def print_status(self, graph):
        # neighbours = graph.get_neighbours(graph.vertices[self.location]) TODO - need this ?
        print(
            "agent index: {}, location: {}, saved: {}, score: {}".format(self.index, self.location, self.ppl_saved,
                                                                         self.score))


class HumanAgent(Agent):
    def __init__(self, index, initial_location, graph):
        super().__init__(index, initial_location)
        # initial positioning  TODO - need this ? if not delete graph
        # self.ppl_saved += graph.vertices[self.location].num_rescue
        # graph.vertices[self.location].num_rescue = 0

    def arrived_to_destination(self, graph, destination):
        # update ppl_saved
        self.ppl_saved += graph.vertices[destination].num_rescue
        # update vertex state
        graph.vertices[destination].num_rescue = 0

    def action(self, graph):
        if self.on_edge > 0:
            print("the agent is on edge")
            return 'ON-EDGE'

        graph.print_graph()

        return input(
            "Please take an action ('no-op' for not moving,"
            "'exit' to exit or insert the vertex number you would like to go to): ".format()).upper()

    def print_scores(self):
        print("index: {}, scores: {},  type: human".format(self.index, self.score))


# TODO
class StupidGreedyAgent(Agent):

    def __init__(self, index, initial_location):
        super().__init__(index, initial_location)

    def arrived_to_destination(self, graph, destination):
        # update ppl_saved
        self.ppl_saved += graph.vertices[destination].num_rescue
        # print the agent saving people
        print("agent {} saved {} people from vertex {}".format(self.index, graph.vertices[destination].num_rescue,
                                                               destination))

        # update vertex state
        graph.vertices[destination].num_rescue = 0

    def action(self, graph):

        if self.on_edge > 0:
            print("the agent is on edge")
            return 'ON-EDGE'

        # if agent have not paths calculate all paths using dijkstra
        optional_paths = graph.dijkstra(self.location + 1)
        # filter paths to only include paths that have people to rescue and that the distance is not infinity
        optional_paths = list(
            filter(lambda x: x.distance != float('inf') and x.vertex.num_rescue > 0 and x.distance != 0,
                   optional_paths))

        # check if there are paths available
        if not optional_paths:
            print('no paths to rescue people')
            return 'EXIT'

        # sort by the shortest distance
        optional_paths.sort(key=lambda x: x.distance)

        cur = optional_paths[0]
        nxt = cur.prev_vertex
        while nxt.prev_vertex is not None:
            cur = nxt
            nxt = cur.prev_vertex

        return cur.vertex.index

    def print_scores(self):
        print("index: {}, scores: {},  type: greedy".format(self.index, self.score))


# TODO
class SaboteurAgent(Agent):

    def __init__(self):
        pass
