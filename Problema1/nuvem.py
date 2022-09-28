from http import client
import socket
import threading
import time

FORMATO = 'utf-8' 
SERVER = "127.0.0.1"

#--------------------------------------------------------------------------------
#função que bloqueia ou desbloqueia hidrometro
def funcionamento():
    #TCP - Funcionamento do hidrometro
    PORT = 8080 #Porta
    ADDR_S= (SERVER, PORT) #Endereço  

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #conexão TCP
    tcp.connect(ADDR_S) 
    try:
        mensagem = input('Para sair use CTRL+X e pressione enter\nDigite se deseja Ativar ou Desativar o hidrômetro: ')
        #while True:		
        enviar = ("Hidrometro="+ mensagem)
        tcp.send(enviar.encode(FORMATO))
        time.sleep(10)                                         #pausa para envio de dados
        #mensagem = input('Para sair use CTRL+X e pressione enter\nDigite se deseja Ativar ou Desativar o hidrômetro: ')
        #break
    finally:
        print('Fechando conexão...')
        tcp.close()
#--------------------------------------------------------------------------------  
 
#função que recebe informações do hidrometro
def recebeDados():
    #UDP - Recebimento de dados
    HOST = ''              # Endereco IP do Servidor
    PORT = 8000
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    orig = (HOST, PORT)
    udp.bind(orig)
    try:
        while True:
            msg, cliente = udp.recvfrom(1024) #Recebe em bites a mensagem e o client
            print ("Consumo: ", msg.decode(FORMATO)) #Recebe em bites, então necessário uma conversão
            time.sleep(6) #pausa para receber dados
            if not msg: break
            
    finally:
        
        print ("Fechada a conexão com: ", cliente) 
        udp.close()
#--------------------------------------------------------------------------------
def iniciar():
        #while True:
        #Bloqueio e desbloqueio de hidrometro
        thread1 = threading.Thread(target=funcionamento)
        
        #Recebe dados do hidrometro
        thread2 = threading.Thread(target=recebeDados)
        

        time.sleep(0.5)                                         #pausa para envio de dados
        thread1.start()
        time.sleep(0.5)                                         #pausa para envio de dados
        thread2.start()   

#--------------------------------------------------------------------------------------
iniciar()