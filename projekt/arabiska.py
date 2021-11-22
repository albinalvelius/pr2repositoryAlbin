try:
    antal_ord = int(input("Antal ord ? "))
except:
    print("FEL: Ange ett positivt heltal")
    quit()

mening = input("Mening ? ")
arabisk_mening = ""
arabisk_mening_final1 = ""
arabisk_mening_final2 = ""

vocals = "aeiouy"
consonants = "bcdfghjklmnpqrstvwxyz"

for i in range(len(mening)):
    arabisk_mening = arabisk_mening + mening[-i-1]

k = 0
while True:
    a = 0
    b = 0
    try:
        for i in range(len(vocals)):
            if arabisk_mening[k] == vocals[i]:
                if arabisk_mening[k] == arabisk_mening[k+1]:
                    print(arabisk_mening[k], arabisk_mening[k+1])
                    #arabisk_mening_final = arabisk_mening_final + arabisk_mening[k+1]
                    k = k + 1
                    a = 1
        for i in range(len(vocals)):
            if arabisk_mening[k] == vocals[i]:
                for p in range(len(consonants)):
                    if arabisk_mening[k+1] == consonants[p]:
                        for u in range(len(consonants)):
                            if arabisk_mening[k+2] == consonants[u]:
                                b = 1
                                k = k + 1
                                print(arabisk_mening[k], arabisk_mening[k+1], arabisk_mening[k+2])
        if a == 1 and b == 1:
            k = k + 1
    except:
        pass
    arabisk_mening_final1 = arabisk_mening_final1 + arabisk_mening[k]
    k = k + 1
    if k >= len(arabisk_mening):
        break

#Fick det inte att fungara ;(

"""
j = 0
while True:
    try:
        for i in range(len(vocals)):
            if arabisk_mening_final1[j] == vocals[i]:
                for p in range(len(consonants)):
                    if arabisk_mening_final1[j+1] == consonants[p]:
                        for u in range(len(consonants)):
                            if arabisk_mening_final1[j+2] == consonants[u]:
                                j = j + 1
                                print(arabisk_mening_final1[j], arabisk_mening_final1[j+1], arabisk_mening_final1[j+2])
    except:
        pass
    arabisk_mening_final2 = arabisk_mening_final2 + arabisk_mening_final1[j]
    j = j + 1
    if j >= len(arabisk_mening_final1):
        break
"""
print(arabisk_mening_final1)