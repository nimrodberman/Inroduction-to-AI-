class Agent:
    def __init__(self, index, initial_location):
        self.index = index
        self.location = initial_location
        self.score = 0
        self.not_active = False
        # self.carried_people = 0 TODO: need this ?
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
        self.on_edge = steps

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

    def __init__(self):
        pass

# TODO
class SaboteurAgent(Agent):

    def __init__(self):
        pass


