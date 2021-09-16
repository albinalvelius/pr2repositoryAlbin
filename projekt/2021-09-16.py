def addNumbers(number):
    sum = 0
    for i in range(len(number)):
        sum = sum + int(number[i])
    print(sum)

addNumbers(str(input("Input: ")))