input = input("SKRIV TEXT: ")
numbers = 0
for i in input:
    try:
        for x in range(10):
            if int(i) == x:
                numbers = numbers + 1
                break
    except:
        continue
print(numbers)