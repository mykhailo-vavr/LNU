import numpy as np
import math


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
    return np.array(matrix), np.array(vector)


def isValidMatrix(matrix):
    return (matrix.T == matrix).all() and np.linalg.det(matrix) > 0


def getU(matrix):
    U = [[0] * len(matrix) for i in range(len(matrix))]

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if j < i:
                U[i][i] = 0
            elif i == j:
                sum = 0
                for k in range(i):
                    sum += U[k][i]**2
                try:
                    U[i][j] = math.sqrt(matrix[i][i] - sum)
                except:
                    print(f"\nSquare root is negative. Index of line: {i}\n")
                    exit()
            else:
                sum = 0
                for k in range(i):
                    sum += U[k][i] * U[k][j]
                U[i][j] = (matrix[i][j] - sum) / U[i][i]

    return np.array(U)


def getAuxiliaryUnknown(U, vector):
    unknown = []
    for i in range(len(U)):
        sum = 0
        for k in range(i):
            sum += U[k][i] * unknown[k]
        unknown.append((vector[i] - sum) / U[i][i])

    return unknown


def getSolutions(U, unknown):
    solutions = [None] * len(U)
    for i in reversed(range(len(U))):
        sum = 0
        for k in range(i + 1, len(U)):
            sum += U[i][k] * solutions[k]
        solutions[i] = (unknown[i] - sum) / U[i][i]

    return solutions


def squareRootMethod(matrix, vector):
    if not isValidMatrix(matrix):
        return print("Invalid matrix")

    U = getU(matrix)
    print("\nU:\n", U)

    unknown = getAuxiliaryUnknown(U, vector)
    print("\nAuxiliary unknown: ", unknown)

    solutions = getSolutions(U, unknown)
    print("\nSolutions: ", solutions, "\n")


# matrix, vector = getMatrixAndVector()

# solved SLE
matrix = np.array([(4, 2, 2, 1), (2, 5, 1, 2), (2, 1, 5, 1), (1, 2, 1, 4.875)])
vector = np.array([9, 10, 9, 8.875])

# v5 SLE
# matrix = np.array([(0.93, 1.42, -2.25), (1.42, -2.87, 2.36),
#                    (-2.25, 2.36, -1.44)])
# vector = np.array([2.48, -0.75, 1.83])

squareRootMethod(matrix, vector)
