import socket
import threading
import json
import os
import select
import time
import datetime
import re
import ast


HOST='127.0.0.1'
PORT=9999
database='database.txt'
lock=threading.Lock()

def check_eq(equation):
    pattern = r'^\s*[a-zA-Z0-9()]+(\s*[+\-*/]\s*[a-zA-Z0-9()]+)*\s*$'
    if re.match(pattern, equation):
        print('Valid Equation')
        return True
    print('Invalid Equation')
    return False
def Caculate(equation):
    result={}
    if not check_eq(equation):
        result['error']='Invalid Equation'
        result['status']=False
    else:
        try:
            parse_eq=ast.parse(equation,mode='eval')
            ans=eval(compile(parse_eq,'<string>','eval'))
            result['success']=ans
            result['status']=True
        except:
            result['error']='equation error'
            result['status']=False
    return result


def handle_request(client_s):
    global start_server
    client_s.settimeout(1000)
    while start_server:
        try:
            ready=select.select([client_s],[],[],1)
            if ready:
                data=client_s.recv(1024)

                try:
                    data=data.decode('utf-8')
                    if isinstance(data,str) and data=='end':
                        break
                    result=json.loads(data)
                except json.JSONDecodeError as e:
                    result=None
                    print(e)
                if result is None:
                    break
                if result.get('mode')=='simple':
                    response=Caculate(result.get('eq'))
                
                response_data=json.dumps(response)
                client_s.sendall(bytes(response_data,encoding='utf-8'))
        except socket.timeout:
            print('Client Timeout')
            break
        except KeyboardInterrupt:
            print('Stop')
            break

    client_s.close()
    print('Client disconnect')


def run_server():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen(10)
    print('Server running')
    global start_server
    start_server=True
    while start_server:
        def keyboard_input():
            global start_server
            while True:
                command = input("Enter 'ctrl+c' to stop the server: ")
                if command.strip().lower() == 'ctrl+c':
                    start_server = False
                    print('Stopping server...')
                    break

        input_thread = threading.Thread(target=keyboard_input)
        input_thread.start()
        try:
            ready=select.select([s],[],[],1)
            if ready:
                client_s,client_addr=s.accept()

                t=threading.Thread(target=handle_request,args=(client_s,))
                t.start()
        except KeyboardInterrupt:
            print('Stop')
            start_server=False

if __name__=="__main__":
    run_server()
    start_server=True
