import socket
import time
import subprocess
import threading
import os

os.system("kill -9 `ps -fA | grep \"[0-9] python3 doc_server.py\" | sed \"s/[a-zA-Z+]*\\ \\ *\\([0-9][0-9]*\\).*/\\1/g\" | tr '\\n' '\\ ' | sed \"s/" + str(os.getpid()) + "//g\"` 2> /dev/null")


data = []

def receive(connection):
    print("hello")
    global data
    c = 0
    while True:
        time.sleep(0.001)
        data.append(connection.read(1024))
        #print("Received",c)
        #c+=1

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    # Run a viewer with an appropriate command line. Uncomment the mplayer
    # version if you would prefer to use mplayer instead of VLC
    cmdline = ['vlc', '--demux', 'h264', '-']
    #cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
    t = threading.Thread(target=receive, args=(connection,))
    t.start()
    c = 0
    time.sleep(5)
    while True:
        #c+=1
        # Repeatedly read 1k of data from the connection and write it to
        # the media player's stdin
        count = 0
        while not data:
            #break
            #print(count)
            #count +=1
            continue

        #print(c,"list size:",len(data))
        #c+=1
        player.stdin.write(data.pop(0))
        #if(len(data)<5):
         #   time.sleep(0.5)
    t.join()
except:
    #connection.close()
    server_socket.close()
    player.terminate()