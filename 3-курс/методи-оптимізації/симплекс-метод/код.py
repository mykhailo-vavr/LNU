import numpy as np

def simplex(c, A, b):
    m, n = A.shape
    # додамо змінну функції заміни
    c = np.append(c, np.zeros(n + 1))
    A = np.hstack((A, np.eye(m)))
    c = np.hstack((c, np.zeros(m)))
    # додамо штучні змінні
    for i in range(m):
        if b[i] < 0:
            A[i,:] *= -1
            b[i] *= -1
    A = np.hstack((A, np.eye(m)))
    c = np.hstack((c, np.ones(m) * -1))
    # початковий базис
    basis = list(range(n, n + m))
    while True:
        # знайдемо опорний стовпець
        j = np.argmin(c[:n+m])
        if c[j] >= 0:
            break
        # знайдемо опорний рядок
        ratios = np.array([b[i]/A[i,j] if A[i,j] > 0 else np.inf for i in range(m)])
        i = np.argmin(ratios)
        if ratios[i] == np.inf:
            return "немає оптимального розв'язку"
        # обновимо базис
        basis[i] = j
        # перевірка на обмеженість
        if np.all(A[:,j] <= 0):
            return "задача необмежена"
        # проведемо елементарні операції
        pivot = A[i,j]
        A[i,:] /= pivot
        b[i] /= pivot
        for k in range(m):
            if k == i:
                continue
            factor = A[k,j]
            A[k,:] -= factor * A[i,:]
            b[k] -= factor * b[i]
        factor = c[j]
        c -= factor * A[i,:]
    # розрахунок оптимального розв'язку та значення функції мети
    x = np.zeros(n + m)
    x[basis] = b
    opt_val = np.dot(c[:n], x[:n])
    return x[:n], opt_val

A = np.array([[4, 3, 2, -1], [1, -2, -5, -3]])
b = np.array([7, -12])
c = np.array([3, 7, 6, 5])

z, x = simplex(c, A, b)
print("Optimal solution:")
print("z =", z)
print("x =", x)