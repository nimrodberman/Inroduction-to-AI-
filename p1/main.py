from p1.Enviorment import EnvironmentSimulator
from p1.helpers import Parser, get_init_user_prompt

if __name__ == '__main__':
    # parse graph environment
    graph = Parser().parse_file_to_graph('env.txt')

    # print the graph
    graph.print_graph()

    # get the agents
    agents = get_init_user_prompt(graph)

    # init the simulator
    simulator = EnvironmentSimulator(graph, agents)

    # run the simulation
    simulator.run_simulation()
