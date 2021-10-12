# -*- coding: utf-8 -*-
import socket,cv2, pickle,struct,time
cap = cv2.VideoCapture('2.mp4')

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '127.0.1.1' 
BUFFER_SIZE = 128
port = 9999
client_socket.connect((host_ip,port))
if client_socket: 
    msg = client_socket.recv(BUFFER_SIZE)
    print(msg)
    client_socket.send(b'pi')
    msg = client_socket.recv(BUFFER_SIZE)
    print(msg)
    client_socket.send(b'pi')
    msg = client_socket.recv(BUFFER_SIZE)
    print(msg)
    if cap.isOpened():
        client_socket.send(b'open')
    else:
        client_socket.send(b'close')
    while (cap.isOpened()):
        try:
            img, frame = cap.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            client_socket.sendall(message)
            #time.sleep(0.1)

        except:
            print('FINISHED!')
            break
    client_socket.send(b'close session')
    msg = client_socket.recv(BUFFER_SIZE)
    print(msg)
        