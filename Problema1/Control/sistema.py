import socket
import threading
import time

from Model.administrador import Administrador
from Model.hidrometro import Hidrometro
from Model.usuario import Usuario

PORT = 5000 #Porta
FORMATO = 'utf-8' 
SERVER = socket.gethostbyname(socket.gethostname()) #Função que pega o ipv4 atual
ADDR = (SERVER, PORT) #Endereço

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

hidrometro1 = Hidrometro("1100",True,"Avenida Coronel Plinio da Silva Gomes","4 m³/s");

#--------------------------------------------------------------------------------
    #função que envia os dados do hidrometro
def enviaDados(self):
    if(self.funcionamento == True):
        udp = socket.socket(socket.AF_INET, socket.DGRAM)     #configuração UDP
        dest = (SERVER, PORT)                                         #destino de envio
        udp.connect(dest)                                           #conectando

        msg = str(self.consumo)                               #converte para string
        while msg != '\x18':
            udp.send(msg.encode('utf-8'))                           #conversão mensagem 
            msg = str(self.consumo)
            time.sleep(2)                                           #pausa para envio de dados
        
        print ('mensagem enviada' )                                 #finalização da conexão
        udp.close()
    else:
        print("Seu hidrômetro encontra-se bloqueado.")
#--------------------------------------------------------------------------------   
    #função que recebe o bloqueio e desbloqueio do hidrometro  - em 'funcionamento" 
def recebeDados(self):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #conexão TCP
    orig = (SERVER, PORT)
    tcp.bind(orig)
    tcp.listen(1)

    con, cliente = tcp.accept()
    print('Conectado por: ',cliente) 

    msg = con.recv(1024)
    print (cliente, msg)
    if(msg == "ligado" or msg == "Ligado" or msg == "funcionando" or msg == "Funcionando" or msg == "ligar" or msg == "Ligar"):
        self.funcionamento = True
    elif(msg == "desligado" or msg == "Desligado" or msg == "desativado" or msg == "Desativado" or msg == "desativar" or msg == "Desativar"):
        self.funcionamento = False
    else:
        print("Talvez tenha escrito errado, por favor tente novamante");

    print("O hidrometro encontra-se no estado:",self.funcionamento)
    
    print ('Finalizando conexao do cliente',cliente)            #finaliza a conexão com o cliente
    con.close()
#--------------------------------------------------------------------------------


def iniciar():
    print('iniciando thread 1')
    thread1 = threading.Thread()
    print('iniciando thread 2')
    thread2 = threading.Thread()
    thread1.start()
    thread2.start()

iniciar()