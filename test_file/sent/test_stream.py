import socket
#import picamera
import time
import io
import sys
import struct

HOST = ""
PORT = 63272
TEST = 1
buff= 2048
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST,PORT))
server_socket.listen(1)
print("(%s:%s) Listening..."%("192.168.0.111",PORT))
connection, addr = server_socket.accept()


connection = connection.makefile('wb')
#with picamera.PiCamera() as camera:
if True:
    #camera.resolution = (640, 480)
    #camera.rotation = 180
    print("\033[33mStarting Camera...\033[m")
    time.sleep(2)
    
    try:
        while True:
            stream = io.BytesIO()
            stream.flush()

            if TEST:
                fd = open("in.jpg","rb")
                stream.write(fd.read())

            #camera.capture(stream, 'jpeg', use_video_port=True)
            size = stream.tell()
            print("size: %f KB"%(size/1024))
            print("size: %d bytes"%(size))
            #size = bytes(str(size),"utf-8")
            
            connection.write(struct.pack('!i', size))
            connection.flush()

            stream.seek(0)
            connection.write(stream.read())
                
            break

            stream.seek(0)
            stream.truncate()
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")
    except Exception as e:
        print(e)

connection.close()
server_socket.close()
print("Finish streaming!")


'''
with picamera.PiCamera() as camera:
#if True:
    camera.resolution = (640, 480)
    camera.rotation = 180
    print("\033[33mStarting Camera...\033[m")
    time.sleep(2)
    
    try:
        while True:
            stream = io.BytesIO()
            stream.flush()

            if TEST:
                fd = open("in.jpg","rb")
                stream.write(fd.read())

            camera.capture(stream, 'jpeg', use_video_port=True)
            size = stream.tell()
            print("size: %f KB"%(size/1024))
            print("size: %d bytes"%(size))
            size = bytes(str(size),"utf-8")
            print("len =",size,"len(size) =",len(size))
            connection.send(size)
            stream.seek(0,0)
            count = 1
            while True:
                time.sleep(0.005)
                partition = stream.read(buff)
                print(count,". ",len(partition),sep="")
                connection.send(partition)
                count+=1
                if(len(partition) != buff):
                    break
                
            break

            stream.seek(0)
            stream.truncate()
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")
    except Exception as e:
        print(e)

connection.close()
server_socket.close()
print("Finish streaming!")
'''




