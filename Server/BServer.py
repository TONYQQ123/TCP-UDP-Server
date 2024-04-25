import socket
import threading
import json
import os
import select
import time
import datetime
import re
import ast
import socketserver


HOST='127.0.0.1'
PORT=9998
def run_num():
    global count
    global start_server
    while start_server:
        count+=1
        time.sleep(0.01)
def run_eng():
    global en
    global start_server
    while start_server:
        for i in range(25):
            if not start_server:
                return
            en+=1
        en=65
class Handle(socketserver.BaseRequestHandler):

    def handle(self):
        global num_subscribe
        global eng_subscribe
        global start_server
        global count
        global en
        data,s=self.request
        try:
            data=data.decode('utf-8')
            if isinstance(data,str) and data=='end':
                return
            result=json.loads(data)
        except json.JSONDecodeError as e:
            result=None
            print(e)
        except:
            print(self.request[1])
        if result is None:
            return
        if result.get('num')=='1':
            if self.client_address not in num_subscribe:
                num_subscribe.append(self.client_address)
        elif self.client_address in num_subscribe:
            num_subscribe.remove(self.client_address)
        if result.get('english')=='1':
            if self.client_address not in eng_subscribe:
                eng_subscribe.append(self.client_address)
        elif self.client_address in eng_subscribe:
            eng_subscribe.remove(self.client_address)

        while start_server:
            for j in range(25):
                for addr in num_subscribe:
                    response=count
                    response_data=json.dumps(response)
                    s.sendto(bytes(response_data,encoding='utf-8'),addr)
                    print('Sent!')
                    print(response_data)
                    print(len(num_subscribe))
                    time.sleep(1)
                for addr in eng_subscribe:
                    response=chr(en)
                    response_data=json.dumps(response)
                    s.sendto(bytes(response_data,encoding='utf-8'),addr)
                    print('Sent!')
                    time.sleep(1)

def run_udp():
    start_server=True
    def keyboard_input():
        global start_server
        while True:
            try:
                command = input("Enter 'ctrl+c' to stop the server: ")
                if command.strip().lower() == 'ctrl+c':
                    start_server = False
                    print('Stopping server...')
                    break
            except KeyboardInterrupt:
                start_server = False
                break
            except:
                start_server = False
                break
    input_thread = threading.Thread(target=keyboard_input)
    input_thread.start()
    with socketserver.ThreadingUDPServer((HOST,PORT),Handle) as server:
        print('start')
        server.serve_forever()

if __name__=="__main__":
    start_server=True
    count=0
    en=65
    num_subscribe=[]
    eng_subscribe=[]
    num_t=threading.Thread(target=run_num)
    en_t=threading.Thread(target=run_eng)
    num_t.start()
    en_t.start()
    run_udp()
