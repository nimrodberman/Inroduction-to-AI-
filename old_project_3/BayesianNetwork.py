from typing import Dict, List

from project3.Helpers import NodeTypes


class ProbTable:
    def __init__(self):
        self.prob_table: Dict = {}

    def add_prob(self, key_tuple: tuple, prob_value: float):
        if key_tuple[0] != NodeTypes.FIRST:
            if len(key_tuple) == 1:
                self.prob_table[key_tuple[0]] = prob_value
            else:
                self.prob_table[key_tuple] = prob_value
        else:
            self.prob_table[NodeTypes.FIRST] = prob_value

    def calculate_probability(self):
        # TODO - calculate the probability of the node given its parents
        pass

    def __str__(self) -> str:
        table_str = ""
        for key in self.prob_table.keys():
            table_str += str(key) + " " + str(self.prob_table[key]) + "\n"

        return table_str


class Node:
    def __init__(self, name: str, prob_table: ProbTable):
        self.name = name
        self.prob_table = prob_table

    def __str__(self):
        return "Name: {} \n ProbTable:\n{}".format(self.name, self.prob_table.__str__())


class BayesianNetwork:
    def __init__(self):
        self.parents: Dict[Node, List] = {}
        self.children: Dict[Node, List] = {}

    def add_variable_node(self, node: Node):

        # if the node is not in the dictionary, add it
        if not self.parents.get(node):
            self.parents[node] = []

        if not self.children.get(node):
            self.children[node] = []

    def add_causal_edge(self, parent_node: Node, children_node,
                        edge_weight: int):  # TODO - do we need to add the weight?

        if parent_node not in self.parents[children_node]:
            self.parents[children_node].append(parent_node)

        if children_node not in self.children[parent_node]:
            self.children[parent_node].append(children_node)

    def get_all_parents_nodes(self, variable_name: str) -> List[Node]:

        variable_node = self.get_variable(variable_name)
        return list(self.parents[variable_node])

    def get_variable(self, variable_name: str) -> Node:

        for var in self.children.keys():
            if var.name == variable_name:
                return var
