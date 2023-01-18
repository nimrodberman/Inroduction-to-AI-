from enum import Enum
from Global import p1, p2


# __________ Helper types __________
class WeatherTypes(Enum):
    MILD = 1
    STORMY = 2
    EXTREME = 3


class VertexTypes:
    WEATHER = "W"
    BLOCKAGE = "B"
    EVACUEES = "E"


# __________ helper functions __________
def get_vertex_type(vertex):
    if VertexTypes.EVACUEES in vertex:
        return VertexTypes.EVACUEES

    if VertexTypes.BLOCKAGE in vertex:
        return VertexTypes.BLOCKAGE

    if VertexTypes.WEATHER in vertex:
        return VertexTypes.WEATHER


def noisyOr(vertex, v_neighbors):
    q = 1
    if vertex[0]:
        q *= p2

    i = 1
    while i < len(vertex):
        if vertex[i]:
            q *= min(1, p1 * v_neighbors[i][1])
        i += 1

    return 1 - q


def get_user_prompt() -> int:
    print("Please enter the number of the desired action:")
    print("1. Reset evidence")
    print("2. Add piece of evidence to the evidence bank")
    print("3. Do probabilistic reasoning")
    print("4. Exit")

    # if input is different than 1-4, ask again exit
    try:
        user_input = int(input())
        if 1 <= user_input <= 4:
            return user_input
    except Exception as e:
        raise Exception("Invalid input {}".format(e))


def get_user_evidence() -> int:
    print("Please add the number of the desired evidence:")
    print("1. Weather Status")
    print("2. Saw a person")
    print("3. Saw a blockage")

    # if input is different than 1-3, ask again exit
    try:
        user_input = int(input())
        if 1 <= user_input <= 3:
            return user_input
    except Exception as e:
        raise Exception("Invalid input {}".format(e))


def get_user_inference() -> int:
    print("Please add the number of the desired inference:")
    print("1. What is the probability that each of the vertices contains evacuees?")
    print("2. What is the probability that each of the vertices is blocked?")
    print("3. What is the distribution of the weather variable?")
    print("4. What is the probability that a certain path (set of edges) is free from blockages?")
    print("5. What is the path from a given location to a goal that"
          " has the highest probability of being free from blockages?")

    # if input is different than 1-5, ask again exit
    try:
        user_input = int(input())
        if 1 <= user_input <= 5:
            return user_input
    except Exception as e:
        raise Exception("Invalid input {}".format(e))


def handle_evidence_creating(e_type):
    if e_type == 1:
        e_key = VertexTypes.WEATHER
        print("Please enter the weather status:")
        print("1. Mild")
        print("2. Stormy")
        print("3. Extreme")
        e_value = int(input())
        return e_key, e_value

    elif e_type == 2:
        # enter the location of the person
        print("Please enter the location of the person:")
        e_key = VertexTypes.EVACUEES + input()
        e_value = True

        return e_key, e_value

    elif e_type == 3:
        pass
    else:
        raise Exception("Invalid evidence type {}".format(e_type))
