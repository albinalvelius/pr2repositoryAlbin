#Långdistansbuss Paris - Peking

#logga in / registrera som kund
#logga in som admin

#Passagerare samt resan som klasser
#Passagerare identifeiras med Vikt, Ålder, Kön, Namn

import tkinter as tk
from socket import *
from threading import Thread
import time

x = tk.Tk()
c = tk.Canvas(x, bg="white", height=720, width=1280, bd=0)

def connectToServer():
    try:
        global s
        s = socket()
        s.connect(("localhost", 12345)) #"217.208.70.106"
        print("Connection successfull")
        logIn()
    except:
        print("Could not connect to server")
        return

def messageServer(msg):
    e = msg.encode()
    s.send(e)

def logIn():
    def forget():
        try:
            title.place_forget()
            usernameText.place_forget()
            passwordText.place_forget()
            usernameBox.place_forget()
            passwordBox.place_forget()
            loginb.place_forget()
            registerb.place_forget()
            c.delete("all")
        except:
            pass
    title = tk.Label(c, text="Intercontinental Busses", bg="white")
    title.place(anchor=tk.CENTER, x=640, y=170)
    usernameText = tk.Label(c, text="Username", bg="white")
    usernameText.place(anchor=tk.CENTER, x=640, y=280)
    passwordText = tk.Label(c, text="Password", bg="white")
    passwordText.place(anchor=tk.CENTER, x=640, y=330)
    usernameBox = tk.Entry(c, bg="lightgray")
    usernameBox.place(anchor=tk.CENTER, x=640, y=300)
    passwordBox = tk.Entry(c, bg="lightgray")
    passwordBox.place(anchor=tk.CENTER, x=640, y=350)
    loginb = tk.Button(c, text="Log In", command=lambda: messageServer("login" + " " + str(usernameBox.get()) + " " + str(passwordBox.get())))
    loginb.place(anchor=tk.CENTER, x=640, y=380)
    registerb = tk.Button(c, text="Register", command=lambda: messageServer("register" + " " + str(usernameBox.get()) + " " + str(passwordBox.get())))
    registerb.place(anchor=tk.CENTER, x=640, y=420)

connectToServer()

c.pack()
x.mainloop()