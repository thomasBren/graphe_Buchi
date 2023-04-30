from z3 import *


def affichage(m, n, x):
    for i in range(n):
        line = ""
        for j in range(n):
            if m.evaluate(x[i][j]):
                line += "X "
            else:

                line += ". "
        print(line)


def main(n):
    # création des littéraux x[ligne][colonne]
    cases = []
    for i in range(n):
        y = []
        for j in range(n):
            y.insert(j, Bool("x_" + str(i) + "_" + str(j)))
        cases.insert(i, y)

    sol = Solver()

    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    if j != l and i != k:
                        sol.add(Implies(cases[i][j], Not(cases[i][l])))
                        sol.add(Implies(cases[i][j], Not(cases[k][j])))

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if k != i:
                    if 0 <= j + k - i <= n - 1:
                        sol.add(Implies(cases[i][j], Not(cases[k][j + k - i])))
                    if 0 <= j + i - k <= n - 1:
                        sol.add(Implies(cases[i][j], Not(cases[k][j + i - k])))

    for i in range(n):
        list = []
        for j in range(n):
            list.append(cases[i][j])
        sol.add(Or(list))

    print(sol.check())

    if str(sol.check())=='sat':
        m = sol.model()
        print(m)
        affichage(m, n, cases)
        return m
    else:
        print("not satisfiable")
        return 0




if __name__ == '__main__':
    main(8)
