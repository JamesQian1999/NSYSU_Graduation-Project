import bluetooth  # sudo apt-get install python3-bluez
import os
import sys
import select

os.system("clear")

rev_buff = 2048
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

print("\033[33mConnecting...\033[m")
sys.stdout.write("\033[F") 

service_matches = bluetooth.find_service( uuid = "00001101-0000-1000-8000-00805F9B34FB" , address = None )
if len(service_matches) == 0:
    print("couldn't find the SampleServer service =(")
    sys.exit(0)
        
i = 0
while (1):
    try:
        global port, name, host
        first_match = service_matches[i]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]
        print("Try to connect \"%s\" on %s port %d"  % (name, host,port))
    
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


print("\n\033[34mConnect to ", name,"(",host,"port:",port,") successful.\033[m",sep="")

print("\n\033[32mSent:\033[m\t\tHello")
sock.send("Hello")

data = sock.recv(rev_buff)
print("\n\033[32mReceived:\033[m\t", data.decode(), sep="")


sock.close()
