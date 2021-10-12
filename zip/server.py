# -*- coding: utf-8 -*-
import socket
import threading
import queue
import time
import sys

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 9967
BUFFER_SIZE = 1024
socket_address = ('',port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at",socket_address)
RaspberryPi_device = dict()
RaspberryPi_device_state = dict()
RaspberryPi_device_command = dict()
Phone_device_get_video = dict()

#device_name：pi裝置的名稱; phone_device_name：phone裝置的名稱
def Phone_command_channel(addr,client_socket,device_name,phone_device_name): #指令
    while True:
        client_socket.send(b"get Phone device command")
        command = client_socket.recv(BUFFER_SIZE)   #收到手機端傳來的指令
        RaspberryPi_device_command[device_name] = command
        if command ==b'get video':
            Phone_device_get_video[phone_device_name] = True
        elif command ==b'close video':
            Phone_device_get_video[phone_device_name] = False
        time.sleep(5)
        
def Phone_device_channel(addr,client_socket,device_name,phone_device_name): #串流
    while True:
        #當接收到"get video"時
        while Phone_device_get_video[phone_device_name]==True:
            if RaspberryPi_device_state[device_name]==b'open' and Phone_device_get_video[phone_device_name]:
            #確定pi的鏡頭是open狀態就可以傳影像
            #如果pi關鏡頭，所以手機會break，手機重傳open給server，確定好pi開鏡頭再get
                client_socket.send(b"send data")
                i = 1
                time.sleep(2)
                while True:
                    if Phone_device_get_video[phone_device_name]==False: #phone close
                            break
                    if RaspberryPi_device[device_name].empty(): #pi close
                        time.sleep(0.03)
                        if RaspberryPi_device_state[device_name] == b'close':
                            client_socket.send(b"RaspberryPi device is close.")
                            break
                    else:
                        print("sent",i)
                        sys.stdout.write("\033[F")
                        i+=1
                        msg = RaspberryPi_device[device_name].get()
                        client_socket.send(msg) #傳影片給手機
            elif RaspberryPi_device_state[device_name]==b'close':
                client_socket.send(b"RaspberryPi device is close.")
            else:
                client_socket.send(b"RaspberryPi device state is unknown.")
            time.sleep(3)

def Phone_client(addr,client_socket):
    client_socket.send(b"get Phone device name")
    phone_device_name = client_socket.recv(BUFFER_SIZE) #phone裝置的名稱
    if phone_device_name not in Phone_device_get_video:
        #Phone_device_get_video[phone_device_name] = False'
        Phone_device_get_video[phone_device_name] =True
    client_socket.send(b"get select device name")
    device_name = client_socket.recv(BUFFER_SIZE) #pi裝置的名稱
    if device_name not in RaspberryPi_device:
        client_socket.send(b"No device found!")
        return
    while True:
        client_socket.send(b"Phone command channel or device channel?")
        channel = client_socket.recv(BUFFER_SIZE) #收到要輸入指令還是傳影像 
        if channel==b'command': #指令
            Phone_command_channel(addr,client_socket,device_name,phone_device_name)
            break
        elif channel==b'device': #串流
            Phone_device_channel(addr,client_socket,device_name,phone_device_name)
            break
        else:
            client_socket.send(b"command or device?")
        time.sleep(3)

def RaspberryPi_command_channel(addr,client_socket,device_name): #指令
    while True:
        while RaspberryPi_device_state[device_name]==b'NULL':
            client_socket.send(b"get RaspberryPi device camera status")
            camera_status = client_socket.recv(BUFFER_SIZE) #收到樹莓派的開關鏡頭狀態
            if camera_status==b'open' or camera_status==b'close':
                RaspberryPi_device_state[device_name] = camera_status
        if RaspberryPi_device_command[device_name]!=b'NULL':
            client_socket.send(RaspberryPi_device_command[device_name]) #phone要求pi的鏡頭open or close
            RaspberryPi_device_command[device_name] = b'NULL'
            time.sleep(5)
        time.sleep(3)

def RaspberryPi_device_channel(addr,client_socket,device_name): #串流
    while True:
        while RaspberryPi_device_state[device_name]==b'open': #鏡頭open時
            while True:
                data = client_socket.recv(BUFFER_SIZE) #pi傳影像
                if RaspberryPi_device[device_name].full():
                    RaspberryPi_device[device_name].get()
                RaspberryPi_device[device_name].put(data) #FIFO
                time.sleep(0.01)
                if RaspberryPi_device_command[device_name] == b'close video':
                    RaspberryPi_device_state[device_name] = b'close'
                    time.sleep(3)
                    break
        time.sleep(1)

def RaspberryPi_client(addr,client_socket):
    client_socket.send(b"get RaspberryPi device name")
    device_name = client_socket.recv(BUFFER_SIZE) #pi裝置的名稱
    if device_name not in RaspberryPi_device:
        RaspberryPi_device[device_name] = queue.Queue(maxsize=100)
    if device_name not in RaspberryPi_device_state:
        #RaspberryPi_device_state[device_name] = b'NULL'
        RaspberryPi_device_state[device_name] = b'open'
    if device_name not in RaspberryPi_device_command:
        RaspberryPi_device_command[device_name] = b'NULL'
    while True:
        client_socket.send(b"RaspberryPi command channel or device channel?")
        channel = client_socket.recv(BUFFER_SIZE) #收到要輸入指令還是傳影像
        if channel==b'command': #指令
            RaspberryPi_command_channel(addr,client_socket,device_name)
            break
        elif channel==b'device': #串流
            RaspberryPi_device_channel(addr,client_socket,device_name)
            break
        else:
            client_socket.send(b"command or device?")
        time.sleep(3)

def client(addr,client_socket):
    try:
        print('CLIENT {} CONNECTED!'.format(addr))
        if client_socket:
             client_socket.send(b"Welcome to the server!")
             client_socket.send(b"Device service phone or pi")
             device = client_socket.recv(BUFFER_SIZE) #server收到裝置是pi或phone
             if device == b'phone':
                 Phone_client(addr,client_socket)
             elif device == b'pi':
                 RaspberryPi_client(addr,client_socket)
             client_socket.close()
    except Exception as e:
        print(f"CLINET {addr} DISCONNECTED")
        client_socket.close()

server_socket.makefile('wb')
while True:
    client_socket,addr = server_socket.accept()
    thread = threading.Thread(target=client, args=(addr,client_socket))
    thread.start()
    print("TOTAL CLIENTS ",threading.activeCount() - 1)