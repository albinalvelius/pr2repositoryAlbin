strings = []
i = ""
while i != "x":
    i = input("(x = done) Type input: ")
    if i != "x":
        strings.insert(0, i)
print(strings)