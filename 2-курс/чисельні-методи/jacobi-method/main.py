from numpy import *


def getMatrixAndVector():
    print("Write size:")
    size = int(input())

    matrix = []
    print("Write matrix:")
    for i in range(size):
        row = []
        for j in range(size):
            value = float(input())
            row.append(value)
        matrix.append(row)
    print("Write vector:")
    vector = []
    for i in range(size):
        value = float(input())
        vector.append(value)
    return matrix, vector


def isConvergence(matrix):
    size = len(matrix)
    for i in range(size):
        sum = 0
        for j in range(size):
            if j != i:
                sum += abs(matrix[i][j])
        if abs(matrix[i][i]) < sum:
            return False
    return True


def jacobiMethod(matrix, vector, eps):
    if not isConvergence(matrix):
        print("This method is not convergence!!")
        exit()

    sols = [0, 0, 0]
    tempEps = 1
    print(sols)

    while tempEps > eps:
        tempEps = 0
        tempVector = vector.copy()
        tempSols = sols.copy()

        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if i != j:
                    tempVector[i] -= matrix[i][j] * tempSols[j]
            newSol = tempVector[i] / matrix[i][i]
            localEps = abs(tempSols[i] - newSol)
            if localEps > tempEps:
                tempEps = localEps
            sols[i] = newSol
        print(sols)


# matrix, vector = getMatrixAndVector()

# matrix = [[4.5, -1.8, 3.6], [3.1, 2.3, -1.2], [1.8, 2.5, 4.6]]
# vector = [-1.7, 3.6, 2.2]

matrix = [[10, 1, - 1], [1, 10, -1], [-1, 1, 10]]
vector = [11, 10, 10]
eps = 0.001
jacobiMethod(matrix, vector, eps)
