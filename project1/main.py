from typing import Dict
from project1.agents import HumanAgent, StupidGreedyAgent, SaboteurAgent


class GlobalState:
    def __init__(self):
        self.time = 0
        self.agents = []
        self.graph = None


class EnvSimulator:
    def __init__(self, env, global_state):

        self.env = env
        self.global_state = global_state

    # display the global state
    def display_global_state(self):
        pass

    def run(self):
        while True:

            # for each agent, play its turn
            for agent in self.global_state.agents:
                agent.play_turn(self.global_state)

            # update the global state
            self.global_state.time += 1


# init the game state
def init_state():
    state = {"agents": []}
    return state


def get_init_user_prompt(state: GlobalState):
    # get agents number:
    agents_number = int(input("Enter number of agents: "))

    # for each agent, get its type
    for i in range(agents_number):
        # get agent type
        agent_type = input("Enter {} agent type(0-human, 1-stupid greedy, 2-saboteur): ".format(i))
        # get agent desired location
        agent_desired_location = input("Enter {} agent desired location: ".format(i))
        if agent_type == 0:
            state.agents.append(HumanAgent(agent_type, agent_desired_location, state))
        elif agent_type == 1:
            state.agents.append(StupidGreedyAgent(agent_type, agent_desired_location))
        elif agent_type == 2:
            state.agents.append(SaboteurAgent(agent_type, agent_desired_location))
        else:
            print("Error: invalid agent type")
            exit()


if __name__ == '__main__':
    # init the global state
    global_state = GlobalState()

    # init the player
    get_init_user_prompt(global_state)

    # init the simulator
    env_simulator = EnvSimulator(None, global_state)

    # run the simulator
    env_simulator.run()
