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

def insertBooking(command, tc):
    sql = "INSERT INTO client_booking (idClient, idBus) VALUES (%s, %s)"
    val = (command[1], command[2])
    mycursor.execute(sql, val)
    mydb.commit()
    send_toClient("adminpage", tc)

def deleteBooking(command, tc):
    mycursor.execute(f"DELETE FROM client_booking WHERE client_booking.id = {command[1]}")
    mydb.commit()
    send_toClient("adminpage", tc)

def editClient(command, tc):
    mycursor.execute(f"UPDATE `client_info` SET `first_name` = '{command[2]}', `last_name` = '{command[3]}', `age` = '{command[4]}', `height` = '{command[5]}', `username` = '{command[6]}', `password` = '{command[7]}' WHERE `client_info`.`id` = {command[1]}")
    mydb.commit()
    #send_toClient("adminpage", tc)

def editBus(command, tc):
    mycursor.execute(f"UPDATE `bus_trips` SET `bus_from` = '{command[2]}', `bus_to` = '{command[3]}', `brand` = '{command[4]}', `departure_date` = '{command[5]}' WHERE `bus_trips`.`id` = {command[1]}")
    mydb.commit()
    send_toClient("adminpage", tc)

def deleteBus(command, tc):
    mycursor.execute(f"DELETE FROM bus_trips WHERE bus_trips.id = {command[1]}")
    mydb.commit()
    print("deleted bus id: " + command[1])
    send_toClient("adminpage", tc)

def deleteClient(command, tc):
    mycursor.execute(f"DELETE FROM `client_info` WHERE `client_info`.`id` = {command[1]}")
    mydb.commit()
    print("deleted client id: " + command[1])
    #send_toClient("adminpage", tc)

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
    print("Final package: " + final_package)
    send_toClient(final_package, tc)

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
    print("package: " + package)
    send_toClient(package, tc)

def login(command, tc):
    mycursor.execute("SELECT * FROM client_info")
    myresult = mycursor.fetchall()
    for i in myresult:
        if i[5] == command[1] and i[6] == command[2]:
            sendLoginData(i, tc)
            print(command[1] + " Logged In!")
            return
        elif command[1] == "admin" and command[2] == "admin":
            send_toClient("adminpage", tc)
            print(command[1] + " Logged In!")
            return
    send_toClient("logout", tc)

def registerClient(command, tc):
    mycursor.execute("SELECT * FROM client_info")
    myresult = mycursor.fetchall()
    for i in myresult:
        if i[5] == command[1] or command[1] == "admin":
            print("Username already taken!")
            return
    sql = "INSERT INTO client_info (first_name, last_name, age, height, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (command[1], command[2], command[3], command[4], command[5], command[6])
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    send_toClient("logout", tc)

def registerBus(command, tc):
    sql = "INSERT INTO bus_trips (bus_from, bus_to, brand, departure_date) VALUES (%s, %s, %s, %s)"
    val = (command[1], command[2], command[3], command[4])
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    send_toClient("adminpage", tc)

def listen_input(tc):
    global msg
    #try:
    b = conn[tc].recv(1024)
    msg = str(b.decode())
    print("msg: " + msg)
    command = msg.split()
    print("command: " + str(command))

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
    """except:
        print(f'{addr[tc]} Disconnected')
        return"""
    #print(addr[tc], msg)
    listen_input(tc)

def listen_client():
    global threadcount
    print("Waiting for new connection...")
    x, y = s.accept()
    conn.append(x)
    addr.append(y)
    clientList.append(Thread(target=listen_input, args=[threadcount]))
    initThreads(threadcount)
    threadcount = threadcount + 1
    listen_client()

def send_toClient(msg, tc):
    a = str(msg)
    b = a.encode()
    conn[tc].send(b)

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