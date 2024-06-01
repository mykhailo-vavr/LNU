import numpy as np
import matplotlib.pyplot as plt


def lagrange(x, y, x_i):
    size = len(y) - 1
    result = 0
    for j in range(size):
        p1 = p2 = 1
        for i in range(size):
            if i != j:
                p1 *= (x_i - x[i])
                p2 *= (x[j] - x[i])
        result += y[j] * p1 / p2
    return result


# Example
# x = np.array([-1, -0.2, 1.8, 2.7, 4, 2])
# y = np.array([5, 4.6, 5.7, 5.02, 4.3, None])
# solution = lagrange(x, y, 2)

# Task
x = np.array([-1, 0, 1, 2, -2])
y = np.array([2, 2, -2, -4, None])
solution = lagrange(x, y, -2)

y[len(y) - 1] = solution
print("Solution:", solution)

x_new = np.linspace(np.min(x), np.max(x))
y_new = [lagrange(x, y, i) for i in x_new]
plt.plot(x, y, 'o', x_new, y_new)
plt.grid(True)
plt.show()