import socket
import threading
import time
import http.server 

FORMATO = 'utf-8' 
SERVER = "127.0.0.1"
PROTOCOL= "HTTP/1.0"
#--------------------------------------------------------------------------------
#função que bloqueia ou desbloqueia hidrometro
def funcionamento():
    #TCP - Funcionamento do hidrometro
    PORT = 8080 #Porta
    ADDR_S= (SERVER, PORT) #Endereço  
    while True:
        try:   
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #conexão TCP
            tcp.connect(ADDR_S) 
            try:
                mensagem = input('Para sair use CTRL+X e pressione enter\nDigite se deseja Ativar ou Desativar o hidrômetro: ')
                        
                enviar = ("Hidrometro="+ mensagem)
                tcp.send(enviar.encode(FORMATO))
                time.sleep(10)                                         #pausa para envio de dados
                respostaSistema = tcp.recv(1024)
                respostaSistema = respostaSistema.decode(FORMATO)
                print("Recebido do servidor: ",respostaSistema)
            finally:
                print('Fechando conexão...')
                tcp.close()
        except:
            print("Servidor TCP desligado, tente novamente mais tarde.")
            time.sleep(10)

#--------------------------------------------------------------------------------  
 
#função que recebe informações do hidrometro
def recebeDados():
    #UDP - Recebimento de dados
    HOST = ''              # Endereco IP do Servidor
    PORT = 8090
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
 
#função que recebe informações do hidrometro
def servidor():
    SERVERCLASS  = http.server.HTTPServer 
    HANDLERCLASS = http.server.SimpleHTTPRequestHandler 
    situacoes = http.server.BaseHTTPRequestHandler
    port = 8000
    server_address = ('127.0.0.1', port) 
    HANDLERCLASS.protocol_version = PROTOCOL 
    http_server = SERVERCLASS(server_address, HANDLERCLASS) 
    sa = server_address
    print("Servidor on: ", sa[0], "porta", sa[1], "...") 
    http_server.serve_forever()
#--------------------------------------------------------------------------------
def iniciar():
    #Bloqueio e desbloqueio de hidrometro
    thread1 = threading.Thread(target=funcionamento)
    
    #Recebe dados do hidrometro
    thread2 = threading.Thread(target=recebeDados)

    #Servidor HTTP
    thread3 = threading.Thread(target=servidor)

    thread1.start()
    time.sleep(0.5)                                         #pausa para envio de dados

    thread2.start()
    time.sleep(0.5)                                         #pausa para envio de dados

    thread3.start()   
#--------------------------------------------------------------------------------------
iniciar()