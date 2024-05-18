#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# С использованием многопоточности для заданного значения x
# найти сумму ряда S с точностью члена ряда по абсолютному
# значению E = 10e-7 и произвести сравнение полученной суммы
# с контрольным значением функции для двух бесконечных рядов.


import math
from threading import Lock, Thread


E = 10e-7
lock = Lock()


def ser1(x, eps, results):
    s = 0
    n = 1
    while True:
        term = (1)**(n + 1) * math.sin(n * x) / n
        if abs(term) < eps:
            break
        else:
            s += term
            n += 1
    with lock:
        results["series1"] = s


def ser2(x, eps, results):
    s = 0
    n = 0
    term = x  
    while abs(term) >= eps:
        s += term
        n += 1
        term *= x**2 / ((2 * n) * (2 * n + 1)) 
    with lock:
        results["series2"] = s


def main():
    results = {}

    x1 = - math.pi / 2
    control1 = math.sin(x1)

    x2 = 2
    control2 = (math.exp(x2) - math.exp(-x2)) / 2

    thread1 = Thread(target=ser1, args=(x1, E, results))
    thread2 = Thread(target=ser2, args=(x2, E, results))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    sum1 = results["series1"]
    sum2 = results["series2"]

    print(f"x1 = {x1}")
    print(f"Sum of series 1: {round(sum1, 7)}")
    print(f"Control value 1: {round(control1, 7)}")
    print(f"Match 1: {round(sum1, 7) == round(control1, 7)}")

    print(f"x2 = {x2}")
    print(f"Sum of series 2: {round(sum2, 7)}")
    print(f"Control value 2: {round(control2, 7)}")
    print(f"Match 2: {round(sum2, 7) == round(control2, 7)}")


if __name__ == "__main__":
    main()
