try:
    kuvert_vikt = int(input("Kuvert ? "))
    affish_vikt = int(input("Affish ? "))
    blad_vikt = int(input("Blad ? "))
except:
    print("FEL: Ange ett positivt heltal")
    quit()

totalvikt = 2*kuvert_vikt*(0.229*0.324) + 2*affish_vikt*(0.297*0.420) + blad_vikt*(0.210*0.297)
print("Svar:", totalvikt)