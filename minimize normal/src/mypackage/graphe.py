# Python implementation of Kosaraju's algorithm to print all SCCs
# https://www.geeksforgeeks.org/strongly-connected-components/
# https://www.geeksforgeeks.org/python-program-for-topological-sorting/

from collections import defaultdict
import time


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
        stack.append(v)

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
            if not visited[i]:
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
            if not visited[i]:
                self.topologicalSortUtil(i, visited, stack)

        # Print contents of stack
        return stack


# The code above is contributed by Neelam Yadav
# https://www.geeksforgeeks.org/strongly-connected-components/
# https://www.geeksforgeeks.org/python-program-for-topological-sorting/

# The code below is contributed by Thomas Brenart


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
                    if transition1[0] == element[0] and transition2[0] == element[1] and transition1[1] == transition2[
                        1]:
                        if ([transition1[2], transition2[2]] in distinguishable or [transition2[2], transition1[
                            2]] in distinguishable) and [transition1[0], transition2[0]] not in distinguishable:
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


def get_SCC_transition(SCC, A_prime):
    SCC_transition = []
    for state in SCC:
        for element in state:
            for transition in A_prime.transitions:
                if transition[0] == element:
                    for state2 in SCC:
                        if transition[2] in state2 and [state, '0', state2] not in SCC_transition:
                            if state != state2:
                                SCC_transition.append([state, '0', state2])

    return SCC_transition


def get_SCC_graph(A_prime):
    input_error = False
    SCC_states = get_SCC(A_prime)
    SCC_initial = []
    SCC_final = []
    SCC_transitions = get_SCC_transition(SCC_states, A_prime)

    for state in SCC_states:
        not_final = True

        if state[0][0] in A_prime.final_states:
            not_final = False

        for element in state:
            if element in A_prime.initial_state:
                SCC_initial = state
            if element in A_prime.final_states and not not_final and state not in SCC_final:
                SCC_final.append(state)
            if element in A_prime.final_states and not_final:
                input_error = True
            if element not in A_prime.final_states and not not_final:
                input_error = True

    if input_error:
        print("")
        print("############################################")
        print("input error : the given automata is not weak")
        print("############################################")
        return 0

    SCC_states = rewrite_SCC_states(SCC_states)
    SCC_initial = rewrite_SCC_state(SCC_initial)
    SCC_final = rewrite_SCC_states(SCC_final)
    SCC_transitions = rewrite_SCC_transitions(SCC_transitions)

    print("")
    print("")
    print("=======  SCC_Graph  =========")
    print("")
    print("SCC_states :")
    print(SCC_states)
    print("SCC_initial :")
    print(SCC_initial)
    print("SCC_final :")
    print(SCC_final)
    print("SCC_transitions :")
    print(SCC_transitions)
    print("")
    print("")

    SCC_graph = create_automata(SCC_states, '0', SCC_initial, SCC_final, SCC_transitions)
    return SCC_graph


def rewrite_SCC_states(SCC_states):
    new_SCC = []
    for state in SCC_states:
        string = ""
        i = 0
        for element in state:
            if i != 0:
                string = string + ("_")
            i = i+1
            string = string + (str(element))
        new_SCC.append(string)
    return new_SCC


def rewrite_SCC_state(SCC):
    new_SCC = []
    string = ""
    i = 0
    for element in SCC:
        if i != 0:
            string = string + ("_")
        i = i + 1
        string = string + (str(element))
    new_SCC.append(string)
    return new_SCC


def rewrite_SCC_transitions(SCC_transitions):
    new_SCC_transitions = []
    for transition in SCC_transitions:
        tmp = []
        for element in transition:
            if element != 0:
                tmp.append(rewrite_SCC_state(element))
            else:
                tmp.append('0')
        new_SCC_transitions.append((tmp[0][0], tmp[1][0], tmp[2][0]))
    return new_SCC_transitions


def topological_sort(SCC_graph):
    g = Graph(len(SCC_graph.states))
    for transition in SCC_graph.transitions:
        for i in range(len(SCC_graph.states)):
            for j in range(len(SCC_graph.states)):
                if SCC_graph.states[i] == transition[0] and SCC_graph.states[j] == transition[2]:
                    g.addEdge(i, j)
    sort = g.topologicalSort()
    return sort


def get_successor(v, SCC_graph):
    successor = []
    for transit in SCC_graph.transitions:
        if transit[0] == v and transit[2] != v and transit[2] not in successor:
            successor.append(transit[2])
    return successor


def isTransient(v, A_prime):
    touched_vertex = []
    old_vertex = []
    new_vertex = []

    list_ = []
    str_v = str(v)
    chars = list(str_v)
    for j in chars:
        list_.append(j)

    if "_" not in list_:
        for transition in A_prime.transitions:
            if transition[0] == v and transition[2] == v:
                return False
            if transition[0] == v:
                touched_vertex.append(transition[2])
                old_vertex.append(transition[2])
        add = True
        while add:
            add = False
            for transition in A_prime.transitions:
                if transition[0] in touched_vertex and transition[2] not in old_vertex:
                    new_vertex.append(transition[2])
                    old_vertex.append(transition[2])
                    add = True
                    if transition[2] == v:
                        return False
            touched_vertex = new_vertex
            new_vertex = []
        return True


def get_min_successor(v, SCC_graph, color_list):
    list_color_successor = []
    list_successor = get_successor(v, SCC_graph)
    for successor in list_successor:
        count = 0
        while successor != SCC_graph.states[count]:
            count += 1
        if color_list[count] != -1:
            list_color_successor.append(color_list[count][1])

    return min(list_color_successor)


def get_final_states_coloring(A_prime):
    inverted_sort = []
    SCC_graph = get_SCC_graph(A_prime)
    k = len(SCC_graph.states)
    if (k % 2) != 0:
        k += 1
    color_list = [-1] * len(SCC_graph.states)
    if SCC_graph == 0:
        return 0
    sort = topological_sort(SCC_graph)
    for i in sort:
        inverted_sort.insert(0, i)
    print("inverted_sort :")
    print(inverted_sort)
    for i in inverted_sort:
        if not get_successor(SCC_graph.states[i], SCC_graph):
            if SCC_graph.states[i] in SCC_graph.final_states:
                color_list[i] = [SCC_graph.states[i], k]
            else:
                color_list[i] = [SCC_graph.states[i], k - 1]
        else:
            h = get_min_successor(SCC_graph.states[i], SCC_graph, color_list)
            if isTransient(SCC_graph.states[i], A_prime):
                color_list[i] = [SCC_graph.states[i], h]
            else:
                if (h % 2) == 0 and SCC_graph.states[i] in SCC_graph.final_states:
                    color_list[i] = [SCC_graph.states[i], h]
                else:
                    if (h % 2) != 0 and SCC_graph.states[i] not in SCC_graph.final_states:
                        color_list[i] = [SCC_graph.states[i], h]
                    else:
                        color_list[i] = [SCC_graph.states[i], h - 1]

    print("color_list :")
    print(color_list)
    print("")

    color_final_states = []

    for color in color_list:
        if color[1] % 2 == 0:
            color_final_states.append(color[0])

    return color_final_states


def minimize(A_prime):
    list_pair = get_pair(A_prime)

    distinguishable, not_distinguishable = get_distinguishable(A_prime, list_pair)

    list_blocks = create_blocks(A_prime, not_distinguishable)

    new_automata_transition = build_new_automata(A_prime, list_blocks)

    initial_state_new_automata = get_start(A_prime, list_blocks)

    final_state_new_automata = get_end(A_prime, list_blocks)

    list_blocks = rewrite_SCC_states(list_blocks)
    initial_state_new_automata = rewrite_SCC_state(initial_state_new_automata[0])
    final_state_new_automata = rewrite_SCC_states(final_state_new_automata)
    new_automata_transition = rewrite_SCC_transitions(new_automata_transition)

    new_automata = create_automata(list_blocks, A_prime.symbols, initial_state_new_automata, final_state_new_automata,
                                   new_automata_transition)

    return new_automata


def main():
    list_file = {"weakgraph1.txt"}
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

        final_states_coloring = get_final_states_coloring(A_prime)

        list_final = []
        for element in final_states_coloring:
            fsc = str(element)
            chars = list(fsc)
            for j in chars:
                if j != "_":
                    list_final.append(j)

        coloring_automata = create_automata(A_prime.states, A_prime_symbols, A_prime_initial_state,
                                            list_final, A_prime_transitions)

        print("")
        print("==================================================")
        print("")
        print("coloring Automata : ")
        print("A_states : ")
        print(*coloring_automata.states)
        print("A_symbols : ")
        print(*coloring_automata.symbols)
        print("A_initial_state : ")
        print(*coloring_automata.initial_state)
        print("A_final_states : ")
        print(*coloring_automata.final_states)
        print("A_transitions : ")
        print(*coloring_automata.transitions)
        print("")
        print("")

        new_automata = minimize(coloring_automata)

        print("")
        print("==================================================")
        print("")
        print("output Minimized Automata : ")
        print("A_states : ")
        print(*new_automata.states)
        print("A_symbols : ")
        print(*new_automata.symbols)
        print("A_initial_state : ")
        print(*new_automata.initial_state)
        print("A_final_states : ")
        print(*new_automata.final_states)
        print("A_transitions : ")
        print(*new_automata.transitions)
        print("")
        print("")


if __name__ == '__main__':
    start = time.time()
    main()
    print("execution time : " + str(time.time() - start) + " sec")
