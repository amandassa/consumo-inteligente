from hidrometro import Hidrometro #importa Hidrometro para transforma-lo em um client socket
#Importação de bibliotecas
import socket
import threading
import time

#Criação de constante de localhost como ip de servidor
SERVER = "127.0.0.1"

#Criação de constante de porta para situação client e situação serve
PORT_Client = 8000 #Porta
PORT_Server = 8080

#Constante para formato utf-8
FORMATO = 'utf-8' 

#--------------------------------------------------------------------------------
#função que envia os dados do hidrometro
def enviaDados(consumo, funcionamento):
    #UDP - Envio de dados
    ADDR_C = (SERVER, PORT_Client)    #Endereço
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     #configuração UDP

    if(funcionamento == True):
        #Envio
        msg = str(consumo)                               #converte para string
        while msg != '\x18':
            udp.sendto(msg.encode('utf-8'),ADDR_C)                  #conversão mensagem 
            time.sleep(10)                                         #pausa para envio de dados
            consumo = consumo+1;
            msg = str(consumo)
            if funcionamento == False: break
            if not msg: break
        udp.close()
    else:
        print("Seu hidrômetro encontra-se bloqueado.")
#--------------------------------------------------------------------------------  
 
#função que recebe o bloqueio e desbloqueio do hidrometro  - em 'funcionamento" 
def recebeDados(hidrometro):
    #TCP - Recebimento de dados
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #conexão TCP
    ADDR_S = (SERVER, PORT_Server) #Endereço  
    tcp.bind(ADDR_S)
    tcp.listen(10)

    while(True):
        print("Esperando por conexões:")
        con, cliente = tcp.accept()
        print("Conctado por: ", cliente)
        try:
            while True:			
                msg = con.recv(1024).decode(FORMATO)
                try:
                    mensagem_separada = msg.split("=")
                    funcionamento = mensagem_separada[1]
                    print("Funcionamento: ",funcionamento)
                    print("Mensagem: ",msg)
                except:
                    print("Mensagem inválida.")
                finally:
                    if not msg: break
        

                if(msg.startswith("Hidrometro=")): 
                    if(funcionamento == "ligado" or funcionamento == "Ligado" or funcionamento == "funcionando" or funcionamento == "Funcionando"or funcionamento == "ativar" or funcionamento == "Ativar" or funcionamento == "ligar" or funcionamento == "Ligar"):
                        hidrometro = True
                        print("O hidrômetro encontra-se no estado: ",hidrometro)

                    elif(funcionamento == "desligado" or funcionamento == "Desligado" or funcionamento == "desativado" or funcionamento == "Desativado" or funcionamento == "desativar" or funcionamento == "Desativar"):
                        hidrometro = False
                        print("O hidrômetro encontra-se no estado: ",hidrometro)
                        
                    else:
                        print("Talvez tenha escrito errado, por favor tente novamente");
        finally:	
            print ('Finalizando conexao do cliente',cliente)            #finaliza a conexão com o cliente
            print("O hidrômetro encontra-se no estado atual de: ",hidrometro)

#--------------------------------------------------------------------------------
def iniciar():
    hidrometro =  Hidrometro(121212, "Av. José Botelho, 123", False, 3, 5, False)
    thread1 = threading.Thread( target=enviaDados, args=(hidrometro.getConsumo(),hidrometro.getStatus()))
    thread2 = threading.Thread( target=recebeDados, args=(hidrometro.getStatus(),))
    #thread3 = threading.Thread( target=recebeDados, args=(hidrometro.getStatus(),))
    thread1.start()                               
    thread2.start()                         
    #thread3.start()
#--------------------------------------------------------------------------------------
iniciar()