#!/usr/bin/python
import threading
import thread
import socket
import time



def sender(N, id, UDP_IP , UDP_IP2 , UDP_PORT ):
    UDP_PORTr = UDP_PORT*10 + 5
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((UDP_IP2, UDP_PORTr))
    sock.settimeout(10)
    sock.sendto("ready", (UDP_IP, UDP_PORT)) #take ready to start
    sock.sendto(str(N) , (UDP_IP, UDP_PORT)) #how many messages
    for data in range(N):
        try:
            data, addr = sock.recvfrom(1024)
            sock.sendto( data , (UDP_IP, UDP_PORT)) #sending back to reciever
        except socket.timeout:
            break





def reciever(UDP_IP , UDP_IP2 , UDP_PORT , UDP_PORT2):
    totalTime = 0
    UDP_PORTr = UDP_PORT*10 + 5
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(10)
    data, addr = sock.recvfrom(1024)
    N = 0
    NN=0
    if data == "ready":
        data, addr = sock.recvfrom(1024)
        N = int(data)
        for i in range(N):
            try:
                data =  str(float(round(time.time() * 1000)))
                sock.sendto( data , (UDP_IP2, UDP_PORTr))
                data, addr = sock.recvfrom(1024)
                data = float(round(time.time() * 1000)) - float(data) #calculate time difference to find rtt

                if data  > 0:
                    totalTime += data
                    NN=NN+1
            except socket.timeout:
                break
        if NN:
            totalTime =  totalTime/(NN)  #taking avarage of rtts
        print totalTime
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(str(totalTime), ("10.10.5.2", UDP_PORT2))
    sock.sendto(str(totalTime), ("10.10.5.2", UDP_PORT2)) #send rtt to d




UDP_PORT = 5005
UDP_PORT1 = 5001
UDP_PORTs2 = 5002
UDP_PORT3 = 5003
UDP_PORT12 = 50021



UDP_IP = [  [0          ,"10.10.1.2","10.10.2.1" ,"10.10.3.2" ,0],
            ["10.10.1.1",0          ,"10.10.8.2" ,0           ,"10.10.4.2"],
            ["10.10.2.2","10.10.8.1",0           ,"10.10.6.2" ,"10.10.5.2"],
            ["10.10.3.1",0          ,"10.10.6.1" ,0           ,"10.10.7.1"],
            [0          ,"10.10.4.1","10.10.5.1" ,"10.10.7.2" ,0]
         ]



#reciving rtt from s
s2 = threading.Thread(target = reciever, args=(UDP_IP[0][2], UDP_IP[2][0] ,UDP_PORT,UDP_PORTs2,))
s2.start()

#reciving rtt from r1
r12 = threading.Thread(target = reciever, args=(UDP_IP[1][2],UDP_IP[2][1] , UDP_PORT,UDP_PORT12,))
r12.start()
#sending rtt to d
r2d = threading.Thread(target = sender, args=(100 , "r2", UDP_IP[2][4],UDP_IP[4][2]  , UDP_PORT,))
r2d.start()
#sending rtt to r3
r23 = threading.Thread(target = sender, args=(100 , "r2", UDP_IP[2][3] , UDP_IP[3][2] , UDP_PORT,))
r23.start()


s2.join()
r12.join()
r2d.join()
r23.join()



sockd = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sockd.bind(("10.10.5.1", 10002))
data, addr = sockd.recvfrom(1024) #getting routelist
print data
f= open("routelist.txt","w+")
f.write(data)
f.close()