from hidrometro import Hidrometro #importa Hidrometro para transforma-lo em um client socket

#Importação de bibliotecas
import socket
import threading
import time

#Criação de constante de localhost como ip de servidor
SERVER = "127.0.0.1"

#Criação de constante de porta para situação client e situação serve
PORT_CLIENT = 8090 #Porta
PORT_SERVER = 8080

#Constante para formato utf-8
FORMATO = 'utf-8' 

#Inicia um hidrometro
hidrometro =  Hidrometro(121212, "Av. José Botelho, 123", False, 3, 5, False)
#--------------------------------------------------------------------------------
#função que envia os dados do hidrometro
def enviaDados():
    #UDP - Envio de dados
    ADDR_C = (SERVER, PORT_CLIENT)    #Endereço
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     #configuração UDP
    while True:
        if(hidrometro.getStatus() == True):
            #Envio
            msg = str(hidrometro.getConsumo())                               #converte para string
            while msg != '\x18':
                udp.sendto(msg.encode('utf-8'),ADDR_C)                  #conversão mensagem 
                time.sleep(6)                                         #pausa para envio de dados
                msg = str(hidrometro.getConsumo())
                if (hidrometro.getStatus() == False):
                    print("Seu hidrômetro foi bloqueado!");
                    break
                if not msg: break
            udp.close()
        else:
            print("Seu hidrômetro encontra-se bloqueado.")
            time.sleep(6) #Tempo para uma nova verificação    
#--------------------------------------------------------------------------------  
 
#função que recebe o bloqueio e desbloqueio do hidrometro  - em 'funcionamento" 
def recebeDados():
    #TCP - Recebimento de dados
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #conexão TCP
    ADDR_S = (SERVER, PORT_SERVER) #Endereço  
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
                    tcp.sendall(b'Recebido!')
                except:
                    print("Mensagem inválida.")
                finally:
                    if not msg: break
                    con.sendall(b'Recebido')
        

                if(msg.startswith("Hidrometro=")): 
                    if(funcionamento == "ligado" or funcionamento == "Ligado" or funcionamento == "funcionando" or funcionamento == "Funcionando"or funcionamento == "ativar" or funcionamento == "Ativar" or funcionamento == "ligar" or funcionamento == "Ligar"):
                        hidrometro.novoStatus(True)

                    elif(funcionamento == "desligado" or funcionamento == "Desligado" or funcionamento == "desativado" or funcionamento == "Desativado" or funcionamento == "desativar" or funcionamento == "Desativar"):
                        hidrometro.novoStatus(False)
                        
                    else:
                        print("Talvez tenha escrito errado, por favor tente novamente");
        except:
            print("Sem conexão")
        finally:	
            print ('Finalizando conexao do cliente',cliente)            #finaliza a conexão com o cliente
            print("O hidrômetro encontra-se no estado atual de: ",hidrometro.getStatus())


#--------------------------------------------------------------------------------
def atualizaConsumo():
    while True:
        if hidrometro.getStatus() == True:
            print("Consumo:", hidrometro.getConsumo())
            print("Vazao:", hidrometro.getVazao())
            consumo = hidrometro.getConsumo()
            vazao = hidrometro.getVazao()
            novoValor = consumo + vazao;
            hidrometro.setConsumo(novoValor);
            time.sleep(6)   

#--------------------------------------------------------------------------------
def iniciar():
    
    thread1 = threading.Thread(target=enviaDados)
    thread2 = threading.Thread(target=recebeDados)
    thread3 = threading.Thread(target=atualizaConsumo)

    thread1.start()                               
    thread2.start()                             
    thread3.start()                           
#--------------------------------------------------------------------------------------
iniciar()