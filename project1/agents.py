def update_vertex_visit(vertex, agent_type):
    if agent_type == 'human':
        # update the global state
        vertex.num_of_ppl = 0
        if vertex.britte == False:
            vertex.britte = True


class HumanAgent:
    def __init__(self, agent_type, location, global_state):
        self.global_state = global_state
        self.agent_type = agent_type
        self.location = location
        self.steps = 0
        self.on_the_move = 0
        self.people_saved = 0
        self.score = 0

    def get_possible_actions(self):
        return [0]

    def play_turn(self, global_state):
        # check if the agent is on the move
        if self.on_the_move > 0:
            self.on_the_move -= 1
            print('agent is on the move, more {} turns left to get to the vertex'.format(self.on_the_move))

            return

        possible_vertices = self.get_possible_actions()

        # print possible vertices
        print("Possible vertices to move on:")
        for v in possible_vertices:
            print(v)

        # get user input for vertex to move on
        vertex = int(input("Enter vertex to move on: "))
        # check that is a valid input
        if vertex not in possible_vertices:
            print("Invalid vertex")
            exit()

        # move on vertex
        self.location = vertex

        # check if the agent saved people and if so update the agent and the world state
        self.people_saved = self.people_saved + vertex.num_of_ppl
        self.score = self.people_saved * 1000 - self.steps

        update_vertex_visit(vertex, self.agent_type)


class StupidGreedyAgent:
    def __init__(self, agent_type, location):
        self.agent_type = agent_type
        self.location = location
        self.score = 0

    def play_turn(self, global_state):
        pass


class SaboteurAgent:
    def __init__(self, agent_type, location):
        self.agent_type = agent_type
        self.location = location
        self.score = 0

    def play_turn(self, global_state):
        pass
