import math as m
cellRadius = 500 / (3**0.5)

a = (709, -768)
b = (3 * cellRadius, -1500)
print(m.dist(a, b))

n = 9


def test(a):
    a += 1
    print(a)


test(n)
print(n)
