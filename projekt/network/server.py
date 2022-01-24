from socket import *
from threading import Thread

def start_server():
    s = socket()            # Skapa ett socket-objekt
    host = "localhost"      # som körs på den egna datorn
    port = 12345            # på port 12345.
    s.bind((host, port))    # Konfigurera socket-objektet.
    s.listen()
    return s
s = start_server()

print("Väntar på att en klient ska ansluta till servern...")
conn, addr = s.accept()     # När en klient ansluter
print("En klient anslöt från adressen", addr)

def reciever():
    b = conn.recv(1024)         # Ta emot ett meddelande från klienten
    msg = b.decode("utf-16")    # Gör om från bytekod till vanlig text
    print(msg)
    reciever()

thread1 = Thread(target=reciever)
thread1.start()

while True:
    msg = ""
    msg = input("Massege: ")
    if msg == "1":
        thread1.join()
        quit()
    b = msg.encode("utf-16")    # Gör om meddelandet till bytekod
    conn.send(b)                # Skicka meddelandet till klienten