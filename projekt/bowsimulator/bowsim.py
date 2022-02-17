from glob import glob
import threading
import tkinter as tk
import time
import random as rand
from tkinter.constants import ANCHOR
from tokenize import Triple
from turtle import color
from typing import Text
import keyboard
import math
from socket import *
from threading import Thread

x = tk.Tk()
c = tk.Canvas(x, bg="white", height=720, width=1280)
c.pack()

arrowImg = tk.PhotoImage(file='./projekt/bowsimulator/arrow1.png')
board = tk.PhotoImage(file='./projekt/bowsimulator/board.png')
board = board.subsample(5,5)
bg = tk.PhotoImage(file='./projekt/bowsimulator/bg.png')
cross = tk.PhotoImage(file='./projekt/bowsimulator/cross.png')
cross = cross.subsample(17,17)
uibg = tk.PhotoImage(file="./projekt/bowsimulator/uibg.png")
button1 = tk.PhotoImage(file="./projekt/bowsimulator/button1.png")
button2 = tk.PhotoImage(file="./projekt/bowsimulator/button2.png")
button3 = tk.PhotoImage(file="./projekt/bowsimulator/button3.png")
button4 = tk.PhotoImage(file="./projekt/bowsimulator/button4.png")
textingimg = tk.PhotoImage(file="./projekt/bowsimulator/texting.png")
iphone = tk.PhotoImage(file="./projekt/bowsimulator/iphone6.png")

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
g = 0.5
score = False
latestScore = 0
highScore = 0
boardY = 450
shakeFactor = 1
boardSpeed = 1
boardSpeedScale = 0
msglist = []
isOnline = False

def gameloop():
    c.delete("all")
    global run, tension, arrowX, arrowY, arrowYVel, arrowXvel, fired, angle, g, score, latestScore, highScore, boardY, boardSpeed, boardSpeedScale, isOnline
    tension = tension - 0.05
    if tension <= 0:
        tension = 0
    if tension >= 3:
        tension = 3
    if boardY >= 660 or boardY <= 60:
        boardSpeed = -boardSpeed
    boardY = boardY + boardSpeedScale * boardSpeed
    c.create_image(600, 360, image=bg)
    c.create_image(100+shakeFactor*rand.randint(0, int((int(tension))-tension/2)), 500+int(shakeFactor*(rand.randint(0, int(tension))-tension/2)), image=bowAnimation[int(tension)])
    c.create_image(1200, boardY, anchor=tk.CENTER, image=board)
    if not fired:
        angle = angle + shakeFactor*0.005*(rand.randint(0, int(tension)) - rand.randint(0, int(tension)))
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
            tension = 0
        c.create_image(100 + math.cos(angle)*300, 500 + math.sin(angle)*300, image=cross)
    if fired:
        c.create_image(arrowX, arrowY, image=arrowImg)
        arrowX = arrowX + arrowXvel
        arrowYVel = arrowYVel - g
        arrowY = arrowY + -arrowYVel
        if keyboard.is_pressed("r"):
            fired = False
            run = True
            arrowX = 100
            arrowY = 500
            arrowXvel = 0
            arrowYVel = 0
            g = 0.5
            score = False
            if boardSpeedScale > 0:
                boardSpeed = 1
    if arrowX >= 1160:
        arrowYVel = 0
        arrowXvel = 0
        g = 0
        boardSpeed = 0
        score = True
    if tension != 0:
        c.create_rectangle(30, 30, 30 + tension*50, 50, fill="red")
    if score:
        latestScore = 1000-10*int(abs(boardY-arrowY))
        if latestScore < 0:
            latestScore = 0
        c.create_text(400, 400, text=f"SCORE: {latestScore}", fill="red", font=('Helvetica','30','bold'))
        if latestScore > highScore:
            highScore = latestScore
    if highScore > 0:
        c.create_text(1100, 50, text=f"HIGHSCORE: {highScore}", fill="black", font=('Helvetica','30','bold'))
    c.create_text(20, 60, anchor=tk.NW, text=f"Aim: W/S", fill="black", font=('Helvetica','10','bold'))
    c.create_text(20, 80, anchor=tk.NW, text=f"Charge: Space", fill="black", font=('Helvetica','10','bold'))
    c.create_text(20, 100, anchor=tk.NW, text=f"Fire: Q", fill="black", font=('Helvetica','10','bold'))
    c.create_text(20, 120, anchor=tk.NW, text=f"Reset: R", fill="black", font=('Helvetica','10','bold'))
    c.update()
    x.after(17, func = gameloop)

def online_chat(s, msg, host, conn):
    c.delete("all")
    c.create_image(640, 360, image=textingimg)
    c.create_image(150, 360, image=iphone)
    msglist.append(msg)
    for i in range(len(msglist)):
        c.create_text(100, 650 - 20*i, text=msglist[i])
    inputtext = tk.Text(c, height=10, width=20)
    inputtext.place(anchor=tk.CENTER, x=470, y=550)
    def sendmsg():
        msg = inputtext.get(1.0, "end-1c")
        b = msg.encode()
        s.send(b)
        for i in range(len(msglist)):
            c.create_text(100, 100 + 20*i, text=msglist[-(i+1)])
    a = tk.Button(c, text="SEND!", command=sendmsg)
    a.place(anchor=tk.CENTER, x=464, y=676)

def start_client(host, port):
    s = socket()
    s.connect((host, port))
    def reciever():
        b = s.recv(1024)
        msg = b.decode()
        online_chat(s, msg, False, "")
        print(msg)
        reciever()
    rec_thread = Thread(target=reciever)
    rec_thread.start()
    online_chat(s, "", False, "")

def startUI():
    c.delete("all")
    def serverDir():
        exitToChat(False)
    def clientDir():
        exitToChat(True)
    def diff1():
        global shakeFactor
        shakeFactor = 0
        forgetButtons()
        gameloop()
    def diff2():
        global shakeFactor, boardSpeedScale
        shakeFactor = 0
        boardSpeedScale = 1
        forgetButtons()
        gameloop()
    def diff3():
        global shakeFactor, boardSpeedScale
        shakeFactor = 1
        boardSpeedScale = 1
        forgetButtons()
        gameloop()
    def diff4():
        global shakeFactor, boardSpeedScale
        shakeFactor = 3
        boardSpeedScale = 10
        forgetButtons()
        gameloop()
    def exitToChat(client):
        if client:
            start_client(str(ip.get(1.0, "end-1c")), int(port.get(1.0, "end-1c")))
        else:
            start_server(str(ip.get(1.0, "end-1c")), int(port.get(1.0, "end-1c")))
        forgetButtons()
    def forgetButtons():
        try:
            a.place_forget()
            b.place_forget()
            d.place_forget()
            e.place_forget()
            f.place_forget()
            g.place_forget()
            h.place_forget()
            i.place_forget()
            ip.place_forget()
            port.place_forget()
        except:
            pass
        c.delete("all")
    def setOnline():
        global isOnline
        isOnline = True
        forgetButtons()
        startUI()
    def setOffline():
        global isOnline
        isOnline = False
        forgetButtons()
        startUI()
    c.create_image(600, 360, image=uibg)
    a = tk.Button(c, image=button1, command=diff1)
    a.place(anchor=tk.CENTER, x=464, y=676)
    b = tk.Button(c, image=button2, command=diff2)
    b.place(anchor=tk.CENTER, x=693, y=668)
    d = tk.Button(c, image=button3, command=diff3)
    d.place(anchor=tk.CENTER, x=938, y=669)
    e = tk.Button(c, image=button4, command=diff4)
    e.place(anchor=tk.CENTER, x=1190, y=669)
    f = tk.Button(c, text="START SERVER", command=serverDir)
    g = tk.Button(c, text="START CLIENT", command=clientDir)
    c.create_text(464, 560, anchor=tk.CENTER, text=f"EASY", fill="black", font=('Helvetica','10','bold'))
    c.create_text(693, 560, anchor=tk.CENTER, text=f"MEDIUM", fill="black", font=('Helvetica','10','bold'))
    c.create_text(938, 560, anchor=tk.CENTER, text=f"HARD", fill="black", font=('Helvetica','10','bold'))
    c.create_text(1190, 560, anchor=tk.CENTER, text=f"VERY HARD", fill="black", font=('Helvetica','10','bold'))
    c.create_text(900, 100, anchor=tk.CENTER, text=f"Ultra Accurate Bow Simulator v1.0.2", fill="red", font=('Helvetica','30','bold'))
    if isOnline:
        c.create_text(900, 170, anchor=tk.CENTER, text=f"ONLINE: {isOnline}", fill="green", font=('Helvetica','30','bold'))
        c.create_text(800, 200, anchor=tk.CENTER, text=f"IP: ", fill="green", font=('Helvetica','15','bold'))
        c.create_text(800, 220, anchor=tk.CENTER, text=f"PORT: ", fill="green", font=('Helvetica','15','bold'))
        ip = tk.Text(c, height=1, width=15)
        ip.place(anchor=tk.CENTER, x=900, y=200)
        port = tk.Text(c, height=1, width=15)
        port.place(anchor=tk.CENTER, x=900, y=220)
        f.place(anchor=tk.CENTER, x=300, y=400)
        g.place(anchor=tk.CENTER, x=300, y=440)
    else:
        c.create_text(900, 170, anchor=tk.CENTER, text=f"ONLINE: {isOnline}", fill="red", font=('Helvetica','30','bold'))
    h = tk.Button(c, text="SET ONLINE", command=setOnline)
    h.place(anchor=tk.CENTER, x=800, y=440)
    i = tk.Button(c, text="SET OFFLINE", command=setOffline)
    i.place(anchor=tk.CENTER, x=800, y=480)


startUI()
x.mainloop()