import numpy as np
import scipy

a = np.array([22, 188, 210, 380])
b = np.array([125, 75, 200, 220, 0])
D = np.array([[23, 21, 11, 8, 3],
              [7, 17, 5, 2, 4],
              [2, 16, 8, 4, 3],
              [3, 9, 21, 8, 4]])


def ij(c_min):
    c = np.inf
    for i in range(c_min.shape[0]):
        for j in range(c_min.shape[1]):
            if (c_min[i, j] != 0) and (c_min[i, j] < c):
                c = c_min[i, j]
                i_, j_ = i, j
    return i_, j_


def M_min(a_, b_, c_):
    a = np.copy(a_)
    b = np.copy(b_)
    c = np.copy(c_)

    if a.sum() > b.sum():
        b = np.hstack((b, [a.sum() - b.sum()]))
        c = np.hstack((c, np.zeros(len(a)).reshape(-1, 1)))
    elif a.sum() < b.sum():
        a = np.hstack((a, [b.sum() - a.sum()]))
        c = np.vstack((c, np.zeros(len(b))))

    m = len(a)
    n = len(b)
    x = np.zeros((m, n), dtype=int)
    funk = 0
    while True:
        c_min = np.zeros((m, n))
        for i in range(m):
            for j in range(n):
                c_min[i, j] = (c[i, j] * min(a[i], b[j]))
        i, j = ij(c_min)
        x_ij = int(min(a[i], b[j]))
        x[i, j] = x_ij
        funk += int(c_min[i, j])
        a[i] -= x_ij
        b[j] -= x_ij
        if len(c_min[c_min > 0]) == 1:
            break
    return x, funk


x, funk = M_min(a, b, D)
print('Опорный план: \n', x)
print('Значение целевой функции: ', funk)



def prepare(a, b):
    m = len(a)
    n = len(b)
    h = np.diag(np.ones(n))
    v = np.zeros((m, n))
    v[0] = 1
    for i in range(1, m):
        h = np.hstack((h, np.diag(np.ones(n))))
        k = np.zeros((m, n))
        k[i] = 1
        v = np.hstack((v, k))
    return np.vstack((h, v)).astype(int), np.hstack((b, a))

def potenz(a_, b_, c_):
    a = np.copy(a_)
    b = np.copy(b_)
    c = np.copy( c_)

    if a.sum() > b.sum():
        b = np.hstack((b, [a.sum() - b.sum()]))
        c = np.hstack((c, np.zeros(len(a)).reshape(-1, 1)))
    elif a.sum() < b.sum():
        a = np.hstack((a, [b.sum() - a.sum()]))
        c = np.vstack((c, np.zeros(len(b))))

    m = len(a)
    n = len(b)
    A_eq, b_eq = prepare(a, b)

    res = scipy.optimize.linprog(c.reshape(1, -1), A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='simplex')
    return res.x.astype(int).reshape(m, n), res.fun.astype(int)


x2, funk2 = potenz(a, b, D)
print('Метод потенциалов: \n', x2)
print('Значение целевой функции: ', funk2)