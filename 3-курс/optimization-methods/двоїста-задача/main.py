import numpy as np
from scipy.optimize import linprog


def get_dual(c, A, b, sense):
  dual_c = b
  dual_A = np.transpose(A)
  dual_b = c
  sense = "min" if sense == "max" else "max"

  return dual_c, dual_A, dual_b, sense

def print_dual(c, A, b, sense):
  print(f'F = {" + ".join([f"{c[i]}y{i+1}" for i in range(len(c))])} -> {sense}')

  for i in range(len(A)):
      values=[]
      
      for j in range(len(A[0])):
          values.append(f"{A[i][j]}y{i + 1}")
      print(f'{" + ".join(values)} <= {b[i]}')         
  print('yi>=0')

c = np.array([2, -1, 1])
A = np.array([[1, 2, -1], [2, -4, 3]])
b = np.array([5, 3])
bounds = [(0, None), (0, None)]
sense = "min"

c, A, b, find = get_dual(c, A, b, sense)
print_dual(c, A, b, find)

res = linprog(c=c, A_eq=A, b_eq=b, bounds=bounds, method='highs')

if res.success:
    print("x =", res.x)
    print("f =", res.fun)
else:
    print("Infinity function")