import math
pi = 0
for i in range(1000000):
    k = i*2 + 1
    if (i % 2) == 0:
        pi = pi + 1/k
    else:
        pi = pi - 1/k

pi = 4*pi
print(pi)