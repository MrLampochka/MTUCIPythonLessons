import matplotlib.pyplot as plt
import numpy as np


def makeGraph(x1, x2):
    x = np.linspace(-3, 3,100)
    plt.grid(True)
    y = lambda x: a*(x**2)+b*x+c
    plt.plot(x, y(x))
    plt.plot(x1, y(x1), marker="o", color="red")
    plt.plot(x2, y(x2), marker="o", color="red")
    plt.show()

print("Введите коэффициенты для уравнения")
print("ax^2 + bx + c = 0:")
a = float(input("a = "))
b = float(input("b = "))
c = float(input("c = "))

discr = b ** 2 - 4 * a * c
print("Дискриминант D = %.2f" % discr)

if discr > 0:
    x1 = (-b + np.sqrt(discr)) / (2 * a)
    x2 = (-b - np.sqrt(discr)) / (2 * a)
    print("x1 = %.2f \nx2 = %.2f" % (x1, x2))
    makeGraph(x1,x2)
elif discr == 0:
    x = -b / (2 * a)
    print("x = %.2f" % x)
    makeGraph(x,x)
else:
    print("Корней нет")
