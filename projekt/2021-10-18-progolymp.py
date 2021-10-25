print("   0 1 2 ")
print("11 X X X 3")
print("10 X X X 4")
print(" 9 X X X 5")
print("   8 7 6")

size = [int(input("ange X storlek: ")), int(input("ange Y storlek: "))]

lamplist = []
for i in range(size[0]*2+size[1]*2):
    lamplist.append(input())

lampcount = size[0] * size[1]
squareList = []

class Xlist():
    def __init__(self, r, g, b, x, y):
        self.r = r
        self.g = g
        self.b = b
        self.x = x
        self.y = y

for i in range(size[0]):
    for k in range(size[1]):
        squareList.append(Xlist(False, False, False, i, k))

for h in range(size[0]*2+size[1]*2):
    if h <= size[0]-1:
        print(1)
        for k in range(size[0]):
            for j in range(len(squareList)):
                if squareList[j].x == k:
                    print("A")
                    if lamplist[h] == "r":
                        squareList[j].r = True
                    if lamplist[h] == "g":
                        squareList[j].g = True
                    if lamplist[h] == "b":
                        squareList[j].b = True
    elif size[0]-1 < h <= size[0]+size[1]-1:
        print(2)
        for k in range(size[1]):
            for j in range(len(squareList)):
                if squareList[j].y == k:
                    print("B")
                    if lamplist[h] == "r":
                        squareList[j].r = True
                    if lamplist[h] == "g":
                        squareList[j].g = True
                    if lamplist[h] == "b":
                        squareList[j].b = True
    elif size[0]+size[1]-1 < h <= 2*size[0]+size[1]-1:
        print(3)
        for k in range(size[0]):
            for j in range(len(squareList)):
                if squareList[j].x == k:
                    print("C")
                    if lamplist[h] == "r":
                        squareList[j].r = True
                    if lamplist[h] == "g":
                        squareList[j].g = True
                    if lamplist[h] == "b":
                        squareList[j].b = True
    elif 2*size[0]+size[1]-1 < h <= 2*size[0]+2*size[1]-1:
        print(4)
        for k in range(size[1]):
            for j in range(len(squareList)):
                if squareList[j].y == k:
                    print("D")
                    if lamplist[h] == "r":
                        squareList[j].r = True
                    if lamplist[h] == "g":
                        squareList[j].g = True
                    if lamplist[h] == "b":
                        squareList[j].b = True
    else:
        pass

"""
for i in range(size[0]*2+size[1]*2):
    if i <= size[0]-1:
        for k in range(size[1]):
            for j in range(len(squareList)):
                if squareList[j].x == i:
                    print(1)
                    if lamplist[j] == "r":
                        squareList[j].r = True
                    if lamplist[j] == "g":
                        squareList[j].g = True
                    if lamplist[j] == "b":
                        squareList[j].b = True
    elif size[0]-1 < i <= size[0]+size[1]-1:
        for k in range(size[1]):
            for j in range(len(squareList)):
                if squareList[j].y == i:
                    print(2)
                    if lamplist[j] == "r":
                        squareList[j].r = True
                    if lamplist[j] == "g":
                        squareList[j].g = True
                    if lamplist[j] == "b":
                        squareList[j].b = True
    elif size[0]+size[1]-1 < i <= 2*size[0]+size[1]-1:
        for k in range(size[1]):
            for j in range(len(squareList)):
                if squareList[j].x == i:
                    print(3)
                    if lamplist[j] == "r":
                        squareList[j].r = True
                    if lamplist[j] == "g":
                        squareList[j].g = True
                    if lamplist[j] == "b":
                        squareList[j].b = True
    elif 2*size[0]+size[1]-1 < i <= 2*size[0]+2*size[1]-1:
        for k in range(size[1]):
            for j in range(len(squareList)):
                if squareList[j].y == i:
                    print(4)
                    if lamplist[j] == "r":
                        squareList[j].r = True
                    if lamplist[j] == "g":
                        squareList[j].g = True
                    if lamplist[j] == "b":
                        squareList[j].b = True
    else:
        pass
"""
for i in range(len(squareList)):
    if squareList[i].r == True and squareList[i].g == True and squareList[i].b == True:
        print("sus")