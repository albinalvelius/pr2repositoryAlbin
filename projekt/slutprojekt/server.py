from socket import *
from threading import Thread
import time
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="databas"
)
mycursor = mydb.cursor()
print("Uppkopplad till databasen!")

host = ""
port = 12345
conn = []
addr = []
clientList = []
threadcount = 0
msg = ""

s = socket()
s.bind((host, port))
s.listen()

# Funktion som kollar efter bokningar som innehåller bussar/användare som inte längre finns kvar och tar bort
# eventuella bokningar efter behov
def clearUnusedBookings(): 
    mycursor.execute("SELECT * FROM client_info") 
    clientinfo = mycursor.fetchall()
    mycursor.execute("SELECT * FROM bus_trips")
    bustrips = mycursor.fetchall()
    mycursor.execute("SELECT * FROM client_booking")
    clientbookings = mycursor.fetchall()
    u = False
    for i in range(len(clientbookings)-1):
        i0 = clientbookings[i]
        for k in range(len(clientinfo)-1):
            k0 = clientinfo[k]
            if i0[1] == k0[0]:
                u = True
        for p in range(len(bustrips)-1):
            p0 = bustrips[p]
            if i0[2] == p0[0]:
                u = True
        if u == False:
            mycursor.execute(f"DELETE FROM client_booking WHERE client_booking.id = {i0[0]}")
            mydb.commit()
        u = False

# Funktion som för in en resa i resetabellen. Resan innehåller tre värden. ID på resan som är på autoincrement,
# ID på användaren som bokat resan samt ID på bussen som är bokad
def insertBooking(command, tc):
    sql = "INSERT INTO client_booking (idClient, idBus) VALUES (%s, %s)"
    val = (command[1], command[2])
    mycursor.execute(sql, val)
    mydb.commit()
    clearUnusedBookings()

# Funktion som tar bort resan med angivet ID från resetabellen
def deleteBooking(command, tc):
    mycursor.execute(f"DELETE FROM client_booking WHERE client_booking.id = {command[1]}")
    mydb.commit()
    clearUnusedBookings()

# Funktion som ändrar angivna värden i användartabellen
def editClient(command, tc):
    mycursor.execute("SELECT * FROM client_info")
    myresult = mycursor.fetchall()
    for i in myresult: # Kollar om användarnamn redan är taget. Kan inte heller döpa sig till "admin"
        if i[5] == command[2] or command[2] == "admin":
            print("Username already taken!")
            return
    mycursor.execute(f"UPDATE `client_info` SET `first_name` = '{command[2]}', `last_name` = '{command[3]}', `age` = '{command[4]}', `height` = '{command[5]}', `username` = '{command[6]}', `password` = '{command[7]}' WHERE `client_info`.`id` = {command[1]}")
    mydb.commit()

# Funktion som ändrar angivna värden i busstabellen
def editBus(command, tc):
    mycursor.execute(f"UPDATE `bus_trips` SET `bus_from` = '{command[2]}', `bus_to` = '{command[3]}', `brand` = '{command[4]}', `departure_date` = '{command[5]}' WHERE `bus_trips`.`id` = {command[1]}")
    mydb.commit()
    send_toClient("adminpage", tc)

# Funktion som tar bort angiven buss med angivet ID
def deleteBus(command, tc):
    mycursor.execute(f"DELETE FROM bus_trips WHERE bus_trips.id = {command[1]}")
    mydb.commit()
    print("deleted bus id: " + command[1])
    clearUnusedBookings() # Notera att funktionen även kollar efter eventuella resor som påverkas
    send_toClient("adminpage", tc)

# Funktion som tar bort användare med angiget användarID
def deleteClient(command, tc):
    mycursor.execute(f"DELETE FROM `client_info` WHERE `client_info`.`id` = {command[1]}")
    mydb.commit()
    print("deleted client id: " + command[1])
    clearUnusedBookings()

# Funktion som hämtar och packar information som är relevant för admin
def send_admin_data(command, tc):
    if command[1] == "clients":
        mycursor.execute("SELECT * FROM client_info")
    elif command[1] == "busses":
        mycursor.execute("SELECT * FROM bus_trips")
    elif command[1] == "bookings":
        mycursor.execute("SELECT * FROM client_booking")
    myresult = mycursor.fetchall()
    package = ""
    for i in myresult:
        for k in i:
            package = package + str(k) + " "
        package = package + ", "
    package = command[1] + " " + package
    final_package = package.replace("'", "")
    send_toClient(final_package, tc)

# Funktion som hämtar och packar information för användare
def sendLoginData(u, tc):
    mycursor.execute("SELECT * FROM bus_trips")
    myresult = mycursor.fetchall()
    package = ""
    for i in myresult:
        for k in i:
            package = package + str(k) + " "
        package = package + ", "
    package = "login " + package + "!"
    for i in u:
        package = package + str(i) + " "
    package = package + ",!"
    mycursor.execute("SELECT * FROM client_booking")
    myresult = mycursor.fetchall()
    for i in myresult:
        for k in i:
            package = package + str(k) + " "
        package = package + ", "
    package = package.replace("'", "")
    send_toClient(package, tc)

# Funktion som kollar om användaruppgifterna som angivits under login är korrekta för att kunna logga in
def login(command, tc):
    mycursor.execute("SELECT * FROM client_info")
    myresult = mycursor.fetchall()
    for i in myresult:
        if i[5] == command[1] and i[6] == command[2]: # Kollar om användaren är en vanlig användare
            sendLoginData(i, tc)
            print(command[1] + " Logged In!")
            return
        elif command[1] == "admin" and command[2] == "admin": # Kollar om användaren är admin
            send_toClient("adminpage", tc)
            print(command[1] + " Logged In!")
            return
    send_toClient("logout", tc)

# Funktion som registrerar en användare i användartabellen
def registerClient(command, tc):
    mycursor.execute("SELECT * FROM client_info")
    myresult = mycursor.fetchall()
    for i in myresult: # Kollar om användarnamn redan är taget. Kan inte heller döpa sig till "admin"
        if i[5] == command[1] or command[1] == "admin":
            print("Username already taken!")
            return
    sql = "INSERT INTO client_info (first_name, last_name, age, height, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (command[1], command[2], command[3], command[4], command[5], command[6])
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    send_toClient("logout", tc)

# Funktion som registrerar en ny buss i busstabellen
def registerBus(command, tc):
    sql = "INSERT INTO bus_trips (bus_from, bus_to, brand, departure_date) VALUES (%s, %s, %s, %s)"
    val = (command[1], command[2], command[3], command[4])
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    send_toClient("adminpage", tc)

# All logik sker på serversidan. Klienten skickar enbart kommandon till servern som behandlar dem och skickar
# tillbaka information till klienten. Denna funktion lyssnar efter meddelanden från en klient och beroende
# på vad meddelandet innehåller kommer servern köra olika funktioner.
# If stackandet är inte vackert och jag kunde ha gjort det med dictionaries men detta fungerar.
def listen_input(tc):
    global msg
    try:
        b = conn[tc].recv(1024)
        msg = str(b.decode())
        command = msg.split() 
        if command[0] == "login" and len(command) == 3: login(command, tc)
        if command[0] == "register": send_toClient("register", tc)
        if command[0] == "registerClient" and len(command) == 7: registerClient(command, tc)
        if command[0] == "registerBus" and len(command) == 5: registerBus(command, tc)
        if command[0] == "logout": send_toClient("logout", tc)
        if command[0] == "request" and len(command) == 2: send_admin_data(command, tc)
        if command[0] == "deleteClient" and len(command) == 2: deleteClient(command, tc)
        if command[0] == "deleteBus" and len(command) == 2: deleteBus(command, tc)
        if command[0] == "editClient" and len(command) == 8: editClient(command, tc)
        if command[0] == "editBus" and len(command) == 6: editBus(command, tc)
        if command[0] == "insertBooking" and len(command) == 3: insertBooking(command, tc)
        if command[0] == "deleteBooking" and len(command) == 2: deleteBooking(command, tc)
        if command[0] == "myprofile" and len(command) == 1: send_toClient("myprofile", tc)
    except: # Om en klient tappar kopplingen med servern "krashar" servern och ger meddelandet att den tappade anslutningen
        print(f'{addr[tc]} Disconnected')
        return
    listen_input(tc)

# Funktion som lyssnar efter klienter som vill koppla sig till servern
def listen_client():
    global threadcount
    print("Waiting for new connection...")
    x, y = s.accept()
    conn.append(x)
    addr.append(y)
    clientList.append(Thread(target=listen_input, args=[threadcount])) # Skapar en tråd för varje klient som kopplas
    initThreads(threadcount)                                           # med argumentet "antalet trådar" för att hålla
    threadcount = threadcount + 1                                      # koll på klienterna.
    listen_client()

# Funktion som skickar information till den angivna klienten.
# conn[tc] är anslutningsinformationen som krävs för att skicka informationen till rätt klient
def send_toClient(msg, tc):
    a = str(msg)
    b = a.encode()
    conn[tc].send(b)

# Funktion som kan skicka information till alla klienter (används inte)
def send_allClients(msg):
    msg = str(msg)
    b = msg.encode()
    for i in range(threadcount):
        try:
            conn[i].send(b)
        except:
            pass

client_thread = Thread(target=listen_client)
client_thread.start()

def initThreads(tc):
    clientList[tc].start()
    print("start", tc)