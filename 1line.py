while True:
    inputname = input("name please: ")
    print(f"{((1-(int(inputname, 36))/(int(inputname, 35)))**2)*1000}cm")