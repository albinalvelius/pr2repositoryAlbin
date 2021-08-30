input = str(input("Skriv TEXT! "))
konsonantLista = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "z", "x"]
newString = ""
for i in input:
    print(i)
    for k in konsonantLista:
        if i != k:
            newString = newString + i + "o"
            break
        else:
            break
    if i == "b":
        newString = newString + "bob"
    if i == "f":
        newString = newString + "fof"
print(newString)
