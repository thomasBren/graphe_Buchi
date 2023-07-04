from z3 import *


class Automata:
    def __init__(self, states, symbols, initial_state, final_states, transitions):
        self.states = states
        self.symbols = symbols
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions


class AutomataError(Exception):

    def __init__(self, f, *args):
        super().__init__(args)
        self.f = f

    def __str__(self):
        return f'Error found in the {self.f} input'


def create_automata(states, symbols, initial_state, final_states, transitions):
    if not (initial_state[0] in states):
        raise AutomataError("initial_state")
    for final_state in final_states:
        if not (final_state in states):
            raise AutomataError("final_states")
    for transition in transitions:
        if not (transition[0] in states) or not (transition[2] in states) or not (transition[1] in symbols):
            raise AutomataError("transitions")

    return Automata(states, symbols, initial_state, final_states, transitions)


def transitions_in_A(A_states, A_symbols):
    # crée la liste de toutes les A_prime_transitions possible dans le graphe A
    A_transitions = []
    for q in range(len(A_states)):
        A_transitions += [[]]
        for s in range(len(A_symbols)):
            A_transitions[q] += [[]]
            for q2 in range(len(A_states)):
                A_transitions[q][s] += [
                    Bool("A_transition " + ": (" + str(q) + "," + str(A_symbols[s]) + "," + str(q2) + ")")]
                # print("A_transition" + str(q) + str(s) + str(q2))
    return A_transitions


def get_pair(A_prime):
    list_pair = []

    for element in A_prime.states:
        for element2 in A_prime.states:
            if (element != element2) & ([element2, element] not in list_pair):
                list_pair.append([element, element2])
    return list_pair


def get_distinguishable(A_prime, list_pair):
    distinguishable = []
    not_distinguishable = []
    add = True

    for element in list_pair:
        if (element[0] in A_prime.final_states and element[1] not in A_prime.final_states) or (
                element[1] in A_prime.final_states and element[0] not in A_prime.final_states):
            distinguishable.append(element)

    while add:
        add = False
        for element in list_pair:
            for transition1 in A_prime.transitions:
                for transition2 in A_prime.transitions:
                    if transition1[0] == element[0] and transition2[0] == element[1] and transition1[1] == transition2[1]:
                        if ([transition1[2], transition2[2]] in distinguishable or [transition2[2], transition1[2]] in distinguishable) and [transition1[0], transition2[0]] not in distinguishable:
                            distinguishable.append(element)
                            add = True

    for element in list_pair:
        if element not in distinguishable:
            not_distinguishable.append(element)
    return distinguishable, not_distinguishable


def create_blocks(A_prime, not_distinguishable):
    list_blocks = []
    for element in not_distinguishable:
        placed = False
        for block in list_blocks:
            if element[0] in block or element[1] in block:
                placed = True
                if element[0] not in block:
                    block.append(element[0])
                if element[1] not in block:
                    block.append(element[1])
        if not placed:
            list_blocks.append(element)

    for element in A_prime.states:
        placed = False
        for block in list_blocks:
            if element in block:
                placed = True
        if not placed:
            list_blocks.append(element)

    return list_blocks




def minimize(A_prime):
    list_pair = get_pair(A_prime)
    print("pair : ")
    print(list_pair)

    distinguishable, not_distinguishable = get_distinguishable(A_prime, list_pair)

    print("distinguishable :")
    print(distinguishable)
    print("not_distinguishable :")
    print(not_distinguishable)

    list_blocks = create_blocks(A_prime, not_distinguishable)
    print("list_blocks :")
    print(list_blocks)

    return None


def main():
    list_file = {"A.txt"}
    for i in list_file:
        print("Input Automata from file " + i)
        print("")
        input = open("../input_graphe/" + i, "r")
        A_prime_states = list(input.readline().split())
        print("A_prime_states : ")
        print(*A_prime_states)
        A_prime_symbols = list(input.readline().split())
        print("A_prime_symbols : ")
        print(*A_prime_symbols)
        A_prime_initial_state = list(input.readline().split())
        print("A_prime_initial_state : ")
        print(*A_prime_initial_state)
        A_prime_final_states = list(input.readline().split())
        print("A_prime_final_states : ")
        print(*A_prime_final_states)
        A_prime_transitions = []
        for line in input:
            line = line.strip()
            if line:
                prime_transition = tuple(line.split())
                A_prime_transitions.append(prime_transition)
        print("A_prime_transitions : ")
        print(*A_prime_transitions)

        try:
            A_prime = create_automata(A_prime_states, A_prime_symbols, A_prime_initial_state, A_prime_final_states,
                                      A_prime_transitions)
        except AutomataError as ex:
            print(ex)
            return 0

        automata = minimize(A_prime)


if __name__ == '__main__':
    main()
