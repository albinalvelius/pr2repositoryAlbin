from socket import *
from threading import Thread

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

def listen_input(tc):
    global msg
    try:
        b = conn[tc].recv(1024)
        msg = b.decode()
    except:
        print(f'{addr[tc]} Disconnected')
        return
    send_data(tc)
    print(addr[tc], msg)
    listen_input(tc)

def listen_client():
    global threadcount
    print("Waiting for new connection...")
    x, y = s.accept()
    conn.append(x)
    addr.append(y)
    clientList.append(Thread(target=listen_input, args=[threadcount]))
    print(y)
    initThreads(threadcount)
    threadcount = threadcount + 1
    listen_client()

def send_data(tc):
    global msg
    if msg != "":
        print(msg)
        msg = str(addr[tc][0]) + ": " + msg
        b = msg.encode()
        for i in range(threadcount):
            try:
                if i != tc:
                    conn[i].send(b)
                else:
                    pass
            except:
                pass
        msg = ""

client_thread = Thread(target=listen_client)
client_thread.start()

def initThreads(tc):
    clientList[tc].start()
    print("start", tc)