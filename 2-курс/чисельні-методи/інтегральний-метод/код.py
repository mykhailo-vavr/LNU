import numpy as np


class integral:
    def __init__(self, low, up, func, n):
        self.low = low
        self.up = up
        self.func = func
        self.n = n
        self.h = (self.up - self.low) / self.n

    def newton(self, F):
        return F(self.up) - F(self.low)

    def rectangle(self):
        iterations = 0
        area = 0

        x = self.low

        for i in range(self.n - 1):
            iterations += 1
            area += self.h * self.func(x)
            x += self.h

        print("Rectangle iterations:", iterations)
        return area

    def trapezoidal(self):
        iterations = 0
        area = 0

        x = self.low
        f1 = self.func(x)
        f2 = self.func(x + self.h)

        for i in range(self.n - 1):
            iterations += 1
            area += (f1 + f2) * self.h / 2
            f1 = f2
            x += self.h
            f2 = self.func(x + self.h)

        print("Trapezoidal iterations:", iterations)
        return area

    def simpson(self):
        area = (self.func(self.low) + self.func(self.up)) * 0.5
        iterations = 0

        for i in range(1, self.n):
            iterations += 1
            xk = self.low + self.h * i
            xk1 = self.low + self.h * (i - 1)
            area += self.func(xk) + 2 * self.func((xk1 + xk) / 2)

        x = self.low + self.h * self.n
        x1 = self.low + self.h * (self.n - 1)
        area += 2 * self.func((x1 + x) / 2)
        iterations += 1

        print("Simpson iterations:", iterations)
        return area * self.h / 3.0


def f(x):
    return np.log(1 + x * x)


def F(x):
    return x * np.log(1 + x * x) - 2 * (x - np.arctan(x))


i = integral(0, 1.2, f, 100)

methods = np.array([
    'rectangle',
    'trapezoidal',
    'simpson',
    'newton',
])

print("\n")
integrals = np.array([
    i.rectangle(),
    i.trapezoidal(),
    i.simpson(),
    i.newton(F),
])
eps = i.newton(F) - integrals

print('\n')
for i in range(methods.size):
    print(methods[i], ': \t', integrals[i], '\te = ', eps[i])
print('\n')
