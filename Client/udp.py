import socket
import json
import select 
import threading

HOST = '127.0.0.1'
PORT = 9998

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(300)
data={'english':'1'}
data=json.dumps(data).encode('utf-8')
s.sendto(data,(HOST,PORT))
stop=False
def key():
    global stop
    while True:
        try:
            com=input()
        except KeyboardInterrupt:
            stop=True
input_t=threading.Thread(target=key)
input_t.start()
def recv():
    global stop
    global s
    while not stop:
        try:
            message=s.recv(1024).decode()
            print (message[0])
        except KeyboardInterrupt:
            s.close()
            break
client=threading.Thread(target=recv)
client.start()