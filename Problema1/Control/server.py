import socket
import threading
import time

#Servidor
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5000
print ("serve ip:",socket.gethostbyname(socket.gethostname()))

ADDR = (SERVER, PORT) #Endereço
FORMATO = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # STREAM TCP/ DGRAM UDP 
server.bind(ADDR)
server.listen(15)

def start():
    conn, addr = server.accept()
    print("Conectado em :", addr)
    while(True):
        data = conn.recv(1024)
        if not data:
            print("Fechando conexão")
            conn.close()
            break
        conn.sendall(data)

#start();