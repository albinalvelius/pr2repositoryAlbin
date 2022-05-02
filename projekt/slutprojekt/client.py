#Långdistansbuss Paris - Peking

#logga in / registrera som kund
#logga in som admin

#Passagerare samt resan som klasser
#Passagerare identifeiras med Vikt, Ålder, Kön, Namn

import tkinter as tk
from tkinter import *
from socket import *
from threading import Thread
import time

x = tk.Tk()
c = tk.Frame(x, bg="white", height=720, width=1280, bd=0)
c.pack()

def connectToServer():
    try:
        global s
        s = socket()
        s.connect(("localhost", 12345)) #"217.208.70.106"
        print("Connection successfull")
        listenThread = Thread(target=listener)
        listenThread.start()
        logIn()
    except:
        print("Could not connect to server")
        return

def listener():
    global s
    b = s.recv(1024)
    msg = str(b.decode())
    msg = msg.split()
    c.forget()
    for widget in c.winfo_children():
       widget.destroy()
    print(msg)
    if msg[0] == "register":
        register()
    if msg[0] == "login":
        logIn()
    if msg[0] == "mainmenu":
        mainmenu()
    if msg[0] == "logout":
        logIn()
    listener()

def messageServer(msg):
    e = msg.encode()
    s.send(e)

def mainmenu():
    title = tk.Label(c, text="Main Menu", bg="white")
    title.place(anchor=tk.NE, x=640, y=150)
    registerb = tk.Button(c, text="REGISTER", command=lambda: messageServer("logout"))
    registerb.place(anchor=tk.CENTER, x=640, y=420)
    c.pack()

def register():
    title = tk.Label(c, text="Intercontinental Busses", bg="white")
    title.place(anchor=tk.NE, x=640, y=150)
    first_name = tk.Label(c, text="First Name:", bg="white")
    first_name.place(anchor=tk.NE, x=640, y=180)
    last_name = tk.Label(c, text="Last Name:", bg="white")
    last_name.place(anchor=tk.NE, x=640, y=210)
    age = tk.Label(c, text="Age:", bg="white")
    age.place(anchor=tk.NE, x=640, y=240)
    height = tk.Label(c, text="Height:", bg="white")
    height.place(anchor=tk.NE, x=640, y=270)
    username = tk.Label(c, text="Username:", bg="white")
    username.place(anchor=tk.NE, x=640, y=300)
    password = tk.Label(c, text="Password:", bg="white")
    password.place(anchor=tk.NE, x=640, y=330)

    first_name1 = tk.Entry(c, bg="lightgray")
    first_name1.place(anchor=tk.NW, x=640, y=180)
    last_name1 = tk.Entry(c, bg="lightgray")
    last_name1.place(anchor=tk.NW, x=640, y=210)
    age1 = tk.Entry(c, bg="lightgray")
    age1.place(anchor=tk.NW, x=640, y=240)
    height1 = tk.Entry(c, bg="lightgray")
    height1.place(anchor=tk.NW, x=640, y=270)
    username1 = tk.Entry(c, bg="lightgray")
    username1.place(anchor=tk.NW, x=640, y=300)
    password1 = tk.Entry(c, bg="lightgray")
    password1.place(anchor=tk.NW, x=640, y=330)

    registerb = tk.Button(c, text="REGISTER", command=lambda: messageServer("registerClient" + " " + str(first_name1.get()) + " " + str(last_name1.get()) + " " + str(age1.get()) + " " + str(height1.get()) + " " + str(username1.get()) + " " + str(password1.get())))
    registerb.place(anchor=tk.CENTER, x=640, y=420)
    c.pack()


def logIn():
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
    c.pack()

connectToServer()

x.mainloop()