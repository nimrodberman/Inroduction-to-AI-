from project1.Agents import GreedyHeuristicAgent, AStarHeuristicAgent, AStarRealTimeHeuristicAgent
from project1.Enviroment import EnvironmentSimulator, HeuristicGraph
from project1.helpers import Parser, get_init_user_prompt

part1 = False
# agent_type = "AStarHeuristicAgent"
agent_type = "AStarRealTimeHeuristicAgent"
# agent_type = "HeuristicGreedyAgent"
agent_initial_vertex = 1
T = 0.0000001

if __name__ == '__main__':
    # parse graph environment
    graph = Parser().parse_file_to_graph('env.txt')

    # print the graph
    graph.print_graph()

    # get the agents
    if part1:
        agents = get_init_user_prompt(graph)
        simulator: EnvironmentSimulator = EnvironmentSimulator(graph, agents, T)
    else:
        heuristic_graph = HeuristicGraph(agent_initial_vertex, graph)
        graph.prt2_graph = heuristic_graph

        if agent_type == "HeuristicGreedyAgent":
            agents = [GreedyHeuristicAgent(1, agent_initial_vertex)]

        elif agent_type == "AStarHeuristicAgent":
            agents = [AStarHeuristicAgent(1, agent_initial_vertex)]

        else:
            agents = [AStarRealTimeHeuristicAgent(1, agent_initial_vertex)]

        simulator: EnvironmentSimulator = EnvironmentSimulator(heuristic_graph, agents, T)

    # start the simulation
    simulator.run_simulation()

