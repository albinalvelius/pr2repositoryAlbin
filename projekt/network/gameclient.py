from socket import *
from threading import Thread
import tkinter as tk
import keyboard
import time

package = [0, #Ball X
0, #Ball Y
0, #Ball dX
0, #Ball dY
0, #Left player Y
0, #Right player Y
0, #Left player dY
0, #Right player dY
0] #Player score

playerDirection = "neutral"
newPackage = False

x = tk.Tk()
c = tk.Canvas(x, bg="black", height=720, width=1280)
c.pack()

def start_client():
    print("Attempting to connect to server...")
    global s, package, newPackage
    s = socket()
    s.connect(("10.32.34.107", 5006)) #"217.208.70.106"

    def reciever():
        b = s.recv(1024)
        msg = b.decode()
        if msg == "packageRecieve":
            send_data("newPackage")
        if msg[0] == "#":
            num = ""
            for i in msg:
                try:
                    if i == "-":
                        num = num + i
                    else:
                        x = int(i)
                        num = num + i
                except:
                    print(num)
                    if i == " " and i != "#":
                        for i in range(10):
                            if num[0] == str(i):
                                msg1 = ""
                                for k in range(5):
                                    try:
                                        msg1 = msg1 + num[k+1]
                                    except:
                                        break
                                try:
                                    package[i] = int(msg1)
                                except:
                                    print(f'Skumt fel inträffade där msg ({msg1}) på något vis fick en bokstav i sig')
                    num = ""
            print(str(package))        
        reciever()
    rec_thread = Thread(target=reciever)
    rec_thread.start()
    print("Connection successful")
    #send_data("newPackage")
    game_thread = Thread(target=gameloop)
    game_thread.start()


def send_data(msg):
    b = msg.encode()
    s.send(b)
    #print(msg)

def gameloop():
    c.delete("all")
    global playerDirection
    playerDirection1 = playerDirection
    playerDirection = "neutral"
    if keyboard.is_pressed("w"):
        playerDirection = "updateUp"
    if keyboard.is_pressed("s"):
        playerDirection = "updateDown"
    if playerDirection1 != playerDirection:
        send_data(playerDirection)
        #print(package)
    try:
        c.create_text(int(package[0]), int(package[1]), text="0", fill="white")
    except:
        pass
    package[0] = 3*int(package[2]) + int(package[0])
    package[1] = 3*int(package[3]) + int(package[1])
    package[4] = package[4] + package[6]
    package[5] = package[5] + package[7]
    c.create_rectangle(50, package[4]+50, 80, package[4]-50,fill="white")
    c.create_rectangle(1200, package[5]+50, 1230, package[5]-50,fill="white")
    c.create_text(640, 100, text=(f'{str(package[8])[0]}        ||       {str(package[8])[-1]}'), fill="white")
    c.update()
    x.after(30, func = gameloop)

start_client()
x.mainloop()