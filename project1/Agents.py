from project1.Enviroment import Graph, HeuristicGraph


class Agent:
    def __init__(self, agent_index: int, initial_vertex_index: int):
        self.index = agent_index
        self.location = initial_vertex_index
        self.score = 0
        self.is_active = True
        self.ppl_saved = 0
        self.on_edge = 0
        self.sabotage = False
        self.heuristic = False

    def update_score(self, time):
        self.score = self.ppl_saved * 1000 - time

    def arrived_to_destination(self, dest_vertex_index: int, graph):
        if self.sabotage:
            pass
        else:
            vertex = graph.get_vertex(dest_vertex_index)
            # update ppl_saved
            self.ppl_saved += vertex.num_rescue
            # print the agent saving people
            print("agent {} saved {} people from vertex {}".format(self.index, vertex.num_rescue, dest_vertex_index))

            # update vertex state
            vertex.num_rescue = 0

    def update_status_of_agent_and_graph_if_agent_arrived(self, agent_location_vertex: int, graph: Graph):
        """ check if the agent finished his movement. If so, update the graph and the agent status """
        if self.on_edge == 0:
            self.arrived_to_destination(agent_location_vertex, graph)
            return graph.all_ppl_saved()
        return False

    def action_to_take(self, graph: Graph, limit, T):
        """ return the agents next move"""

        # check if the agent is on the move
        if self.on_edge > 0:
            return "ON-EDGE", 1

        # check if the agent has possible moves
        vertex_neighbours = graph.get_vertex_neighbours_indexes(self.location)
        if len(vertex_neighbours) == 0:
            return "NO-MOVES", 0

    def move_agent_to_destination_vertex(self, current_vertex_index: int, dest_vertex_index: int, graph: Graph, agent):
        print('The agent {} is moving from {} to {}'.format(self.index, self.location, dest_vertex_index))
        edge = graph.get_edge(current_vertex_index, dest_vertex_index)

        # update agent state
        steps = edge.weight
        self.location = dest_vertex_index
        self.on_edge = steps - 1  # reduce the journey in one step

        # update vertex state
        graph.update_vertex_visit(current_vertex_index, False, agent)


class HumanAgent(Agent):
    def __init__(self, agent_index, initial_vertex_index):
        super().__init__(agent_index, initial_vertex_index)

    def action_to_take(self, graph: Graph, limit, T):
        """ return the agents next move"""

        # check if the agent is on the move
        if self.on_edge > 0:
            return "ON-EDGE", 1

        # check if the agent has possible moves
        vertex_neighbours = graph.get_vertex_neighbours_indexes(self.location)
        if len(vertex_neighbours) == 0:
            return "NO-MOVES", 0

        graph.print_graph()
        user_input = input(
            "Please take an action ('no-op' for not moving,"
            "'exit' to exit or insert the vertex number you would like to go to): ".format()).upper()

        if user_input == 'NO-OP':
            return 'NO-OP', 1

        if user_input.isdigit():
            destination_vertex = int(user_input)
            # validate the user input is a valid vertex
            if graph.is_edge_exist(self.location, destination_vertex):
                return destination_vertex, 1
            print("The vertex {} is not a valid vertex".format(destination_vertex))

        return "EXIT", 0


class StupidGreedyAgent(Agent):
    def __init__(self, agent_index, initial_vertex_index):
        super().__init__(agent_index, initial_vertex_index)

    def action_to_take(self, graph: Graph, limit, T):
        """ return the agents next move"""

        # check if the agent is on the move
        if self.on_edge > 0:
            return "ON-EDGE", 1

        # check if the agent has possible moves
        vertex_neighbours = graph.get_vertex_neighbours_indexes(self.location)
        if len(vertex_neighbours) == 0:
            return "NO-MOVES", 0

        optional_paths = list(
            filter(lambda p: p.distance != float('inf') and
                             graph.get_vertex(p.dst_vertex).num_rescue > 0 and
                             p.distance != 0,
                   graph.dijkstra(self.location)))

        # check if there are paths available
        if not optional_paths:
            print('no paths to rescue people')
            return 'EXIT', 0

        # sort by distance and return the shortest path
        optional_paths.sort(key=lambda x: x.distance)

        return optional_paths[0].get_next_step(), 1


class SaboteurAgent(Agent):
    def __init__(self, agent_index, initial_vertex_index):
        super().__init__(agent_index, initial_vertex_index)
        self.sabotage = True

    def action_to_take(self, graph: Graph, limit, T):
        """ return the agents next move"""

        # check if the agent is on the move
        if self.on_edge > 0:
            return "ON-EDGE", 1

        # check if the agent has possible moves
        vertex_neighbours = graph.get_vertex_neighbours_indexes(self.location)
        if len(vertex_neighbours) == 0:
            return "NO-MOVES", 0

        optional_paths = list(
            filter(lambda x: x.distance != float('inf') and x.dst_vertex.is_brittle and x.distance != 0,
                   graph.dijkstra(self.location)))

        # check if there are paths available
        if not optional_paths:
            print('no paths to rescue people not moving')
            return 'NO-OP', 1

        # sort by distance and return the shortest path
        optional_paths.sort(key=lambda x: x.distance)
        return optional_paths[0].dst_vertex, 1


class GreedyHeuristicAgent(Agent):
    def __init__(self, agent_index, initial_vertex_index):
        super().__init__(agent_index, initial_vertex_index)
        self.heuristic = True

    # this time we use the heuristic that the graph don't have brittle vertices
    def action_to_take(self, graph: HeuristicGraph, limit, T=0.01):
        """ return the agents next move"""

        # check if the agent is on the move
        if self.on_edge > 0:
            return "ON-EDGE", 1

        # check if the agent has possible moves
        vertex_neighbours = graph.get_vertex_neighbours_indexes(self.location)
        if len(vertex_neighbours) == 0:
            return "NO-MOVES", 0

        # optional_move = list(
        #     filter(lambda p: p.distance != float('inf') and p.dst_vertex.num_rescue > 0 and p.distance != 0,
        #            graph.dijkstra(self.location)))
        optional_move = list(
            filter(lambda p: p.distance != float('inf') and p.distance != 0, graph.dijkstra(self.location)))

        # sort by distance and return the shortest path
        optional_move.sort(key=lambda x: x.distance)
        return optional_move[0].dst_vertex, 1


class AStarHeuristicAgent(Agent):
    def __init__(self, agent_index, initial_vertex_index):
        super().__init__(agent_index, initial_vertex_index)
        self.heuristic = True
        self.moves = []

    # this time we use the heuristic that the graph don't have brittle vertices
    def action_to_take(self, graph: HeuristicGraph, limit=10000, T=0.01):
        # check if the agent is on the move
        if self.on_edge > 0:
            return "ON-EDGE", 1

        # check if the agent has possible moves
        vertex_neighbours = graph.get_vertex_neighbours_indexes(self.location)
        if len(vertex_neighbours) == 0:
            return "NO-MOVES", 0

        # if no moves are planned, search the next moves
        if not self.moves:
            path, time = graph.a_star(self.location, limit)
            if path == 'EXIT':
                return 'EXIT', 0
            self.moves = path.vertices_visited[1:]
            if self.moves == 'EXIT':
                return 'EXIT', 0
            return self.moves.pop(0), 1
        else:
            return self.moves.pop(0), 1


class AStarRealTimeHeuristicAgent(Agent):
    def __init__(self, agent_index, initial_vertex_index):
        super().__init__(agent_index, initial_vertex_index)
        self.heuristic = True
        self.moves = []

    # this time we use the heuristic that the graph don't have brittle vertices
    def action_to_take(self, graph: HeuristicGraph, limit=10, T=0.01):
        # check if the agent is on the move
        if self.on_edge > 0:
            return "ON-EDGE", 1

        # check if the agent has possible moves
        vertex_neighbours = graph.get_vertex_neighbours_indexes(self.location)
        if len(vertex_neighbours) == 0:
            return "NO-MOVES", 0

        # if no moves are planned, search the next moves
        if not self.moves:
            path, time = graph.a_star(self.location, limit, is_real_time=True)
            if path == 'EXIT':
                return 'EXIT', 0
            self.moves = path.vertices_visited[1:]
            if self.moves == 'EXIT':
                return 'EXIT', 0
            return self.moves.pop(0), int(T * time) + 1
        else:
            return self.moves.pop(0), 1
