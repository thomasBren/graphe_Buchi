import unittest
from graphe.src.mypackage.graphe import *


class test(unittest.TestCase):
    def test_getAPrimeFollowers(self):
        q_ = 1
        q2_ = 0
        s = 1
        transitions = [('q0', '0', 'q1'), ('q0', '1', 'q2'), ('q0', '1', 'q1'), ('q1', '0', 'q2'), ('q1', '1', 'q0'),
                       ('q2', '1', 'q0'), ('q2', '0', 'q2'), ('q3', '1', 'q3'), ('q3', '0', 'q3')]
        res = getAPrimeFollowers(q_, s, transitions)
        res2 = getAPrimeFollowers(q2_, s, transitions)

        self.assertEquals(res, [0])
        self.assertEquals(res2, [2, 1])

        bad_s = 3
        res3 = getAPrimeFollowers(q_, bad_s, transitions)
        self.assertEquals(res3, [])

        bad_q_ = 4
        res4 = getAPrimeFollowers(bad_q_, s, transitions)
        self.assertEquals(res4, [])

    def test_transitions_in_A(self):
        A_states = [0, 1]
        A_symbols = [0, 1]
        res = transitions_in_A(A_states, A_symbols)
        self.assertEquals(res, [[[Bool("A_transition : (0,0,0)"), Bool("A_transition : (0,0,1)")],
                                 [Bool("A_transition : (0,1,0)"), Bool("A_transition : (0,1,1)")]],
                                [[Bool("A_transition : (1,0,0)"), Bool("A_transition : (1,0,1)")],
                                 [Bool("A_transition : (1,1,0)"), Bool("A_transition : (1,1,1)")]]])

    def test_vertex_G(self):
        A_states = [0, 1]
        A_prime_states = [0, 1]
        res = vertex_G(A_states, A_prime_states)
        self.assertEquals(res, [[Bool("G : (0,0)"), Bool("G : (0,1)")], [Bool("G : (1,0)"), Bool("G : (1,1)")]])

    def test_final_states_of_A(self):
        A_states = [0, 1]
        res = final_states_of_A(A_states)
        self.assertEquals(res, [Bool("A_final_states : 0"), Bool("A_final_states : 1")])

    def test_path_G(self):
        A_states = [0, 1]
        A_prime_states = [0, 1]
        res, resbis = path_G(A_states, A_prime_states)

        self.assertEquals(res, [[[[Bool("A_path : (0,0,0,0)"), Bool("A_path : (0,0,0,1)")],
                                  [Bool("A_path : (0,0,1,0)"), Bool("A_path : (0,0,1,1)")]],
                                 [[Bool("A_path : (0,1,0,0)"), Bool("A_path : (0,1,0,1)")],
                                  [Bool("A_path : (0,1,1,0)"), Bool("A_path : (0,1,1,1)")]]],
                                [[[Bool("A_path : (1,0,0,0)"), Bool("A_path : (1,0,0,1)")],
                                  [Bool("A_path : (1,0,1,0)"), Bool("A_path : (1,0,1,1)")]],
                                 [[Bool("A_path : (1,1,0,0)"), Bool("A_path : (1,1,0,1)")],
                                  [Bool("A_path : (1,1,1,0)"), Bool("A_path : (1,1,1,1)")]]]])

        self.assertEquals(resbis, [[[[Bool("N_path : (0,0,0,0)"), Bool("N_path : (0,0,0,1)")],
                                     [Bool("N_path : (0,0,1,0)"), Bool("N_path : (0,0,1,1)")]],
                                    [[Bool("N_path : (0,1,0,0)"), Bool("N_path : (0,1,0,1)")],
                                     [Bool("N_path : (0,1,1,0)"), Bool("N_path : (0,1,1,1)")]]],
                                   [[[Bool("N_path : (1,0,0,0)"), Bool("N_path : (1,0,0,1)")],
                                     [Bool("N_path : (1,0,1,0)"), Bool("N_path : (1,0,1,1)")]],
                                    [[Bool("N_path : (1,1,0,0)"), Bool("N_path : (1,1,0,1)")],
                                     [Bool("N_path : (1,1,1,0)"), Bool("N_path : (1,1,1,1)")]]]])

    def test_getAPrimeFollowers(self):
        q_ = 0
        s = 0
        transitions = [('q0', '0', 'q1'), ('q0', '1', 'q2'), ('q0', '1', 'q1'), ('q1', '0', 'q2'), ('q1', '1', 'q0'),
                       ('q2', '1', 'q0'), ('q2', '0', 'q2'), ('q3', '1', 'q3'), ('q3', '0', 'q3')]
        res = getAPrimeFollowers(q_, s, transitions)
        self.assertEquals(res, [1])

        s = 1
        res2 = getAPrimeFollowers(q_, s, transitions)
        self.assertEquals(res2, [2, 1])

        s = 3
        res2 = getAPrimeFollowers(q_, s, transitions)
        self.assertEquals(res2, [])

        s = 1
        q_ = 5
        res2 = getAPrimeFollowers(q_, s, transitions)
        self.assertEquals(res2, [])


    if __name__ == '__main__':
        unittest.main()
