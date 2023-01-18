from p3.BayesianNetwork import BayesianNetwork, Node, ProbTable


class Parser:
    def __init__(self, path):
        self.path = path

    def parse_bayes_net(self) -> BayesianNetwork:
        # create empty bayes network
        bayes_net = BayesianNetwork()

        # read the file
        with open(self.path, 'r') as file:
            for l in file.readlines():
                # split each word in a line
                words = l.split(" ")

                # skip empty lines
                if len(words) == 0:
                    continue

                # classify lines and act accordingly
                if words[0] == "#V":
                    if words[2] != 'F':
                        raise Exception("Only F is supported")

                    # else create a new nodes
                    node_name = words[1]
                    # create blockage node
                    blockage_node_name = node_name + "_blockage"

                    # create evacuees node
                    evacuees_node_name = node_name + "_evacuees"
                    node_table = [[(node_name, False)], [(node_name, True)]]
                    node = Node(node_name, node_table)  # TODO - finish the table building
                    bayes_net.add_variable_node(node)

                if words[0] == "#E":
                    n1_name: str = words[1]
                    n2_name: str = words[2]
                    weight: int = int(words[3][1])
                    # TODO - finish the causal relation building

                if words[0] == "#W":
                    mild = float(words[1])
                    stormy = float(words[2])
                    extreme = float(words[3])

                    if mild + stormy + extreme != 1:
                        raise Exception("The probabilities must sum to 1")

                    w_prob_table = ProbTable()
                    # TODO - finish the weather table building and adding relations

                else:
                    raise Exception("Unknown line type")

        return bayes_net
