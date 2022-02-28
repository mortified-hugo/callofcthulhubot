import math


def distance(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    dist = math.sqrt(x ** 2 + y ** 2)
    return round(dist,2)


print(distance((3,1), (-10,2)))