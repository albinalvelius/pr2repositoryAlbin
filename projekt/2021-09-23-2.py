import math as math
n = 50000
e2 = 0
for i in range(n):
    e2 = e2 + 1/math.factorial(i)
    
e1 = (1+1/n)**n

print(e1-e2)