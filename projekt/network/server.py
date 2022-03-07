from socket import *
from threading import Thread
import time

host = ""
port = 5006
conn = []
addr = []
clientList = []
playerList = []
ballList = []
threadcount = 0
activeClients = 0
msg = ""
playerDirection = "neutral"

s = socket()
s.bind((host, port))
s.listen()

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = 0
        self.score = 0
    def updateDirection(self):
        if playerDirection == "updateUp":
            self.dy = -5
        if playerDirection == "updateDown":
            self.dy = 5
        if playerDirection == "neutral":
            self.dy = 0
        #print("Sending update to clients...")
        send_data()
    def update(self):
        self.y += self.dy
        if self.y < 0:
            self.y = 0
        if self.y > 720:
            self.y = 720
    def updateScore(self):
        self.score = self.score + 1
        if self.score >= 5:
            if self.x == 50:
                print("Left Player WON!!!")
            if self.x == 1230:
                print("Right Player WON!!")
            
        #print(f'Updated player from {self.y} with {self.dy} to {self.y + self.dy}')

class Ball():
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
    def update(self):
        if self.x <= 0 or self.x >= 1280:
            self.dx = -self.dx
            send_data()
            #print("Sending update to clients...")
        if self.y <= 0 or self.y >= 720:
            self.dy = -self.dy
            send_data()
            #print("Sending update to clients...")
        self.x += 3*self.dx
        self.y += 3*self.dy
    def reset(self):
        self.x = 640
        self.y = 360
        self.dx = 1
        self.dy = 1

def listen_input(tc):
    global msg, activeClients, playerDirection
    #try:
    b = conn[tc].recv(1024)
    msg = b.decode()
    #print(msg)
    if msg == "updateDown" or msg == "updateUp" or msg == "neutral":
        playerDirection = msg
        playerList[tc].updateDirection()
    if msg == "newPackage":
        #print("Sending package...")
        #send_data()
        package = [str(ballList[0].x), str(ballList[0].y), str(ballList[0].dx), str(ballList[0].dy)]
        for i in range(len(playerList)):
            package.append(playerList[i].y)
        for i in range(len(playerList)):
            package.append(playerList[i].dy)
        print("Sending package size..." + str(len(package)) + f' {str(package)}')
        for i in range(len(playerList)):
            b = str(str(i+4)+str(package[i+4])).encode()
            conn[tc].send(b)
            time.sleep(1/100)
        for i in range(len(playerList)):
            b = str(str(i+6)+str(package[i+6])).encode()
            conn[tc].send(b)
            time.sleep(1/100)
        for i in range(4):
            b = str(str(i)+str(package[i])).encode()
            conn[tc].send(b)
            time.sleep(1/100)
        b = str(str(8) + str(playerList[0].score) + str(playerList[1].score)).encode()
        print(f'Score: {str(8) + str(playerList[0].score) + str(playerList[1].score)}')
        conn[tc].send(b)
    #except:
    #    print(f'{addr[tc]} Disconnected')
    #    activeClients = activeClients - 1
    #    return
    msg = ""
    listen_input(tc)

def listen_client():
    global threadcount, activeClients
    print("Waiting for new connection...")
    x, y = s.accept()
    conn.append(x)
    addr.append(y)
    clientList.append(Thread(target=listen_input, args=[threadcount]))
    print(y)
    initThreads(threadcount)
    threadcount = threadcount + 1
    activeClients = activeClients + 1
    send_data()
    listen_client()

client_thread = Thread(target=listen_client)
client_thread.start()

def initThreads(tc):
    clientList[tc].start()
    print("start", tc)

def send_data():
    global activeClients
    if activeClients != 0:
        for i in range(len(conn)):
            try:
                #time.sleep(1/10)
                a = "packageRecieve"
                b = a.encode()
                conn[i].send(b)
                #print(f'sent: {a}')
            except:
                print(f'Playerlist: {str(len(playerList))}, Conn: {str(len(conn))}. OR DISCONNECT')
                pass

ballList.append(Ball(640, 360, 1, 1))
playerList.append(Player(50, 360))
playerList.append(Player(1230, 360))

while True:    
    time.sleep(1/30)
    try:
        for i in range(len(ballList)):
            ballList[i].update()
    except:
        pass
    for i in range(len(playerList)):
        playerList[i].update()
        try:
            for k in range(len(ballList)):
                if ballList[k].x < 20:
                    playerList[0].updateScore()
                    for i in range(len(ballList)):
                        ballList[i].reset()
                    send_data()
                elif ballList[k].x > 1260:
                    playerList[1].updateScore()
                    for i in range(len(ballList)):
                        ballList[i].reset()
                    send_data()
                if abs(playerList[i].y - ballList[k].y) < 50 and abs(playerList[i].x - ballList[k].x) < 25:
                    ballList[k].dx = -ballList[k].dx
                    print("Collision")
                    send_data()
        except:
            pass
