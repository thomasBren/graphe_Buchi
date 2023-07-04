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


def getAPrimeFollowers(q_, s, transitions):
    followers = []
    for transition in transitions:
        if transition[0] == "q" + str(q_):
            if transition[1] == str(s):
                # print(transition)
                # print("q"+str(q_))
                # print(str(s))
                # print(int (transition[2].split("q")[1]))
                followers += [int(transition[2].split("q")[1])]
    # print(followers)
    return followers


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


def vertex_G(A_states, A_prime_states):
    # crée la liste les sommets du graphe G possibles
    G_states = []
    for q in range(len(A_states)):
        G_states += [[]]
        for q_ in range(len(A_prime_states)):
            G_states[q] += [Bool("G : (" + str(q) + "," + str(q_) + ")")]
            # print("G" + str(q) + str(q_))
    return G_states


def path_G(A_states, A_prime_states):
    # crée la liste de tout les path A et N possibles pour dans G
    A_path = []
    N_path = []
    for q1 in range(len(A_states)):
        A_path += [[]]
        N_path += [[]]
        for q1_ in range(len(A_prime_states)):
            A_path[q1] += [[]]
            N_path[q1] += [[]]
            for q2 in range(len(A_states)):
                A_path[q1][q1_] += [[]]
                N_path[q1][q1_] += [[]]
                for q2_ in range(len(A_prime_states)):
                    A_path[q1][q1_][q2] += [
                        Bool("A_path : (" + str(q1) + "," + str(q1_) + "," + str(q2) + "," + str(q2_) + ")")]
                    N_path[q1][q1_][q2] += [
                        Bool("N_path : (" + str(q1) + "," + str(q1_) + "," + str(q2) + "," + str(q2_) + ")")]
                    # print("A_path" + str(q1) + str(q1_) + str(q2) + str(q2_))
                    # print("N_path" + str(q1) + str(q1_) + str(q2) + str(q2_))
    return A_path, N_path


def affichage_path(model, A_states, A_prime_states):
    for a in range(len(A_states)):
        for b in range(len(A_prime_states)):
            for c in range(len(A_states)):
                for d in range(len(A_prime_states)):
                    print("--------------------------------------")
                    for i in model:
                        # print(repr(i).split(":")[1])
                        # print(" (" + str(a) + "," + str(b) + "," + str(c) + "," + str(d) + ")")

                        if repr(i).split(":")[0] == "A_path " and repr(i).split(":")[1] == " (" + str(a) + "," + str(
                                b) + "," + str(c) + "," + str(d) + ")":
                            print(str(i) + " " + str(is_true(model[i])))
                        if repr(i).split(":")[0] == "N_path " and repr(i).split(":")[1] == " (" + str(a) + "," + str(
                                b) + "," + str(c) + "," + str(d) + ")":
                            print(str(i) + " " + str(is_true(model[i])))
                    print("")


def affichage_transition(model):
    print("")
    for i in model:
        if repr(i).split(":")[0] == "A_transition ":
            print(i)
            print(is_true(model[i]))


def affichage_G_states(model):
    print("")
    for i in model:
        if repr(i).split(":")[0] == "G ":
            print(i)
            print(is_true(model[i]))


def affichage_final_states_a(model):
    print("")
    for i in model:
        if repr(i).split(":")[0] == "A_final_states ":
            print(i)
            print(is_true(model[i]))


def final_states_of_A(A_states):
    # crée la liste de tout les état finaux possibles pour A

    A_final_states = []
    for q1 in range(len(A_states)):
        A_final_states += [Bool("A_final_states : " + str(q1))]
        # print("A_final_states : " + str(q1))
    return A_final_states


def minimize(A_prime):
    # print("")
    # print("New automata : ")

    A_states = []
    for i in range(len(A_prime.states) - 1):
        A_states.append("q" + str(i))
    # print("A_states : ")
    # print(*A_states)
    A_symbols = A_prime.symbols
    # print("A_symbols : ")
    # print(*A_symbols)
    A_initial_state = ["q0"]
    # print("A_initial_state : ")
    # print(*A_initial_state)

    A_transitions = transitions_in_A(A_states, A_symbols)
    G_states = vertex_G(A_states, A_prime.states)
    A_path, N_path = path_G(A_states, A_prime.states)
    A_final_states = final_states_of_A(A_states)
    sol = Solver()

    # clause 1

    for q1 in range(len(A_states)):
        for s in range(len(A_symbols)):
            transit = []
            for q2 in range(len(A_states)):
                transit += [A_transitions[q1][s][q2]]
            sol.add(Or(transit))  # au moins 1
            # print(Or(transit))

    # au max 1 par definition du graphe A fonction total (?)
    for q1 in range(len(A_states)):
        for s in range(len(A_symbols)):
            for q2 in range(len(A_states)):
                for q3 in range(len(A_states)):
                    if q2 != q3:
                        sol.add(Implies(A_transitions[q1][s][q2], Not(A_transitions[q1][s][q3])))
                        # print(Implies(A_transitions[q1][s][q2],Not(A_transitions[q1][s][q3])))

    # clause 2

    for q1 in range(len(A_states)):
        for q_ in range(len(A_prime.states)):
            # print(new_G_states[q1][q_])
            for q2 in range(len(A_states)):
                for s in range(len(A_prime.symbols)):
                    followers = getAPrimeFollowers(q_, s, A_prime.transitions)
                    for follower in followers:  # pas opti
                        # if q1==0 and q_==0:
                        # print(str(q1) +" "+ str(q_))
                        # print(str(q1) +" "+ str(s)+" "+str(q2))
                        # print(str(q2) + " "+str(follower))

                        sol.add(Implies(And(G_states[q1][q_], A_transitions[q1][s][q2]), G_states[q2][follower]))
                        # print(Implies(And(G_states[q1][q_], A_transitions[q1][s][q2]), G_states[q2][follower]))

    # clause 3

    for q1 in range(len(A_states)):
        for q2 in range(len(A_states)):
            for q3 in range(len(A_states)):
                for q1_ in range(len(A_prime.states)):
                    for q2_ in range(len(A_prime.states)):
                        for s in range(len(A_prime.symbols)):
                            followers = getAPrimeFollowers(q2_, s, A_prime.transitions)
                            for follower in followers:  # pas opti
                                if A_prime.states[follower] not in A_prime.final_states:
                                    if q1 != q3 or q1_ != follower:
                                        sol.add(Implies(And(N_path[q1][q1_][q2][q2_], A_transitions[q2][s][q3]),
                                                        N_path[q1][q1_][q3][follower]))

    # clause 4

    for q1 in range(len(A_states)):
        for q2 in range(len(A_states)):
            for q1_ in range(len(A_prime.states)):
                for q2_ in range(len(A_prime.states)):
                    for s in range(len(A_prime.symbols)):
                        followers = getAPrimeFollowers(q2_, s, A_prime.transitions)
                        for follower in followers:  # pas opti
                            if A_prime.states[q1_] not in A_prime.final_states and q1_ == follower:
                                sol.add(Implies(And(N_path[q1][q1_][q2][q2_], A_transitions[q2][s][q1]),
                                                Not(A_final_states[q1])))

    # clause 5

    for q1 in range(len(A_states)):
        for q2 in range(len(A_states)):
            for q3 in range(len(A_states)):
                for q1_ in range(len(A_prime.states)):
                    for q2_ in range(len(A_prime.states)):
                        for s in range(len(A_prime.symbols)):
                            followers = getAPrimeFollowers(q2_, s, A_prime.transitions)
                            for follower in followers:  # pas opti
                                if A_prime.states[q1_] in A_prime.final_states:
                                    if q1 != q3 or q1_ != follower:
                                        # print(Implies(And(A_path[q1][q1_][q2][q2_], A_transitions[q2][s][q3], Not(A_final_states[q3])), A_path[q1][q1_][q3][follower]))
                                        sol.add(Implies(And(A_path[q1][q1_][q2][q2_], A_transitions[q2][s][q3],
                                                            Not(A_final_states[q3])),
                                                        A_path[q1][q1_][q3][follower]))

    # clause 6

    for q1 in range(len(A_states)):
        for q2 in range(len(A_states)):
            for q1_ in range(len(A_prime.states)):
                for q2_ in range(len(A_prime.states)):
                    for s in range(len(A_prime.symbols)):
                        followers = getAPrimeFollowers(q2_, s, A_prime.transitions)
                        for follower in followers:  # pas opti
                            if A_prime.states[q1_] in A_prime.final_states:
                                if q1_ == follower:
                                    sol.add(Implies(And(A_path[q1][q1_][q2][q2_], A_transitions[q2][s][q1]),
                                                    A_final_states[q1]))

    # clause 7
    sol.add(G_states[0][0] == True)
    for q in range(len(A_states)):
        for q_ in range(len(A_prime.states)):
            sol.add(Implies(G_states[q][q_], A_path[q][q_][q][q_]))
            sol.add(Implies(G_states[q][q_], N_path[q][q_][q][q_]))

    # on veut pas un état final dans un mais pas dans l'autre
    for q1 in range(len(A_states)):
        for q2 in range(len(A_states)):
            for q1_ in range(len(A_prime.states)):
                for q2_ in range(len(A_prime.states)):
                    sol.add(Not(And(A_path[q1][q1_][q2][q2_], Not(N_path[q1][q1_][q2][q2_]))))
                    sol.add(Not(And(N_path[q1][q1_][q2][q2_], Not(A_path[q1][q1_][q2][q2_]))))
                    # print(Not(And(A_path[q1][q1_][q2][q2_], Not(N_path[q1][q1_][q2][q2_]))))

    # pour avoir un autre modèle (correct pour graphe2)
    # sol.add(A_transitions[0][1][1] == True)

    if sol.check() == sat:
        model = sol.model()

        # affichage_path(model, A_states, A_prime_states)
        # affichage_transition(model)
        # affichage_G_states(model)
        # affichage_final_states_a(model)

        A_final_states = []
        A_transitions = []
        for i in model:
            if is_true(model[i]):
                type = repr(i).split(":")[0]
                val = repr(i).split(":")[1]
                if type == "A_final_states ":
                    A_final_state = (A_states[int(val[1])])
                    A_final_states.append(A_final_state)
                if type == "A_transition ":
                    A_transition = (A_states[int(val[2])], val[4], A_states[int(val[6])])
                    A_transitions.append(A_transition)

        new_automata = create_automata(A_states, A_symbols, A_initial_state, A_final_states, A_transitions)
        return new_automata

    return None


def main():
    list_file = {"LTL4.txt", "LTL3.txt", "LTL2.txt", "LTL1.txt", "file_graph.txt"}
    for i in list_file:
        print("Input Automata from file " + i)
        print("")
        input = open("../input_graphe/"+i, "r")
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

        minimizing = True
        loop_number = 0
        while minimizing:
            loop_number += 1
            if len(A_prime.states) < 2:
                minimizing = False
                loop_number -= 1
            else:
                automata = minimize(A_prime)
                if automata is None:
                    minimizing = False
                    loop_number -= 1
                else:
                    A_prime = automata
        print("")
        print("")
        print("minimization number = " + str(loop_number))
        print("")
        print("output Automata : ")
        print("A_states : ")
        print(*A_prime.states)
        print("A_symbols : ")
        print(*A_prime.symbols)
        print("A_initial_state : ")
        print(*A_prime.initial_state)
        print("A_final_states : ")
        print(*A_prime.final_states)
        print("A_transitions : ")
        print(A_prime.transitions)
        print("")
        print("")
        print("==================================================")



if __name__ == '__main__':
    main()
