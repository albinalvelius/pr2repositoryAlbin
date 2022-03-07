from socket import *
from threading import Thread

def start_client():
    print("Attempting to connect to server...")
    global s
    s = socket()
    s.connect((str(input("IP: ")), 12345)) #"217.208.70.106"
    def reciever():
        b = s.recv(1024)
        msg = b.decode()
        print(msg)
        reciever()
    rec_thread = Thread(target=reciever)
    rec_thread.start()
    print("Connection successful")

start_client()

while True:
    msg = input().encode()
    s.send(msg)