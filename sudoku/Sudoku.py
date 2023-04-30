from z3 import *



def main():
    lits = []
    for i in range(9):
        lits += [[]]
        for j in range(9):
            lits[i] += [[]]
            for digit in range(1, 10):
                lits[i][j] += [Bool("x" + str(i) + str(j) + str(digit))]
    s = Solver()

    for i in range(9):
        for j in range(9):
            or_list = []
            for v in range(9):
                or_list += [lits[i][j][v]]
            s.add(Or(or_list))

    for i in range(9):
        for j in range(9):
            for v in range(9):
                for v_ in range(9):
                    if v != v_:
                        s.add(Implies(lits[i][j][v], Not(lits[i][j][v_])))

    for i in range(9):
        for j in range(9):
            for v in range(9):
                for k in range(9):
                    if k != i:
                        s.add(Implies(lits[i][j][v], Not(lits[k][j][v])))
                    if k != j:
                        s.add(Implies(lits[i][j][v], Not(lits[i][k][v])))

    for v in range(9):
        for i in range(3):
            for j in range(3):
                or_list2 = []
                for a in range(3):
                    for b in range(3):
                        or_list2 += [lits[3*i+a][3*j+b][v]]
                s.add(Or(or_list2))

    if str(s.check()) == 'sat':

        m = s.model()
        affichage(m,lits)


def affichage(m,lits):
    lines = []
    for i in range(9):
        lines += [[]]
        line = ""
        for j in range(9):
            for x in range(9):
                if m.evaluate(lits[i][j][x]):
                    line+=str(x+1)+" "
                    if((j+1)%3==0):
                        line += "|" + " "
        if ((i) % 3 == 0):
            print("-----------------------")
        print(line)
    print("-----------------------")



if __name__ == '__main__':
    main()
