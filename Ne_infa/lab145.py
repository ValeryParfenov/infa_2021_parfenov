import numpy as np
import matplotlib.pyplot as plt

X = np.array([0, 1, 2, 3, 5, 7, 9, 4, 6, 8, 10])
Y = np.array([0, 139, 280, 421, 704, 990, 1278, 563, 847, 1135, 1425])
Y11 = np.array([0, 184, 369, 554, 924, 1296, 1672, 739, 1111, 1484, 1862])
Y22 = np.array([0, 227, 455, 683, 1139, 1598, 2058, 911, 1368, 1826, 2287])
Xerror_range = 0
Yerror_range = 1
x_value_name = 'n'
y_value_name = '/nu, Гц'
LX = len(X)

print("СРЕДНЕЕ")
x1 = np.mean(X)
print(x1, "- среднее значение")
X1 = X - x1
x11 = np.mean(abs(X1))
print(x11, "- среднее отклонение от среднего \n")

print("СРЕДНЕ КВАДРАТИЧНОЕ")
X2 = (X) ** 2
x2 = (np.mean(X2)) ** 0.5
print(x2, "- среднеквадратичное значение")
x21 = (np.mean((X - x1) ** 2)) ** 0.5
print(x21, "- среднеквадратичное отклонение от среднего")
x22 = (np.mean((X - x2) ** 2)) ** 0.5
print(x22, "- среднеквадратичное отклонение от среднеквадратичного \n")

x3 = (np.sum((X - x1) ** 2) / (LX - 1)) ** 0.5
print(x3, "- случайная ошибка единичного измерения")
x31 = (np.sum((X - x1) ** 2) / ((LX - 1) * LX)) ** 0.5
print(x31, "- случайная ошибка каждого измерения в серии")
x32 = x31 ** 2
print(x32, "- дисперсия\n\n")

print("---------------- МНК -----------------\n")
b = (np.mean(X * Y) - np.mean(X) * np.mean(Y)) / (np.mean(X ** 2) - np.mean(X) ** 2)
a = np.mean(Y) - b * np.mean(X)
Sb = (1 / LX ** 0.5) * ((np.mean(Y ** 2) - np.mean(Y) ** 2) / (np.mean(X ** 2) - np.mean(X) ** 2) - b ** 2) ** 0.5
Sa = Sb * (np.mean(X ** 2) - np.mean(X) ** 2) ** 0.5
Y1 = a + b * X
r = (np.mean(X * Y) - np.mean(X) * np.mean(Y)) / (
            (np.mean(Y ** 2) - np.mean(Y) ** 2) * (np.mean(X ** 2) - np.mean(X) ** 2)) ** 0.5

plt.plot(X, Y1)
plt.errorbar(X, Y, color='green', marker='o', linestyle='none', xerr=Xerror_range, yerr=Yerror_range)

b11 = (np.mean(X * Y11) - np.mean(X) * np.mean(Y11)) / (np.mean(X ** 2) - np.mean(X) ** 2)
a11 = np.mean(Y11) - b11 * np.mean(X)
Sb11 = (1 / LX ** 0.5) * ((np.mean(Y11 ** 2) - np.mean(Y11) ** 2) / (np.mean(X ** 2) - np.mean(X) ** 2) - b11 ** 2) ** 0.5
Sa11 = Sb11 * (np.mean(X ** 2) - np.mean(X) ** 2) ** 0.5
Yb1 = a11 + b11 * X
r11 = (np.mean(X * Y11) - np.mean(X) * np.mean(Y11)) / (
            (np.mean(Y11 ** 2) - np.mean(Y11) ** 2) * (np.mean(X ** 2) - np.mean(X) ** 2)) ** 0.5
plt.plot(X, Yb1)
plt.errorbar(X, Y11, color='green', marker='o', linestyle='none', xerr=Xerror_range, yerr=Yerror_range)

b22 = (np.mean(X * Y22) - np.mean(X) * np.mean(Y22)) / (np.mean(X ** 2) - np.mean(X) ** 2)
a22 = np.mean(Y22) - b22 * np.mean(X)
Sb22 = (1 / LX ** 0.5) * ((np.mean(Y22 ** 2) - np.mean(Y22) ** 2) / (np.mean(X ** 2) - np.mean(X) ** 2) - b22 ** 2) ** 0.5
Sa22 = Sb22 * (np.mean(X ** 2) - np.mean(X) ** 2) ** 0.5
Yb2 = a22 + b22 * X
r22 = (np.mean(X * Y22) - np.mean(X) * np.mean(Y22)) / (
            (np.mean(Y22 ** 2) - np.mean(Y22) ** 2) * (np.mean(X ** 2) - np.mean(X) ** 2)) ** 0.5
plt.plot(X, Yb2)
plt.errorbar(X, Y22, color='green', marker='o', linestyle='none', xerr=Xerror_range, yerr=Yerror_range)

plt.ylabel(r'$\nu, Гц$')
plt.xlabel(x_value_name)
plt.grid()
plt.show()
print("y = a + bx")
print("b1 =", b, "+-", Sb, "Гц")
print("a1 =", a, "+-", Sa, "Гц")
print("r1 =", r)
print("b2 =", b11, "+-", Sb11, "Гц")
print("a2 =", a11, "+-", Sa11, "Гц")
print("r2 =", r11)
print("b3 =", b22, "+-", Sb22, "Гц")
print("a3 =", a22, "+-", Sa22, "Гц")
print("r3 =", r22)
