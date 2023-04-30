from z3 import *
from itertools import combinations


def one_value(litterals):
    constraint = []
    for pair in combinations(litterals, 2):
        a, b = pair[0], pair[1]
        constraint += [Or(Not(a), Not(b))]
    constraint += [Or(litterals)]
    return And(constraint)


def main():
    lits = []
    for i in range(9):
        lits += [[]]
        for j in range(9):
            lits[i] += [[]]
            for digit in range(1, 10):
                lits[i][j] += [Bool("x" + str(i) + str(j) + str(digit))]
    s = Solver()


    # une fois par colonne
    for i in range(9):
        for value in range(9):
            col = []
            for j in range(9):
                col += [lits[j][i][value]]
            s.add(one_value(col))

    # une fois par ligne
    for i in range(9):
        for value in range(9):
            row = []
            for j in range(9):
                row += [lits[i][j][value]]

            s.add(one_value(row))

    # une valeur par case
    for i in range(9):
        for j in range(9):
            s.add(one_value(lits[i][j]))

    # une fois par case 3x3
    for i in range(3):
        for j in range(3):
            for value in range(9):
                case = []
                for a in range(3):
                    for b in range(3):
                        case += [lits[3 * i + a][3 * j + b][value]]
                s.add(one_value(case))

    if str(s.check()) == 'sat':
        print("sat")
        m = s.model()
        lines = []
        for i in range(9):
            lines += [[]]
            for j in range(9):
                digit = 0
                for x in range(9):
                    if m.evaluate(lits[i][j][x]):
                        digit = x + 1
                lines[i] += [digit]
        affichage(lines)


def affichage(lines):
    i = 0
    j = 0
    for line in lines:
        j += 1
        p = ""
        for x in line:
            i += 1
            p += (" " + (str(x)))
            if i % 3 == 0:
                p += (" |")
        print(p)
        if j % 3 == 0:
            print("-----------------------")


if __name__ == '__main__':
    main()
