while True:
    x = int(input("(0 to break) x: "))
    y = int(input("(0 to break) y: "))
    if x > 0:
        if y > 0:
            print("Quadrant 1")
        else:
            print("Quadrant 4")
    else:
        if y > 0:
            print("Quadrant 2")
        else:
            print("Quadrant 3")
    if x == 0 or y == 0:
        break