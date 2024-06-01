import random
import matplotlib.pyplot as plt
import numpy as np


# equations = []

# while True:
#     equation = input(f"Enter coefficients of inequality {len(equations) + 1} (a*x1 + b*x2 <= c): ")
#     if equation.lower() == "done":
#         break
#     a, b, c = [float(x) for x in equation.split()]
#     sign = input("Enter sign <= or >=: ")
#     equations.append((a, b, c, sign))

equations = [[1, -1, 3, '<='], [1, 1, 6, '<='], [-1, 3, 10, '<='], [1, 4, 4, '>=']]

fig, ax = plt.subplots()
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

bound = 10

for i in range(len(equations)):
    a, b, c, sign = equations[i]
    x = np.arange(-bound, bound, 1)
    y = (c - a * x) / b
    
    color = f"#{random.randrange(0x1000000):06x}"
    alpha = 0.2
    ax.plot(x, y, color=color)

    if sign == ">=" or b < 0:
        ax.fill_between(x, bound, y, color=color, alpha=alpha)
        continue
    
    ax.fill_between(x, -bound, y, color=color, alpha=alpha)

plt.show()
