import tkinter as tk
import time
import random as rand
import keyboard
import math

x = tk.Tk()
c = tk.Canvas(x, bg="white", height=720, width=1280)
c.pack()

arrowImg = tk.PhotoImage(file='./projekt/bowsimulator/arrow1.png')
board = tk.PhotoImage(file='./projekt/bowsimulator/board.png')
board = board.subsample(7,7)
bg = tk.PhotoImage(file='./projekt/bowsimulator/bg.png')
cross = tk.PhotoImage(file='./projekt/bowsimulator/cross.png')
cross = cross.subsample(17,17)

bowAnimation = [
    tk.PhotoImage(file='./projekt/bowsimulator/bow1.png'), 
    tk.PhotoImage(file='./projekt/bowsimulator/bow2.png'), 
    tk.PhotoImage(file='./projekt/bowsimulator/bow3.png'),
    tk.PhotoImage(file='./projekt/bowsimulator/bow4.png')]

arrowX = 100
arrowY = 500
arrowYVel = 0
arrowXvel = 0
run = True
fired = False
angle = 0
tension = 0

def gameloop():
    global run, tension, arrowX, arrowY, arrowYVel, arrowXvel, fired, angle
    tension = tension - 0.05
    if tension <= 0:
        tension = 0
    if tension >= 3:
        tension = 3
    print(tension)
    c.create_image(600, 360, image=bg)
    c.create_image(100, 500, image=bowAnimation[int(tension)])
    c.create_image(1200, 400, image=board)
    if not fired:
        if keyboard.is_pressed("w"):
            angle = angle - 0.01
        if keyboard.is_pressed("s"):
            angle = angle + 0.01
        if keyboard.is_pressed("space"):
            tension = tension + 0.15
        if keyboard.is_pressed("q"):
            fired = True
            arrowXvel = math.cos(angle)*10*tension
            arrowYVel = -math.sin(angle)*10*tension

        c.create_image(100 + math.cos(angle)*300, 500 + math.sin(angle)*300, image=cross)
    if fired:
        c.create_image(arrowX, arrowY, image=arrowImg)
        arrowX = arrowX + arrowXvel
        arrowYVel = arrowYVel - 0.5
        arrowY = arrowY + -arrowYVel
    if arrowX >= 1200:
        run = False
    if run:
        c.update()
        time.sleep(1/60)
        c.delete("all")
        gameloop()

gameloop()
x.mainloop()