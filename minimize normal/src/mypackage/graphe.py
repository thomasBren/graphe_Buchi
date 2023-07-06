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

    # le cas où état final et pas final dans le même block

    for element in list_blocks:
        new_block = []
        if element[0] in A_prime.final_states:
            for sub_element in element:
                print(element)
                print(sub_element)
                if sub_element not in A_prime.final_states:
                    new_block.append(sub_element)
        if element[0] not in A_prime.final_states:
            for sub_element in element:
                if sub_element in A_prime.final_states:
                    new_block.append(sub_element)
        if len(new_block) != 0:
            list_blocks.append(new_block)
            for sub_element in new_block:
                element.remove(sub_element)

    print(list_blocks)
    return list_blocks

def build_new_automata(A_prime, list_blocks):

    new_automata_transition = []

    for element in list_blocks:
        for transition in A_prime.transitions:
            if transition[0] == element[0]:
                for element2 in list_blocks:
                    if transition[2] in element2:
                        new_automata_transition.append([element, transition[1], element2])

    return new_automata_transition

def get_start(A_prime, list_blocks):

    initial_state_new_automata = []

    for block in list_blocks:
        for element in block:
            if element in A_prime.initial_state and block not in initial_state_new_automata:
                initial_state_new_automata.append(block)

    return initial_state_new_automata

def get_end(A_prime, list_blocks):

    final_state_new_automata = []

    for block in list_blocks:
        for element in block:
            if element in A_prime.final_states and block not in final_state_new_automata:
                final_state_new_automata.append(block)

    return final_state_new_automata




def minimize(A_prime):
    list_pair = get_pair(A_prime)
    #print("pair : ")
    #print(list_pair)

    distinguishable, not_distinguishable = get_distinguishable(A_prime, list_pair)

    #print("distinguishable :")
    #print(distinguishable)
    #print("not_distinguishable :")
    #print(not_distinguishable)

    list_blocks = create_blocks(A_prime, not_distinguishable)
    #print("list_blocks :")
    #print(list_blocks)

    new_automata_transition = build_new_automata(A_prime, list_blocks)
    #print("new_automata_transition :")
    #print(new_automata_transition)

    initial_state_new_automata = get_start(A_prime, list_blocks)
    #print("initial_state_new_automata :")
    #print(initial_state_new_automata)

    final_state_new_automata = get_end(A_prime, list_blocks)
    #print("final_state_new_automata :")
    #print(final_state_new_automata)

    new_automata = create_automata(list_blocks, A_prime.symbols, initial_state_new_automata, final_state_new_automata,
                              new_automata_transition)

    return new_automata


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

        new_automata = minimize(A_prime)
    """
    print("")
    print("==================================================")
    print("")
    print("output Automata : ")
    print("A_states : ")
    for element in new_automata.states:
        print(element)
    print("A_symbols : ")
    print(*new_automata.symbols)
    print("A_initial_state : ")
    print(*new_automata.initial_state)
    print("A_final_states : ")
    print(*new_automata.final_states)
    print("A_transitions : ")
    for element in new_automata.transitions:
        print(element)
    print("")
    print("")
    print("==================================================")
    """

if __name__ == '__main__':
    main()
