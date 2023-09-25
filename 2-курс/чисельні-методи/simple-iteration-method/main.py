from math import e, log, sqrt
import numpy as np

# example task
# def functions(x, y):
#     return np.array([sqrt((x * (y + 5) - 1) / 2), sqrt(x + 3 * log(x, 10))])

# def derivatives(x, y):
#     return np.array([(y + 5) / (4 * sqrt(
#         (x * (y + 5) - 1) / 2)), x / (4 * sqrt((x * (y + 5) - 1) / 2)),
#                      (1 + 3 / log(10) * x) / (2 * sqrt(x + 3 * log(x, 10))),
#                      0])

# x0, y0 = 3.5, 2.2


# personal task
def functions(x, y):
    return np.array([log(1 + 2 * y, e), 2 - pow(e, 2 * x)])


def derivatives(x, y):
    return np.array([0, 0, 0, 0])


x0, y0 = 0.3, 0.175


def toFixed(num, n):
    return float(format(num, f".{n}f"))


def isConvergent(derivatives, x, y):
    f1, f2, f3, f4 = derivatives(x, y)
    return abs(f1) + abs(f2) < 1 or abs(f3) + abs(f4) < 1


def simpleIterationMethod(F, derivatives, x0, y0, eps):
    # F - vector of functions

    if not isConvergent(derivatives, x0, y0):
        return print("Method is nonconvergent")

    sols = [x0, y0]

    i = 1
    print(f"{0}: ", [toFixed(x0, 8), toFixed(y0, 8)])
    while True:
        x, y = F(*sols)
        print(f"{i}: ", [toFixed(x, 8), toFixed(y, 8)])
        if abs(max(x - sols[0], y - sols[1])) < eps:
            break
        sols = [x, y]
        i += 1


sols = simpleIterationMethod(functions, derivatives, x0, y0, 0.001)
