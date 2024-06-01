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


def seidelMethod(matrix, vector, eps):
    if not isConvergence(matrix):
        print("This method is not convergence!!")
        exit()

    tempSols = [0] * len(matrix)
    tempEps = 1
    print(tempSols)

    while tempEps > eps:
        tempEps = 0
        tempVector = vector.copy()

        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if i != j:
                    tempVector[i] -= matrix[i][j] * tempSols[j]
            newSol = tempVector[i] / matrix[i][i]
            localEps = abs(tempSols[i] - newSol)
            if localEps > tempEps:
                tempEps = localEps
            tempSols[i] = newSol
        print(tempSols)


# matrix, vector = getMatrixAndVector()

matrix = [[-0.68, -0.18, 0.02, 0.21], [0.16, -0.88, -0.14, 0.27],
          [0.37, 0.27, -1.02, -0.24], [0.12, 0.21, -0.18, -0.75]]
vector = [-1.83, 0.65, -2.23, 1.13]

# matrix = [[10, 1, 1], [2, 10, 1], [2, 2, 10]]
# vector = [12, 13, 14]
eps = 0.0000001
seidelMethod(matrix, vector, eps)
