try:
    green_card = int(input("Antal med grönt kort, N ? "))
    red_card = int(input("Antal utan grönt kort, M ? "))
except:
    print("FEL: Ange ett positivt heltal")
    quit()

required_time = 0


if red_card >= green_card:
    required_time = int(required_time + 10*(red_card - (red_card % green_card))/green_card)
    red_card = red_card % green_card

if red_card > 0:
    readyGreenCards = green_card - red_card
    if (readyGreenCards % 2) == 0 and readyGreenCards != 0:
        green_card = green_card - readyGreenCards/2
        required_time = required_time + 10
    elif readyGreenCards != 0:
        green_card = green_card - (readyGreenCards-1)/2
        required_time = required_time + 10

while True:
    if (green_card % 2) == 0 and green_card != 0:
        green_card = green_card/2
        required_time = required_time + 10
    elif green_card > 1:
        green_card = green_card - (green_card-1)/2
        required_time = required_time + 10
    elif green_card == 1:
        green_card = 0
        required_time = required_time + 10
    if green_card == 0:
        break

print(green_card, red_card, required_time)

#Fick inte fram algoritmen som hittar den snabbaste kombinationen