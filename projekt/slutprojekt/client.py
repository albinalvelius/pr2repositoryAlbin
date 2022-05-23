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

clients = []
busses = []
clientLabel = []
busLabel = []

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
    global s, clients, busses, clientLabel, busLabel
    b = s.recv(1024)
    msg1 = str(b.decode())
    msg = msg1.split()
    clientLabel.clear()
    busLabel.clear()
    clients.clear()
    busses.clear()
    c.forget()
    for widget in c.winfo_children():
       widget.destroy()
    print(msg)
    if msg[0] == "register": register()
    elif msg[0] == "login": logIn()
    elif msg[0] == "mainmenu": mainmenu()
    elif msg[0] == "logout": logIn()
    elif msg[0] == "adminpage": adminpage()
    elif msg[0] == "clients":
        msg1 = msg1.replace("clients ", "")
        print(msg1)
        k = ""
        for i in msg1:
            if i == ",":
                clients.append(k)
                k = ""
            else:
                k = k + i
        adminpage()
    elif msg[0] == "busses":
        msg1 = msg1.replace("busses ", "")
        print(msg1)
        k = ""
        for i in msg1:
            if i == ",":
                busses.append(k)
                k = ""
            else:
                k = k + i
        adminpage()
    listener()
    
def messageServer(msg):
    e = msg.encode()
    s.send(e)

def adminpage():
    global clientLabel, busLabel
    logoutb = tk.Button(c, text="logout", command=lambda: messageServer("logout"))
    logoutb.place(anchor=tk.NW, x=10, y=10)
    getClients = tk.Button(c, text="Load clients", command=lambda: messageServer("request clients"))
    getClients.place(anchor=tk.NW, x=10, y=50)
    getBusses = tk.Button(c, text="Load busses", command=lambda: messageServer("request busses"))
    getBusses.place(anchor=tk.NW, x=10, y=90)
    for i in range(len(clients)):
        clientLabel.append(tk.Label(c, text=str(clients[i]), bg="white"))
        clientLabel[i].place(anchor=tk.NW, x=50, y=150 + 20*i)
    for i in range(len(busses)):
        busLabel.append(tk.Label(c, text=str(busses[i]), bg="white"))
        busLabel[i].place(anchor=tk.NE, x=1230, y=150 + 20*i)
    idE = tk.Entry(c, bg="lightgray")
    idE.place(anchor=tk.NW, x=640, y=150)
    first_nameE = tk.Entry(c, bg="lightgray")
    first_nameE.place(anchor=tk.NW, x=640, y=180)
    last_nameE = tk.Entry(c, bg="lightgray")
    last_nameE.place(anchor=tk.NW, x=640, y=210)
    ageE = tk.Entry(c, bg="lightgray")
    ageE.place(anchor=tk.NW, x=640, y=240)
    heightE = tk.Entry(c, bg="lightgray")
    heightE.place(anchor=tk.NW, x=640, y=270)
    usernameE = tk.Entry(c, bg="lightgray")
    usernameE.place(anchor=tk.NW, x=640, y=300)
    passwordE = tk.Entry(c, bg="lightgray")
    passwordE.place(anchor=tk.NW, x=640, y=330)

    registerclientb = tk.Button(c, text="REGISTER NEW CLIENT", command=lambda: messageServer("registerClient" + " " + str(first_nameE.get()) + " " + str(last_nameE.get()) + " " + str(ageE.get()) + " " + str(heightE.get()) + " " + str(usernameE.get()) + " " + str(passwordE.get())))
    registerclientb.place(anchor=tk.NW, x=640, y=50)
    delclientb = tk.Button(c, text="DELETE CLIENT", command=lambda: messageServer("deleteClient " + str(idE.get())))
    delclientb.place(anchor=tk.NW, x=640, y=80)
    editclientb = tk.Button(c, text="EDIT CLIENT", command=lambda: messageServer("editClient " + str(idE.get()) + " " + str(first_nameE.get()) + " " + str(last_nameE.get()) + " " + str(ageE.get()) + " " + str(heightE.get()) + " " + str(usernameE.get()) + " " + str(passwordE.get())))
    editclientb.place(anchor=tk.NW, x=640, y=110)

    registerbusb = tk.Button(c, text="REGISTER NEW BUS", command=lambda: messageServer("registerBus " + str(first_nameE.get()) + " " + str(last_nameE.get()) + " " + str(ageE.get())))
    registerbusb.place(anchor=tk.NW, x=640, y=350)
    delbusb = tk.Button(c, text="DELETE BUS", command=lambda: messageServer("deleteBus " + str(idE.get())))
    delbusb.place(anchor=tk.NW, x=640, y=380)
    editbusb = tk.Button(c, text="EDIT BUS", command=lambda: messageServer("editBus " + str(idE.get()) + " " + str(first_nameE.get()) + " " + str(last_nameE.get()) + " " + str(ageE.get())))
    editbusb.place(anchor=tk.NW, x=640, y=410)

    idl = tk.Label(c, text="ID:", bg="white")
    idl.place(anchor=tk.NE, x=640, y=150)
    first_namel = tk.Label(c, text="First Name / Bus From:", bg="white")
    first_namel.place(anchor=tk.NE, x=640, y=180)
    last_namel = tk.Label(c, text="Last Name / Bus To:", bg="white")
    last_namel.place(anchor=tk.NE, x=640, y=210)
    agel = tk.Label(c, text="Age / Brand:", bg="white")
    agel.place(anchor=tk.NE, x=640, y=240)
    heightl = tk.Label(c, text="Height:", bg="white")
    heightl.place(anchor=tk.NE, x=640, y=270)
    usernamel = tk.Label(c, text="Username:", bg="white")
    usernamel.place(anchor=tk.NE, x=640, y=300)
    passwordl = tk.Label(c, text="Password:", bg="white")
    passwordl.place(anchor=tk.NE, x=640, y=330)

    c.pack()

def mainmenu():
    title = tk.Label(c, text="Main Menu", bg="white")
    title.place(anchor=tk.NE, x=640, y=150)
    logoutb = tk.Button(c, text="logout", command=lambda: messageServer("logout"))
    logoutb.place(anchor=tk.NW, x=10, y=10)
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
    logoutb = tk.Button(c, text="logout", command=lambda: messageServer("Back"))
    logoutb.place(anchor=tk.NW, x=10, y=10)
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