def food(s, vegan=False):
    if s == "mjölk":
        if vegan:
            print("sojamjölk")
        else:
            print("mjölk")

food(input("Välj mat: "), True)