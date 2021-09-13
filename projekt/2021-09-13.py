class Elev:
    def __init__(self, name, age, approved):
        self.name = name
        self.age = age
        self.ishappy = approved

elev1 = Elev("Max", 14, False)
print(elev1.name, elev1.age, elev1.ishappy)