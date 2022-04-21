from socket import *
from threading import Thread
import tkinter as tk

msglist = []

x = tk.Tk()
c = tk.Canvas(x, bg="white", height=400, width=200)
c.pack()

def online_chat(msg):
    c.delete("all")
    msglist.append(msg)
    for i in range(len(msglist)):
        c.create_text(100, 350 - 20*i, text=msglist[-i])
    inputtext = tk.Text(c, height=1, width=17)
    inputtext.place(anchor=tk.NW, x=5, y=380)
    def sendmsg():
        msg = inputtext.get(1.0, "end-1c")
        b = msg.encode()
        s.send(b)
    a = tk.Button(c, text="SEND!", command=sendmsg)
    a.place(anchor=tk.CENTER, x=180, y=390)


def start_client():
    print("Attempting to connect to server...")
    global s
    s = socket()
    s.connect(("localhost", 12345)) #"217.208.70.106"
    def reciever():
        b = s.recv(1024)
        msg = b.decode()
        online_chat(msg)
        reciever()
    rec_thread = Thread(target=reciever)
    rec_thread.start()
    online_chat("")
    print("Connection successful")

start_client()
x.mainloop()