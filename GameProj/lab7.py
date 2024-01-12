import numpy as np

# Заданная функция и ограничения
c = np.array([-1, -2, -8])
A = np.array([[3, 1, 3],
              [-3, -1, 1],
              [-2, 1, 0]])
b = np.array([3, 0, 0])

# Добавление искусственного базиса
c_artificial = np.array([0, 0, 0, -1])
A_artificial = np.array([[3, 1, 3, 1],
                         [-3, -1, 1, 0],
                         [-2, 1, 0, 0]])
B = np.array([3, 0, 0])


# Метод искусственного базиса
def artificial_basis_method(c, A, b):
    A = np.column_stack((A, np.eye(len(A))))
    m, n = A.shape

    # Проверка наличия искусственного базиса
    if np.sum(c) == 0:
        c = c_artificial
        A = A_artificial

    table = np.zeros((m + 1, n + m + 1))
    table[:-1, :-1] = A
    table[:-1, -1] = b
    table[-1, :-1] = -c

    # Поиск базисного решения
    B = np.arange(n, n + m)
    N = np.arange(n)
    while np.min(table[-1, :-1]) < 0:
        entering_idx = np.argmin(table[-1, :-1])
        entering_var = N[entering_idx]
        col = table[:-1, entering_idx]

        # Выбор исходящей переменной (разрешающая строка)
        ratios = np.divide(table[:-1, -1], col, out=np.inf * np.ones_like(col), where=col > 0)
        leaving_idx = np.argmin(ratios)
        leaving_var = B[leaving_idx]
        row = table[leaving_idx, :]

        # Основная операция симплекс-метода
        table -= np.outer(table[:, entering_idx], table[leaving_idx, :]) / table[leaving_idx, entering_idx]
        table[leaving_idx, :] = row / table[leaving_idx, entering_idx]
        table[:, entering_idx] = col / table[leaving_idx, entering_idx]

        # Обновление базиса
        B[leaving_idx] = entering_var
        N[entering_idx] = leaving_var

    if np.sum(c) == 0:
        is_optimal = True
        x = np.zeros(n)
    else:
        is_optimal = False
        x = table[:-1, -1]

    return is_optimal, x


# Вызов функции для решения задачи
is_optimal, x = artificial_basis_method(c, A, b)

# Вывод результатов
if is_optimal:
    print("Оптимальное решение найдено!")
    print("x1 =", x[0])
    print("x2 =", x[1])
    print("x3 =", x[2])
else:
    print("Задача не имеет оптимального решения.")
