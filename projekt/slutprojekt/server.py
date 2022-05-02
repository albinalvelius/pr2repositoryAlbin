from socket import *
from threading import Thread
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

def login(command, tc):
    mycursor.execute("SELECT * FROM client_info")
    myresult = mycursor.fetchall()
    for i in myresult:
        if i[5] == command[1] and i[6] == command[2]:
            print(command[1] + " Logged In!")
    send_toClient("mainmenu", tc)

def registerClient(command, tc):
    if len(command) == 6:
        sql = "INSERT INTO client_info (first_name, last_name, age, height, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (command[1], command[2], command[3], command[4], command[5], command[6])
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    send_toClient("login", tc)

def listen_input(tc):
    global msg
    #try:
    b = conn[tc].recv(1024)
    msg = str(b.decode())
    print("msg: " + msg)
    command = msg.split()
    print("command: " + str(command))
    if command[0] == "login":
        login(command, tc)
    if command[0] == "register":
        send_toClient("register", tc)
    if command[0] == "registerClient":
        registerClient(command, tc)
    if command[0] == "logout":
        send_toClient("logout", tc)
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