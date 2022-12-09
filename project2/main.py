from typing import List

from project2.Agents import MaxAgent, MinAgent, Agent
from project2.Enviroment import Graph
from project2.Helpers import Parser


def get_init_user_prompt():
    # choose the game mode
    game_type = int(input("Enter game type you would like to play."
                          " 1 for Zero Sum Game, 2 for Semi-cooperative game, 3 for Fully Cooperative game: "))
    # choose the agents positions
    agent1_position = int(input("Enter the vertex number of the first agent: "))
    agent2_position = int(input("Enter the vertex number of the second agent: "))

    return game_type, agent1_position, agent2_position


def create_agents(the_game_mode: int, agent1_position: int, agent2_position: int, game_graph: Graph) -> List[Agent]:
    agent_max = None
    agent_min = None

    if the_game_mode == 1:
        agent_max = MaxAgent(agent1_position, agent2_position, game_mode, game_graph)
        agent_min = MinAgent(agent1_position, agent2_position, game_mode, game_graph)

    elif the_game_mode == 2:
        agent_max = MaxAgent(agent1_position, agent2_position, game_mode, game_graph)
        agent_min = MinAgent(agent1_position, agent2_position, game_mode, game_graph)

    elif the_game_mode == 3:
        agent_max = MaxAgent(agent1_position, agent2_position, game_mode, game_graph)
        agent_min = MinAgent(agent1_position, agent2_position, game_mode, game_graph)

    else:
        print("Invalid game mode")
        exit(0)

    agent_max.second_participator = agent_min
    agent_min.second_participator = agent_max

    # update state parameters
    game_graph.max_loc = agent1_position
    game_graph.min_loc = agent2_position

    game_graph.update_vertex_visit(agent1_position, arrival=True, agent_type=agent_max.agent_type)
    game_graph.update_vertex_visit(agent2_position, arrival=True, agent_type=agent_min.agent_type)

    return [agent_max, agent_min]


def simulate_game(agents: List[Agent], env: Graph):
    i = 0
    move_result = True
    while move_result:
        move_result = agents[i % 2].make_move(env)
        i += 1
    print("game ended")
    # print scores and moves history
    print("Max agent score: {}".format(env.max_score))
    print("Min agent score: {}".format(env.min_score))
    print("Max agent moves history: {}".format(agents[0].moves_history))
    print("Min agent moves history: {}".format(agents[1].moves_history))


if __name__ == '__main__':
    # parse graph environment
    # run with mode 1 and 3. agent 1 initial position=2, agent 2 initial position=4
    graph = Parser().parse_file_to_graph('difference_example_1_3.txt')

    # run with mode 1 and 2. agent 1 initial position=2, agent 2 initial position=3
    # graph = Parser().parse_file_to_graph('difference_example_1_2.txt')

    # print the graph
    graph.print_graph()

    # get the game mode and the agents first locations
    game_mode, agent1_loc, agent2_loc = get_init_user_prompt()

    # create the agents by game mode
    agents = create_agents(game_mode, agent1_loc, agent2_loc, graph)

    # run game simulations
    simulate_game(agents, graph)
