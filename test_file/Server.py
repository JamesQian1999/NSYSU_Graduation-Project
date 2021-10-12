import bluetooth  # sudo apt-get install python3-bluez
import os
from Crypto.PublicKey import RSA  # pip3 install -U PyCryptodome
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import base64
import time
import io
import socket
import struct
from PIL import Image
import cv2
import numpy
import sys
import select

# os.system("clear")

# rev_buff = 2048
# sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# creat 1024bits RSA Key
random_generator = Random.new().read
key = RSA.generate(1024, random_generator)

# RSA Private Key
privateKey = key.export_key()
with open("private.pem", "wb") as f:
    f.write(privateKey)

# RSA Public Key
publicKey = key.publickey().export_key()
with open("public.pem", "wb") as f:
    f.write(publicKey)



# print("\033[33mConnecting...\033[m")
# sys.stdout.write("\033[F") 
        

# service_matches = bluetooth.find_service( uuid = "00001101-0000-1000-8000-00805F9B34FB" , address = None )
# if len(service_matches) == 0:
#     print("couldn't find the SampleServer service =(")
#     sys.exit(0)
        
# i = 0
# while (1):
#     try:
#         global port, name, host
#         first_match = service_matches[i]
#         port = first_match["port"]
#         name = first_match["name"]
#         host = first_match["host"]
#         print("Try to connect \"%s\" on %s port %d"  % (name, host,port))
    
#         sock.connect((host, port))
#         sock.send("SYN")

#         ready = select.select([sock], [], [], 1)
#         if ready[0]:
#             data = sock.recv(1024)
#             if (data):
#                 break

#     except:
#         i+=1

#         try:
#             sock.close()
#         except:
#             pass

#         continue


# print("\n\033[34mConnect to ", name,"(",host,"port:",port,") successful.\033[m",sep="")

# print("\n\033[32mSent:\033[m\t\tSYN")
# sock.send("SYN")

# data = sock.recv(rev_buff)
# print("\n\033[32mReceived:\033[m\t", data.decode(), sep="")


# Read Private Key
encodedKey = open("private.pem", "rb")
pre_key = RSA.import_key(encodedKey.read())

# print("\n\033[32mSent Phone Public Key:\033[m")
# data = pre_key.publickey().export_key()
# print(data.decode('utf-8'))
# sock.send(data)

# data = sock.recv(rev_buff)
# print("\n\033[32mReceived Raspberry Pi Public Key:\033[m")
# print(data.decode('utf-8'))

# pi_public = "pi_public.pem"
# fd = open(pi_public, "wb")
# fd.write(data)

# Sent msg with RSA 
msg = "This is secret."
fd = open('pi_public.pem')
pi_key = fd.read()
pi_key = RSA.importKey(str(pi_key))
cipher = PKCS1_cipher.new(pi_key)
rsa_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
print("\n\033[32mSent Data:\033[m")
print("Before encrypt: ",msg)
print("After encrypt: ",rsa_text.decode('utf-8'))
sock.send(rsa_text)

# # Receive msg with RSA 
# data = sock.recv(rev_buff)
# print("\n\033[32mReceived Data:\033[m")
# print("Before decrypt:",data.decode('utf-8'))
# cipher = PKCS1_cipher.new(pre_key)
# back_text = cipher.decrypt(base64.b64decode(data), 0)
# print("After decrypt:",back_text.decode('utf-8'))

# sock.close()


# #sys.exit(0)
# HOST = "192.168.0.179"
# PORT = 9967
# buff = 2048
# server_socket = socket.socket()
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((HOST,PORT))
# # server_socket.bind(("",10001))
# # server_socket.listen(0)
# # print("\nListening...")
# # connection = server_socket.accept()[0].makefile('rb')
# rcv = client_socket.recv(buff)
# print(rcv.decode())
# rcv = client_socket.recv(buff)
# print(rcv.decode(),": phone")
# client_socket.send(b'phone')

# rcv = client_socket.recv(buff)
# print(rcv.decode(),": Android phone")
# client_socket.send(b'Android phone')

# rcv = client_socket.recv(buff)
# print(rcv.decode(),": Raspberry Pi 4")
# client_socket.send(b'Raspberry Pi 4')

# rcv = client_socket.recv(buff)
# print(rcv.decode(),": device")
# client_socket.send(b'device')

# rcv = client_socket.recv(buff)
# print(rcv.decode())


# connection = client_socket.makefile('rb')
# time.sleep(1)
# try:
#     img = None
#     i=1
#     while True:
#         print("receive",i)
#         i+=1
#         sys.stdout.write("\033[F")
#         image_len = struct.unpack('!i', connection.read(struct.calcsize('!i')))[0]
#         if not image_len:
#             break
#         image_stream = io.BytesIO()
#         image_stream.write(connection.read(image_len))
#         image_stream.seek(0)
#         cv2.imshow('Video',cv2.cvtColor(numpy.array(Image.open(image_stream)), cv2.COLOR_RGB2BGR))
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
#     cv2.destroyAllWindows()
# finally:
#     connection.close()
#     server_socket.close()