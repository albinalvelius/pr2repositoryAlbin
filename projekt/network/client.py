from socket import *
from threading import Thread

def connect_to_server():
    s = socket()                # Skapa ett socket-objekt
    # Ange IP-adress manuellt
    host = input("Ange serverns IP-adress:")
    # t.ex. "localhost" om servern körs på samma dator som klienten
    port = 12345                # Servern körs på port 12345
    s.connect((host, port))     # Anslut till servern
    return s
s = connect_to_server()

def reciever():
    b = s.recv(1024)         # Ta emot ett meddelande från klienten
    msg = b.decode("utf-16")    # Gör om från bytekod till vanlig text
    print(msg)
    reciever()

thread1 = Thread(target=reciever)
thread1.start()

while True:
    msg = ""
    msg = input("message: ")
    if msg == "1":
        thread1.join()
        quit()
    b = msg.encode("utf-16")    # Gör om meddelandet till bytekod
    s.send(b)                # Skicka meddelandet till klienten