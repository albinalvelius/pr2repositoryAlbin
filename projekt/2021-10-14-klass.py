class Djur:
    def __init__(self, name):
        self.name = name
    def ät(self):
        print("nom nom")
    def sov(self):
        print("sleep")

class Fisk(Djur):
    def simma(self):
        print("sim sim")

class Haj(Djur):
    def ät(self, Djur):
        print(f'{Djur} munchades upp')

fisk = Fisk("Harald")

fisk.ät()
fisk.sov()
fisk.simma()

haj = Haj("Jeb")
haj.ät("Harald")