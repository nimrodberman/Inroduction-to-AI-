from p3.BayesianNetwork import BayesianNetwork
from p3.Enviornmnet import WorldGraph
from p3.Helpers import get_user_prompt, get_user_evidence, handle_evidence_creating, get_user_inference, VertexTypes
from p3.InferenceAlgorithms import enumeration_ask, enumerate_path
from p3.Parsers import Parser
import Global

input_path = Global.input_path
# part 1 - define the p1, p2.
p1 = Global.p1
p2 = Global.p2

if __name__ == '__main__':
    # __________ part 1  __________
    # light representation of the environment for display and debug purposes.
    world: WorldGraph = Parser(input_path).parse_world()

    # bayesian network representation of the environment.
    bayesian_network: BayesianNetwork = Parser(input_path).parse_bayes_net(world)

    # print the bayesian network instance
    bayesian_network.print_network()

    # __________ part 2  __________
    evidence_bank = {}
    # get from the user prompt
    while 1:
        user_input = get_user_prompt()
        if user_input == 4:
            print("Exiting...")
            exit(0)

        elif user_input == 1:
            evidence_bank = {}
            print("Evidence bank was reset")

        elif user_input == 2:
            input_evidence = get_user_evidence()
            e_key, e_value = handle_evidence_creating(input_evidence)
            evidence_bank[e_key] = e_value

        elif user_input == 3:
            user_inference_type = get_user_inference()

            if user_inference_type == 1:
                print("You have asked to know what is the probability that each of the vertices contains evacuees")
                print("The Answer:")
                i = 1
                while i < bayesian_network.world_vertices_num + 1:
                    x = "{}{}".format(VertexTypes.EVACUEES, i)
                    ans = enumeration_ask(x, evidence_bank, bayesian_network, world)[0]
                    print("{}: {}".format(x, ans))
                    i += 1

                print("__________________\n")

            elif user_inference_type == 2:
                print("You have asked to know what is the probability that each of the vertices is blocked")
                print("The Answer:")
                i = 1
                while i < bayesian_network.world_vertices_num + 1:
                    x = "{}{}".format(VertexTypes.BLOCKAGE, i)
                    ans = enumeration_ask(x, evidence_bank, bayesian_network, world)[0]
                    print("{}: {}".format(x, ans))
                    i += 1

                print("__________________\n")

            elif user_inference_type == 3:
                print("You have asked to know what is the distribution of the weather variable?")
                print("The Answer:")
                ans = enumeration_ask(VertexTypes.WEATHER, evidence_bank, bayesian_network, world)
                print("Mild: {}".format(ans[0]))
                print("Stormy: {}".format(ans[1]))
                print("Extreme: {}".format(ans[2]))

                print("__________________\n")

            elif user_inference_type == 4:
                print("You have asked to know"
                      " what is the probability that a certain path (set of edges) is free from blockages")
                path = input("Please enter the edges e.g. 123 (means go from E1 then from E2 then from E3)")
                print("The Answer:")
                path_lst = [x for x in path]
                path_lst = world.from_edges_to_vertices(path_lst)
                ans = enumerate_path(path, evidence_bank, bayesian_network, world)

                print(ans)
                print("__________________\n")

            else:
                print("You have asked to know what is the path from a given"
                      " location to a goal that has the highest probability of being free from blockages")
                source = int(input("source vertex"))
                goal = int(input("goal vertex"))

                all_paths = world.find_all_paths(source, goal)
                scores = {}
                for path in all_paths:
                    scores[str(path)] = enumerate_path(path, evidence_bank, bayesian_network, world)

                high = -1
                best_p = ""
                best_s = 0
                for p in scores:
                    if scores[p] > high:
                        high = scores[p]
                        best_s = scores[p]
                        best_p = p

                print("The Answer:")
                print("The best path is {} with probability of {}".format(best_p, best_s))
                print("__________________\n")
