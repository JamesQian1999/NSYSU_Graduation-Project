import io
import socket
import struct
import time
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1",10001))

connection = client_socket.makefile('wb')
count = 1
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        print("starting Camera...........")
        time.sleep(2)
        stream = io.BytesIO()
        while True:
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            stream.seek(0)
            stream.truncate()
finally:
    connection.close()
    client_socket.close()
