# Python implementation of Kosaraju's algorithm to print all SCCs
# https://www.geeksforgeeks.org/strongly-connected-components/
# https://www.geeksforgeeks.org/python-program-for-topological-sorting/

from collections import defaultdict


# This class represents a directed graph using adjacency list representation
class Graph:
    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = defaultdict(list)  # default dictionary to store graph

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # A function used by DFS
    def DFSUtil(self, v, visited, list):
        # Mark the current node as visited and print it
        visited[v] = True
        list.append(v)
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if not visited[i]:
                self.DFSUtil(i, visited, list)

    def fillOrder(self, v, visited, stack):
        # Mark the current node as visited
        visited[v] = True
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if not visited[i]:
                self.fillOrder(i, visited, stack)
        stack = stack.append(v)

    # Function that returns reverse (or transpose) of this graph
    def getTranspose(self):
        g = Graph(self.V)

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph:
            for j in self.graph[i]:
                g.addEdge(j, i)
        return g

    # The main function that finds and prints all strongly
    # connected components
    def find_SCCs(self):
        SCC = []

        stack = []
        # Mark all the vertices as not visited (For first DFS)
        visited = [False] * self.V
        # Fill vertices in stack according to their finishing
        # times
        for i in range(self.V):
            if not visited[i]:
                self.fillOrder(i, visited, stack)

        # Create a reversed graph
        gr = self.getTranspose()

        # Mark all the vertices as not visited (For second DFS)
        visited = [False] * self.V

        # Now process all vertices in order defined by Stack
        while stack:
            i = stack.pop()
            if not visited[i]:
                list = []
                gr.DFSUtil(i, visited, list)
                SCC.append(list)
        return SCC

    # A recursive function used by topologicalSort
    def topologicalSortUtil(self, v, visited, stack):

        # Mark the current node as visited.
        visited[v] = True

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)

        # Push current vertex to stack which stores result
        stack.insert(0, v)

    # The function to do Topological Sort. It uses recursive
    # topologicalSortUtil()
    def topologicalSort(self):
        # Mark all the vertices as not visited
        visited = [False] * self.V
        stack = []

        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        for i in range(self.V):
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)

        # Print contents of stack
        print(stack)

# The code above is contributed by Neelam Yadav
# https://www.geeksforgeeks.org/strongly-connected-components/
# https://www.geeksforgeeks.org/python-program-for-topological-sorting/

# The code below is contributed by Thomas Brenart

def get_SCC(A_prime):
    g = Graph(len(A_prime.states))
    for transition in A_prime.transitions:
        for i in range(len(A_prime.states)):
            for j in range(len(A_prime.states)):
                if A_prime.states[i] == transition[0] and A_prime.states[j] == transition[2]:
                    g.addEdge(i, j)
    SCC = g.find_SCCs()
    

    new_SCC = []
    for sub_graph in SCC:
        sub = []
        for element in sub_graph:
            sub.append(A_prime.states[element])
        new_SCC.append(sub)
    return new_SCC


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
    # print("pair : ")
    # print(list_pair)

    distinguishable, not_distinguishable = get_distinguishable(A_prime, list_pair)

    # print("distinguishable :")
    # print(distinguishable)
    # print("not_distinguishable :")
    # print(not_distinguishable)

    list_blocks = create_blocks(A_prime, not_distinguishable)
    # print("list_blocks :")
    # print(list_blocks)

    new_automata_transition = build_new_automata(A_prime, list_blocks)
    # print("new_automata_transition :")
    # print(new_automata_transition)

    initial_state_new_automata = get_start(A_prime, list_blocks)
    # print("initial_state_new_automata :")
    # print(initial_state_new_automata)

    final_state_new_automata = get_end(A_prime, list_blocks)
    # print("final_state_new_automata :")
    # print(final_state_new_automata)

    new_automata = create_automata(list_blocks, A_prime.symbols, initial_state_new_automata, final_state_new_automata,
                                   new_automata_transition)

    return new_automata


def main():
    list_file = {"SCC.txt"}
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

        SCC = get_SCC(A_prime)
        print(SCC)

        new_automata = minimize(A_prime)
    """
    print("")
    print("==================================================")
    print("")
    print("output Minimized Automata : ")
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
