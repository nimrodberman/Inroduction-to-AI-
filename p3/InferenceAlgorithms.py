# ____________ helper functions ____________ #
import copy
from typing import Dict

from p3.BayesianNetwork import BayesianNetwork
from p3.Enviornmnet import WorldGraph
from p3.Helpers import VertexTypes, WeatherTypes, get_vertex_type
from p3.Parsers import create_table_entry_key, n_create


def get_p_in_e(y, e, bn):
    lst = []
    is_y_has_parents = bn.has_parents(y)
    if is_y_has_parents:
        for p in bn.children_vertices[y]:
            if p in e.keys():
                lst.append(p)
    return lst


def probability_calculations(user_interface_type, evidence_bank, bayesian_network, path=None):
    # path is only for inference 4
    if user_interface_type == 1:
        pass
    elif user_interface_type == 2:
        pass
    elif user_interface_type == 3:
        pass
    elif user_interface_type == 4:
        pass
    else:
        pass


def extend_evidence(e, x):
    if VertexTypes.EVACUEES == get_vertex_type(x) or VertexTypes.BLOCKAGE == get_vertex_type(x):
        e0 = copy.deepcopy(e)
        e0[x] = True
        e1 = copy.deepcopy(e)
        e1[x] = False
        return e0, e1

    else:
        e0 = copy.deepcopy(e)
        e0[x] = WeatherTypes.MILD
        e1 = copy.deepcopy(e)
        e1[x] = WeatherTypes.STORMY
        e2 = copy.deepcopy(e)
        e2[x] = WeatherTypes.EXTREME
        return e0, e1, e2


def elimination_ask_helper(k, x, e, bn):
    # the node is not equal to the key and not in the evidence and don't have successors
    # or is it a root of the evidence
    return ((k != x) and (k not in e.keys()) and (not bn.has_children(k))) or \
           ((k in e.keys()) and (not bn.has_parents(k)))


def extend_vars(e, x, bn: BayesianNetwork):
    vrs = {}

    if VertexTypes.WEATHER not in e.keys():
        vrs[VertexTypes.WEATHER] = bn.get_vertex(VertexTypes.WEATHER)

    for k in bn.vertices:
        if (VertexTypes.BLOCKAGE == get_vertex_type(k) or VertexTypes.EVACUEES == get_vertex_type(k)) \
                and not elimination_ask_helper(k, x, e, bn):
            vrs[k] = bn.get_vertex(k)

    return vrs


def normalize_q(q):
    alpha = sum(q)
    return [item / alpha for item in q]


def take_first(vrs):
    return list(vrs.keys())[0]


def take_rest(vrs, y):
    rest = copy.deepcopy(vrs)
    rest.pop(y)
    return rest


def calculate_bayesian_probabilities(bn, p, v, a, e, w):
    prob = -1

    # if its a weather vertex
    if get_vertex_type(v) == VertexTypes.WEATHER:
        return bn.get_vertex(v).prob_table[a]

    # if its a evacuees vertex
    elif get_vertex_type(v) == VertexTypes.EVACUEES:
        v_id = int(v[1])
        ngb = [it[0] for it in w.get_vertex(v_id).neighbors] + [v_id]
        # get y parents
        ngb.sort()
        values = [e["{}{}".format(VertexTypes.BLOCKAGE, i)] for i in ngb]
        table_key = create_table_entry_key(values, [[i, 0] for i in ngb])
        prob = bn.get_vertex(v).prob_table[table_key]
        if a:
            return prob
        else:
            return 1.0 - prob
    # its a block
    else:
        if p:
            prob = bn.get_vertex(v).prob_table[e[p[0]]]
            if a:
                return prob
            else:
                return 1.0 - prob


# ____________ algorithms ____________ #
def enumerate_path(path, e, bn, w):
    pt, e0 = copy.deepcopy(path), copy.deepcopy(e)
    if not pt:
        return -1
    if len(pt) == 1:
        return enumeration_ask("{}{}".format(VertexTypes.BLOCKAGE, path[0]), e0, bn, w)[1]
    else:
        i = 1
        while i < len(path):
            e0["{}{}".format(VertexTypes.BLOCKAGE, path[i])] = False
            i += 1
        return enumerate_path(pt[1:], e, bn, w) * \
               enumeration_ask("{}{}".format(VertexTypes.BLOCKAGE, path[0]), e0, bn, w)[1]


def enumerate_all(vrs, e, bn: BayesianNetwork, w: WorldGraph):
    # if empty return 1
    if not vrs:
        return 1.0

    # take the first part of the variables
    y = take_first(vrs)
    y_p_in_e = get_p_in_e(y, e, bn)

    # take the rest of the variables
    y_rest = take_rest(vrs, y)

    # if y is already at the evidence
    if y in e.keys():
        return calculate_bayesian_probabilities(bn, y_p_in_e, y, e[y], e, w) * enumerate_all(y_rest, e, bn, w)

    # if y is not at the evidence
    else:
        # if y is a Edge or Blockage vertex
        if get_vertex_type(y) == VertexTypes.EVACUEES or get_vertex_type(y) == VertexTypes.BLOCKAGE:
            e0, e1 = extend_evidence(e, y)
            tr = calculate_bayesian_probabilities(bn, y_p_in_e, y, True, e0, w) * enumerate_all(y_rest, e0, bn, w)
            fls = calculate_bayesian_probabilities(bn, y_p_in_e, y, False, e1, w) * enumerate_all(y_rest, e1, bn, w)
            return sum([tr, fls])

        # if y is a Weather vertex
        else:
            e0, e1, e2 = extend_evidence(e, y)
            mild = bn.get_vertex(y).prob_table[WeatherTypes.MILD] * enumerate_all(y_rest, e0, bn, w)
            stormy = bn.get_vertex(y).prob_table[WeatherTypes.STORMY] * enumerate_all(y_rest, e1, bn, w)
            extreme = bn.get_vertex(y).prob_table[WeatherTypes.EXTREME] * enumerate_all(y_rest, e2, bn, w)
            return sum([mild, stormy, extreme])


def enumeration_ask(x, e: Dict, bn: BayesianNetwork, w: WorldGraph):
    if VertexTypes.EVACUEES == get_vertex_type(x) or VertexTypes.BLOCKAGE == get_vertex_type(x):
        q = [-1, -1]
        e0, e1 = extend_evidence(e, x)
        q[0] = enumerate_all(extend_vars(e0, x, bn), e0, bn, w)
        q[1] = enumerate_all(extend_vars(e1, x, bn), e1, bn, w)

    else:
        q = [-1, -1, -1]
        e0, e1, e2 = extend_evidence(e, x)
        q[0] = enumerate_all(extend_vars(e0, x, bn), e0, bn, w)
        q[1] = enumerate_all(extend_vars(e1, x, bn), e1, bn, w)
        q[2] = enumerate_all(extend_vars(e2, x, bn), e2, bn, w)

    return normalize_q(q)
