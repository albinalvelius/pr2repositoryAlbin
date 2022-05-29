#Långdistansbuss Paris - Peking

#logga in / registrera som kund
#logga in som admin

#Passagerare samt resan som klasser
#Passagerare identifeiras med Ålder, Kön, Namn

import tkinter as tk
from tkinter import *
from socket import *
from threading import Thread
import time
from functools import partial

clients = []
busses = []
bookings = []
clientLabel = []
busLabel = []
bookingLabel = []

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

def clearLabels():
    clientLabel.clear()
    bookingLabel.clear()
    busLabel.clear()

def clearLists():
    clients.clear()
    busses.clear()
    bookings.clear()

def listener():
    global s, clients, busses, bookings, clientLabel, busLabel
    b = s.recv(1024)
    msg1 = str(b.decode())
    msg = msg1.split()
    c.forget()
    for widget in c.winfo_children():
       widget.destroy()
    clearLabels()
    #print(msg1)
    if msg[0] == "register": register()
    elif msg[0] == "mainmenu": mainmenu()
    elif msg[0] == "logout": 
        clearLists()
        logIn()
    elif msg[0] == "adminpage": 
        clearLists()
        adminpage()
    elif msg[0] == "myprofile": myProfile()
    elif msg[0] == "clients" or msg[0] == "busses" or msg[0] == "bookings":
        clearLists()
        msg1 = msg1.replace(f"{msg[0]} ", "")
        #print(msg1)
        k = ""
        for i in msg1:
            if i == ",":
                if msg[0] == "clients": clients.append(k)
                elif msg[0] == "busses": busses.append(k)
                elif msg[0] == "bookings": bookings.append(k)
                k = ""
            else:
                k = k + i
        adminpage()
    elif msg[0] == "login": 
        clearLists()
        msg1 = msg1.replace(f"{msg[0]} ", "")
        #print(msg1)
        k = ""
        p = 0
        for i in msg1:
            if i == "!":
                p = p + 1
            if i == ",":
                if p == 0: busses.append(k)
                elif p == 1: clients.append(k)
                elif p == 2: bookings.append(k)
                k = ""
            elif i != "!":
                k = k + i
        try:
            clients = clients[0].split()
        except:
            pass
        #print(str(clients))
        mainmenu()
    listener()
    
def messageServer(msg):
    e = msg.encode()
    s.send(e)

def adminpage():
    global clientLabel, busLabel, bookingLabel
    logoutb = tk.Button(c, text="logout", command=lambda: messageServer("logout"))
    logoutb.place(anchor=tk.NW, x=10, y=10)
    getClients = tk.Button(c, text="Load clients", command=lambda: messageServer("request clients"))
    getClients.place(anchor=tk.NW, x=10, y=40)
    getBusses = tk.Button(c, text="Load busses", command=lambda: messageServer("request busses"))
    getBusses.place(anchor=tk.NW, x=10, y=70)
    getBookings = tk.Button(c, text="Load Bookings", command=lambda: messageServer("request bookings"))
    getBookings.place(anchor=tk.NW, x=10, y=100)
    for i in range(len(clients)):
        clientLabel.append(tk.Label(c, text=str(clients[i]), bg="white"))
        clientLabel[i].place(anchor=tk.NW, x=50, y=150 + 20*i)
    for i in range(len(busses)):
        busLabel.append(tk.Label(c, text=str(busses[i]), bg="white"))
        busLabel[i].place(anchor=tk.NW, x=50, y=150 + 20*i)
    for i in range(len(bookings)):
        busLabel.append(tk.Label(c, text=str(bookings[i]), bg="white"))
        busLabel[i].place(anchor=tk.NW, x=50, y=150 + 20*i)
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
    registerclientb.place(anchor=tk.NW, x=780, y=150)
    delclientb = tk.Button(c, text="DELETE CLIENT", command=lambda: messageServer("deleteClient " + str(idE.get())))
    delclientb.place(anchor=tk.NW, x=780, y=180)
    editclientb = tk.Button(c, text="EDIT CLIENT", command=lambda: messageServer("editClient " + str(idE.get()) + " " + str(first_nameE.get()) + " " + str(last_nameE.get()) + " " + str(ageE.get()) + " " + str(heightE.get()) + " " + str(usernameE.get()) + " " + str(passwordE.get())))
    editclientb.place(anchor=tk.NW, x=780, y=210)

    registerbusb = tk.Button(c, text="REGISTER NEW BUS", command=lambda: messageServer("registerBus " + str(first_nameE.get()) + " " + str(last_nameE.get()) + " " + str(ageE.get()) + " " + str(heightE.get())))
    registerbusb.place(anchor=tk.NW, x=780, y=240)
    delbusb = tk.Button(c, text="DELETE BUS", command=lambda: messageServer("deleteBus " + str(idE.get())))
    delbusb.place(anchor=tk.NW, x=780, y=270)
    editbusb = tk.Button(c, text="EDIT BUS", command=lambda: messageServer("editBus " + str(idE.get()) + " " + str(first_nameE.get()) + " " + str(last_nameE.get()) + " " + str(ageE.get()) + " " + str(heightE.get())))
    editbusb.place(anchor=tk.NW, x=780, y=300)

    idl = tk.Label(c, text="ID:", bg="white")
    idl.place(anchor=tk.NE, x=640, y=150)
    first_namel = tk.Label(c, text="First Name / Bus From:", bg="white")
    first_namel.place(anchor=tk.NE, x=640, y=180)
    last_namel = tk.Label(c, text="Last Name / Bus To:", bg="white")
    last_namel.place(anchor=tk.NE, x=640, y=210)
    agel = tk.Label(c, text="Age / Brand:", bg="white")
    agel.place(anchor=tk.NE, x=640, y=240)
    heightl = tk.Label(c, text="Height / Departure Date:", bg="white")
    heightl.place(anchor=tk.NE, x=640, y=270)
    usernamel = tk.Label(c, text="Username:", bg="white")
    usernamel.place(anchor=tk.NE, x=640, y=300)
    passwordl = tk.Label(c, text="Password:", bg="white")
    passwordl.place(anchor=tk.NE, x=640, y=330)
    
    bookingClientID = tk.Entry(c, bg="lightgray")
    bookingClientID.place(anchor=tk.NW, x=640, y=390)
    bookingBusID = tk.Entry(c, bg="lightgray")
    bookingBusID.place(anchor=tk.NW, x=640, y=420)

    clientIDLabel = tk.Label(c, text="Client ID / Booking ID:", bg="white")
    clientIDLabel.place(anchor=tk.NE, x=640, y=390)
    busIDLabel = tk.Label(c, text="Bus ID:", bg="white")
    busIDLabel.place(anchor=tk.NE, x=640, y=420)
    
    bookingb = tk.Button(c, text="Insert Booking", command=lambda: messageServer("insertBooking " + str(bookingClientID.get()) + " " + str(bookingBusID.get())))
    bookingb.place(anchor=tk.NW, x=780, y=385)
    removebookingb = tk.Button(c, text="Delete Booking", command=lambda: messageServer("deleteBooking " + str(bookingClientID.get())))
    removebookingb.place(anchor=tk.NW, x=780, y=415)
    
    c.pack()

def myProfile():
    title = tk.Label(c, text="Settings: ", bg="white")
    title.place(anchor=tk.NE, x=940, y=100)
    deleteProfileb = tk.Button(c, text="Delete Profile", command=lambda: messageServer(f"deleteClient {clients[0]}"))
    deleteProfileb.place(anchor=tk.NW, x=940, y=100)
    backb = tk.Button(c, text="Back", command=lambda: messageServer(f"login {clients[5]} {clients[6]}"))
    backb.place(anchor=tk.NW, x=10, y=10)
    editclientb = tk.Button(c, text="Edit Profile", command=lambda: messageServer("editClient " + str(clients[0]) + " " + str(first_nameE.get()) + " " + str(last_nameE.get()) + " " + str(ageE.get()) + " " + str(heightE.get()) + " " + str(usernameE.get()) + " " + str(passwordE.get())))
    editclientb.place(anchor=tk.NW, x=940, y=130)

    first_namel = tk.Label(c, text="First Name:", bg="white")
    first_namel.place(anchor=tk.NE, x=940, y=180)
    last_namel = tk.Label(c, text="Last Name:", bg="white")
    last_namel.place(anchor=tk.NE, x=940, y=210)
    agel = tk.Label(c, text="Age:", bg="white")
    agel.place(anchor=tk.NE, x=940, y=240)
    heightl = tk.Label(c, text="Height:", bg="white")
    heightl.place(anchor=tk.NE, x=940, y=270)
    usernamel = tk.Label(c, text="Username:", bg="white")
    usernamel.place(anchor=tk.NE, x=940, y=300)
    passwordl = tk.Label(c, text="Password:", bg="white")
    passwordl.place(anchor=tk.NE, x=940, y=330)

    first_nameE = tk.Entry(c, bg="lightgray")
    first_nameE.place(anchor=tk.NW, x=940, y=180)
    last_nameE = tk.Entry(c, bg="lightgray")
    last_nameE.place(anchor=tk.NW, x=940, y=210)
    ageE = tk.Entry(c, bg="lightgray")
    ageE.place(anchor=tk.NW, x=940, y=240)
    heightE = tk.Entry(c, bg="lightgray")
    heightE.place(anchor=tk.NW, x=940, y=270)
    usernameE = tk.Entry(c, bg="lightgray")
    usernameE.place(anchor=tk.NW, x=940, y=300)
    passwordE = tk.Entry(c, bg="lightgray")
    passwordE.place(anchor=tk.NW, x=940, y=330)

    for i in range(len(clients)-1):
        clientLabel.append(tk.Label(c, text=str(clients[i+1]), bg="white"))
        clientLabel[i].place(anchor=tk.NW, x=1080, y=180 + 30*i)

    myBookings = tk.Label(c, text="My active bookings: ", bg="white")
    myBookings.place(anchor=tk.NE, x=200, y=100)

    print(bookings)
    bookingbutton = []
    u = 0
    for i in range(len(bookings)):
        k = bookings[i].split()
        if k[1] == clients[0]:
            for p in range(len(busses)):
                j = busses[p].split()
                if k[2] == j[0]:
                    print(j[0])
                    bookingLabel.append(tk.Label(c, text=f"From {j[1]} to {j[2]}. Brand: {j[3]}. Date of Departure: {j[4]}", bg="white"))
                    bookingLabel[u].place(anchor=tk.NW, x=200, y=130 + 30*u)
                    funca = partial(messageServer, f"deleteBooking {k[0]}")
                    bookingbutton.append(tk.Button(c, text="Delete this Booking", command=funca))
                    bookingbutton[u].place(anchor=tk.NE, x=200, y=130 + 30*u)
                    u = u + 1
    
    """IdL = tk.Label(c, text="Bus ID", bg="white")
    IdL.place(anchor=tk.CENTER, x=780, y=100)
    IdE = tk.Entry(c, bg="lightgray")
    IdE.place(anchor=tk.CENTER, x=780, y=130)
    bookButton = tk.Button(c, text="Remove booking with b.ID", command=lambda: messageServer(f"deleteBooking {IdE.get()}"))
    bookButton.place(anchor=tk.CENTER, x=780, y=160)"""

    c.pack()

def mainmenu():
    title = tk.Label(c, text=f'Welcome {clients[1]} {clients[2]}', bg="white")
    title.place(anchor=tk.CENTER, x=640, y=20)
    logoutb = tk.Button(c, text="logout", command=lambda: messageServer("logout"))
    logoutb.place(anchor=tk.NW, x=10, y=10)
    profileb = tk.Button(c, text="My Profile", command=lambda: messageServer("myprofile"))
    profileb.place(anchor=tk.NE, x=1270, y=10)

    bussesl = tk.Label(c, text="Avaliable busses:", bg="white")
    bussesl.place(anchor=tk.NE, x=200, y=100)
    """
    for i in range(len(busses)):
        j = busses[i].split()
        #print("j: " + str(j))
        busLabel.append(tk.Label(c, text=f"ID: {j[0]}. From {j[1]} to {j[2]}. Brand: {j[3]}. Date of Departure: {j[4]}", bg="white"))
        busLabel[i].place(anchor=tk.NW, x=200, y=100 + 30*i)
    
    IdL = tk.Label(c, text="ID of the bus you wish to book", bg="white")
    IdL.place(anchor=tk.CENTER, x=740, y=100)
    IdE = tk.Entry(c, bg="lightgray")
    IdE.place(anchor=tk.CENTER, x=740, y=130)
    bookButton = tk.Button(c, text="Book bus with suggested ID", command=lambda: messageServer(f"insertBooking {clients[0]} {IdE.get()}"))
    bookButton.place(anchor=tk.CENTER, x=740, y=160)"""
    
    bookingbutton = []
    for i in range(len(busses)):
        j = busses[i].split()
        print("j: " + str(j))
        busLabel.append(tk.Label(c, text=f"From {j[1]} to {j[2]}. Brand: {j[3]}. Date of Departure: {j[4]}", bg="white"))
        busLabel[i].place(anchor=tk.NW, x=200, y=130 + 30*i)
        print(j[0])
        funca = partial(messageServer, f"insertBooking {clients[0]} {j[0]}")
        bookingbutton.append(tk.Button(c, text="Book this Bus!" + j[0], command=funca))
        bookingbutton[i].place(anchor=tk.NE, x=200, y=130 + 30*i)
    
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
    logoutb = tk.Button(c, text="Back", command=lambda: messageServer("logout"))
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