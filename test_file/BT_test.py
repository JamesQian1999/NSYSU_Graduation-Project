from bluetooth import *
import sys
import select

import os
os.system("kill -9 `ps -fA | grep \"[0-9] python3 BT_test.py\" | sed \"s/jamesqi+\\ \\ *\\([0-9][0-9]*\\).*/\\1/g\" | tr '\\n' '\\ ' | sed \"s/" + str(os.getpid()) + "//g\"` 2> /dev/null")

# search for the SampleServer service
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_matches = find_service( uuid = uuid, address = None )

if len(service_matches) == 0:
    print("couldn't find the SampleServer service =(")
    sys.exit(0)

i = 0
while (1):
    try:
        first_match = service_matches[i]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]
        print("connecting to \"%s\" on %s port %d"  % (name, host,port))
        # Create the client socket
        sock=BluetoothSocket( RFCOMM )
        sock.connect((host, port))
        sock.send("SYN")

        ready = select.select([sock], [], [], 1)
        if ready[0]:
            data = sock.recv(1024)
            if (data):
                break
    except:
        i+=1
        try:
            sock.close()
        except:
            pass
        continue


print("connected.  type stuff")
while True:
    data = input()
    if len(data) == 0: break
    sock.send(data)

