# -*- coding: utf-8 -*-
import socket,cv2, pickle,struct
import time
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '127.0.1.1'

port = 9999
client_socket.connect((host_ip,port))
BUFFER_SIZE = 128
fhead_size = struct.calcsize('Q')
if client_socket:
    try:
        msg = client_socket.recv(BUFFER_SIZE)
        print(msg)
        client_socket.send(b'phone')
        msg = client_socket.recv(BUFFER_SIZE)
        print(msg)
        client_socket.send(b'open video')
        msg = client_socket.recv(BUFFER_SIZE)
        print(msg)
        client_socket.send(b'pi')
        msg = client_socket.recv(BUFFER_SIZE)
        print(msg)
        client_socket.send(b'get video')
        msg = client_socket.recv(BUFFER_SIZE)
        print(msg)
        client_socket.send(b'pi')
        msg = client_socket.recv(BUFFER_SIZE)
        print(msg)
        if msg==b'send data':
            data = b""
            payload_size = struct.calcsize("Q")
            while len(data) < payload_size:
                packet = client_socket.recv(payload_size)
                if not packet: break
                if packet==b'device is close': break
                data+=packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q",packed_msg_size)[0]
                while len(data) < msg_size:
                    data += client_socket.recv(4)
                frame_data = data[:msg_size]
                data  = data[msg_size:]
                frame = pickle.loads(frame_data)
                cv2.imshow("FROM",frame)
                key = cv2.waitKey(1) & 0xFF
                if key  == ord('q'):
                    break
        client_socket.send(b'close video')
        msg = client_socket.recv(BUFFER_SIZE)
        print(msg)
        client_socket.send(b'pi')
        msg = client_socket.recv(BUFFER_SIZE)
        print(msg)
        client_socket.send(b'close session')
        msg = client_socket.recv(BUFFER_SIZE)
        print(msg)
    except:
        print('FINISHED!')

