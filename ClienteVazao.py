import socket
import time
import os

class ClienteVazao:
    HOST = 'localhost'
    PORT = 7001

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 7000))
        path = 'sentArchive.txt'
        arq = open(path, 'rb') 
        l = arq.read(1024)

        initial_time = time.time()
        
        while(l):
            self.sock.send(l)
            l = arq.read(1024)

        final_time = time.time()
        elapsed_time = final_time - initial_time

        print("A vazão obtida foi de: " + 
              str(round(os.path.getsize(path)/(elapsed_time*1024*1024),2)) 
              + " Mbps")

        arq.close()
        self.sock.close()

ClienteVazao()
