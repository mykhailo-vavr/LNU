from math import inf, sin, cos
import numpy as np


# example task
def functions(x, y):
    return np.array([2 * y - cos(x + 1), x + sin(y) + 0.4])


def jacobian(x, y):
    return np.array([[sin(x + 1), 2], [1, cos(y)]])


x0, y0 = -0.9, 0.5

# personal task
# def functions(x, y):
#     return np.array([sin(x + 2) - y - 1.5, x + cos(y - 2) - 0.5])

# def jacobian(x, y):
#     return np.array([[cos(x + 2), -1], [1, -sin(y - 2)]])

# x0, y0 = 1.3, -1.7


def newtonMethod(F, W, x, y, eps):
    # F - vector of functions
    # W - jacobian matrix

    sols = [x, y]
    i = 0
    while True:
        if i > 3:
            break
        F_n = F(x, y)
        invW_n = np.linalg.inv(W(x, y))
        sols = sols - invW_n.dot(F_n)
        i += 1
        print(f"{i}: ", sols)
        if abs(max(x - sols[0], y - sols[1])) < eps:
            break


sols = newtonMethod(functions, jacobian, x0, y0, 0.001)
