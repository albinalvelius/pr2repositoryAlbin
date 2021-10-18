print("   0 1 2 ")
print("11 X X X 3")
print("10 X X X 4")
print(" 9 X X X 5")
print("   8 7 6")

size = [int(input("ange X storlek: ")), int(input("ange Y storlek: "))]

lamplist = []
for i in range(size[0]*2+size[1]*2):
    lamplist.append(input("Ange r, g, b -> "))

lampcount = size[0] * size[1]