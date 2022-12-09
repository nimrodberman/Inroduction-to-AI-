import copy
from typing import List

from project2.Enviroment import Graph, AgentType
from project2.Helpers import CUTOFF


class Agent:

    def __init__(self, self_loc, other_loc, mode, graph: Graph):
        self.state: Graph = graph
        self.mode = mode
        self.loc = self_loc
        self.second_participator_loc = other_loc
        self.moves_history: [] = []
        self.score = 0
        self.last_seen_states: List[Graph] = []
        self.agent_type = None

    def make_a_move(self, move: int, current_loc: int, agent_type: AgentType):
        if agent_type == AgentType.MAX:
            self.state.max_loc = move
        else:
            self.state.min_loc = move
        self.loc = move
        # update the graph
        self.state.update_vertex_visit(self.loc, arrival=True, agent_type=self.agent_type)
        self.state.update_vertex_visit(current_loc, arrival=False, agent_type=self.agent_type)

    def alpha_beta_pruning_min_max(self, graph: Graph):
        return 0

    def make_move(self, graph: Graph):
        print("{} is making a move".format(type(self).__name__))

        # check if we are in a state loop. if so, terminate
        end_game = self.check_end_conditions()
        if not end_game:
            # update the last seen state
            self.last_seen_states.append(copy.deepcopy(graph))
            # make a move
            move = self.alpha_beta_pruning_min_max(self.state)
            if move is None:
                print("No moves to make")
            else:
                print("Move to make: {}".format(move))
                self.make_a_move(move, self.loc, self.agent_type)

            self.moves_history.append(move)
            return True

        else:
            print("End of the game. Terminating")
            return False

    def check_end_conditions(self):
        # get the graphs states:
        # agents locations, number of people to save, the same agent turn, the same broken vertexes
        # the current graph state
        agents_locations = [self.state.max_loc, self.state.min_loc]
        number_of_people_to_save = self.state.get_number_of_people_to_save()
        same_broken_vertexes = self.state.get_broken_vertices()

        # get the last seen state by the agent
        loop = False
        for state in self.last_seen_states:
            last_seen_agents_locations = [state.max_loc, state.min_loc]
            last_seen_number_of_people_to_save = state.get_number_of_people_to_save()
            last_seen_same_broken_vertexes = state.get_broken_vertices()

            if set(same_broken_vertexes) == set(last_seen_same_broken_vertexes) \
                    and agents_locations == last_seen_agents_locations \
                    and number_of_people_to_save == last_seen_number_of_people_to_save:
                loop = True
                break

        return number_of_people_to_save == 0 or loop

    def max_alpha_beta(self, graph: Graph, number_of_acts, alpha: float, beta: float):
        expansion = graph.expansion(AgentType.MAX)

        if graph.get_number_of_people_to_save() == 0 or number_of_acts >= CUTOFF:
            return self.calculate_score_by_game_mode(graph, AgentType.MAX)

        value = -float('inf')
        for ns in expansion:
            # take the minumum value
            value = max(value, self.min_alpha_beta(ns, number_of_acts + 1, alpha, beta))
            # check if the value is smaller than the alpha
            if value >= beta:
                return value
            # update the alpha
            alpha = min(alpha, value)

        # if there are no moves to make, make no-op expansion
        if not expansion:
            return max(value, self.min_alpha_beta(graph, number_of_acts + 1, alpha, beta))

        return value

    def min_alpha_beta(self, graph: Graph, number_of_acts, alpha: float, beta: float):
        expansion = graph.expansion(AgentType.MIN)

        if graph.get_number_of_people_to_save() == 0 or number_of_acts >= CUTOFF:
            return self.calculate_score_by_game_mode(graph, AgentType.MIN)

        value = float('inf')
        for ns in expansion:
            # take the minumum value
            value = min(value, self.max_alpha_beta(ns, number_of_acts + 1, alpha, beta))
            # check if the value is smaller than the alpha
            if value <= alpha:
                return value
            # update the beta
            beta = min(beta, value)

        # if there are no moves to make, make no-op expansion
        if not expansion:
            return min(value, self.max_alpha_beta(graph, number_of_acts + 1, alpha, beta))

        return value

    def calculate_score_by_game_mode(self, graph: Graph, agent_type: AgentType):
        if self.mode == 1:
            return graph.max_score - graph.min_score

        elif self.mode == 2:
            if agent_type == AgentType.MAX:
                if graph.min_score == graph.max_score:
                    return graph.max_score + graph.min_score
                return graph.max_score
            else:
                return -graph.min_score

        elif self.mode == 3:
            if agent_type == AgentType.MAX:
                return graph.min_score + graph.max_score
            else:
                return -(graph.min_score + graph.max_score)


class MaxAgent(Agent):
    def __init__(self, self_loc, other_loc, mode, graph: Graph):
        super().__init__(self_loc, other_loc, mode, graph)
        self.agent_type = AgentType.MAX

    def alpha_beta_pruning_min_max(self, graph: Graph):
        number_of_acts = 0
        best_option = None
        alpha = -float('inf')
        beta = float('inf')
        value = -float('inf')
        for ns in graph.expansion(self.agent_type.MAX):
            if self.mode == 1:
                ns_value = self.min_alpha_beta(ns, number_of_acts + 1, alpha, beta)
            elif self.mode == 2:
                ns_value = self.min_alpha_beta(ns, number_of_acts + 1, alpha, beta)
            else:
                ns_value = abs(self.min_alpha_beta(ns, number_of_acts + 1, alpha, beta))
            if ns_value > value:
                value = ns_value
                best_option = ns.max_loc
            alpha = max(alpha, value)
        return best_option


class MinAgent(Agent):
    def __init__(self, self_loc, other_loc, max_agent, mode):
        super().__init__(self_loc, other_loc, max_agent, mode)
        self.agent_type = AgentType.MIN

    def alpha_beta_pruning_min_max(self, graph: Graph):
        number_of_acts = 0
        best_option = None
        alpha = -float('inf')
        beta = float('inf')
        value = float('inf')
        for ns in graph.expansion(self.agent_type.MIN):
            if self.mode == 1:
                ns_value = self.max_alpha_beta(ns, number_of_acts + 1, alpha, beta)
            elif self.mode == 2:
                ns_value = self.max_alpha_beta(ns, number_of_acts + 1, alpha, beta)
            else:
                ns_value = -abs(self.max_alpha_beta(ns, number_of_acts + 1, alpha, beta))
            if ns_value < value:
                value = ns_value
                best_option = ns.min_loc
            beta = max(beta, value)
        return best_option
