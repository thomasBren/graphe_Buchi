from z3 import *
from itertools import combinations



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


def orTransition(transitions):
    # print(type(litterals))
    # print(type(litterals[0]))
    constraint = []
    for transition in transitions:
        # print(type(pair))
        b = transition
        # print(type(a[2]))
        constraint += [b]
    #print(Or(constraint))
    return Or(constraint)


def getAPrimeFollowers(q_, s, transitions):
    # print('rentre')
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


def main():
    print("Input Automata : ")
    input = open("../../graphe2.txt", "r")
    A_prime_states = list(input.readline().split())
    print("A_prime_states : ")
    print(*A_prime_states)
    A_prime_symbols = list(input.readline().split())
    print("A_prime_symbols : ")
    print(*A_prime_symbols)
    prime_initial_state = list(input.readline().split())
    print("prime_initial_state : ")
    print(*prime_initial_state)
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
        A_prime = create_automata(A_prime_states, A_prime_symbols, prime_initial_state, A_prime_final_states,
                                  A_prime_transitions)
    except AutomataError as ex:
        print(ex)
        return 0

    print("")
    print("Test : ")
    print(A_prime.transitions[0][0])

    print("")
    print("New automata : ")

    A_states = []
    for i in range(len(A_prime_states) - 1):
        A_states.append("q" + str(i))
    print("A_states : ")
    print(*A_states)
    A_symbols = A_prime_symbols
    print("A_symbols : ")
    print(*A_symbols)
    A_initial_state = ["q0"]
    print("A_initial_state : ")
    print(*A_initial_state)
    #A_final_states = []
    #A_transitions = []
    #print("A_transitions : ")
    #print(*A_transitions)

    #G_states = [("q0", "q0")]  # clause 7 partie 1
    #print("G_states : ")
    #print(*G_states)

    # crée la liste de toutes les A_prime_transitions possible dans le graphe A

    A_transition = []
    for q in range(len(A_states)):
        A_transition += [[]]
        for s in range(len(A_symbols)):
            A_transition[q] += [[]]
            for q2 in range(len(A_states)):
                A_transition[q][s] += [Bool("A_transition" + str(q) + str(s) + str(q2))]
                # print("A_transition" + str(q) + str(s) + str(q2))

    # crée la liste les sommets du graphe G possibles

    G_states = []
    for q in range(len(A_states)):
        G_states += [[]]
        for q_ in range(len(A_prime_states)):
            G_states[q] += [Bool("G" + str(q) + str(q_))]
            # print("G" + str(q) + str(q_))

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
                    A_path[q1][q1_][q2] += [Bool("A_path" + str(q1) + str(q1_) + str(q2) + str(q2_))]
                    N_path[q1][q1_][q2] += [Bool("N_path" + str(q1) + str(q1_) + str(q2) + str(q2_))]
                    # print("A_path" + str(q1) + str(q1_) + str(q2) + str(q2_))
                    # print("N_path" + str(q1) + str(q1_) + str(q2) + str(q2_))

    # crée la liste de tout les état finaux possibles pour A

    A_final_states = []
    for q1 in range(len(A_states)):
        A_final_states += [Bool("A_final_states" + str(q1))]
        print("A_final_states" + str(q1))

    sol = Solver()


    # clause 1

    for q1 in range(len(A_states)):
        for s in range(len(A_symbols)):
            transit = []
            for q2 in range(len(A_states)):
                transit += [A_transition[q1][s][q2]]
            #print(transit)
            sol.add(orTransition(transit))

    # clause 2

    for q1 in range(len(A_states)):
        for q_ in range(len(A_prime_states)):
            #print(new_G_states[q1][q_])
            for q2 in range(len(A_states)):
                for s in range(len(A_prime_symbols)):
                    followers = getAPrimeFollowers(q_, s, A_prime_transitions)
                    for follower in followers:  # pas opti
                        sol.add(Implies(And(G_states[q1][q_]), A_transition[q1][s][q2], G_states[q2][follower]))



    # clause 3

    for q1 in range(len(A_states)):
        for q2 in range(len(A_states)):
            for q3 in range(len(A_states)):
                for q1_ in range(len(A_prime_states)):
                    for q2_ in range(len(A_prime_states)):
                        for s in range(len(A_prime_symbols)):
                            followers = getAPrimeFollowers(q2_, s, A_prime_transitions)
                            for follower in followers:  # pas opti
                                if follower not in A_prime_final_states:
                                    if q1 != q3 or q1_ != follower:
                                        sol.add(Implies(And(N_path[q1][q1_][q2][q2_], A_transition[q2][s][q3]),
                                                   N_path[q1][q1_][q3][follower]))

    # clause 4

    for q1 in range(len(A_states)):
        for q2 in range(len(A_states)):
            for q1_ in range(len(A_prime_states)):
                for q2_ in range(len(A_prime_states)):
                    for s in range(len(A_prime_symbols)):
                        followers = getAPrimeFollowers(q2_, s, A_prime_transitions)
                        for follower in followers:  # pas opti
                            if q1_ not in A_prime_final_states and q1_ == follower:
                                sol.add(Implies(And(N_path[q1][q1_][q2][q2_], A_transition[q2][s][q1]), Not(A_final_states[q1])))

    # clause 5

    for q1 in range(len(A_states)):
        for q2 in range(len(A_states)):
            for q3 in range(len(A_states)):
                for q1_ in range(len(A_prime_states)):
                    for q2_ in range(len(A_prime_states)):
                        for s in range(len(A_prime_symbols)):
                            followers = getAPrimeFollowers(q2_, s, A_prime_transitions)
                            for follower in followers:  # pas opti
                                if q1_ in A_prime_final_states:
                                    if q1 != q3 or q1_ != follower:
                                        sol.add(Implies(And(A_path[q1][q1_][q2][q2_], A_transition[q2][s][q3], Not(A_final_states[q3])),
                                                   A_path[q1][q1_][q3][follower]))

    # clause 6

    for q1 in range(len(A_states)):
        for q2 in range(len(A_states)):
            for q1_ in range(len(A_prime_states)):
                for q2_ in range(len(A_prime_states)):
                    for s in range(len(A_prime_symbols)):
                        followers = getAPrimeFollowers(q2_, s, A_prime_transitions)
                        for follower in followers:  # pas opti
                            if q1_ in A_prime_final_states:
                                if q1_ == follower:
                                    sol.add(Implies(And(A_path[q1][q1_][q2][q2_], A_transition[q2][s][q1]), A_final_states[q1]))

    # clause 7
    sol.add(G_states[0][0])
    for q in range(len(A_states)):
        for q_ in range(len(A_prime_states)):
            sol.add(Implies(G_states[q][q_], A_path[q][q_][q][q_]))
            sol.add(Implies(G_states[q][q_], N_path[q][q_][q][q_]))


    print("G_states : ")
    print(*G_states)

    if str(sol.check()) == 'sat':
        print("")
        print("sat")

        m = sol.model()
        print(m)

        



if __name__ == '__main__':
    main()
