import json
import random
from paho.mqtt import client as mqtt_client

'''o banco de dados segue o padrão:
nevoaDB = {
    idNevoa: [{maiores consumos da nevoa}]
}
'''
# banco de dados com os dados das nevoas
nevoaDB = {}
# conexáo mqtt com todas as nevoas
nevoas = {
    'broker': 'localhost',      # mudar para maquina central do larsid
    'port': 1883,
    'topicPub': "nuvem",     
    'topicSub': "nuvem/#"
}

#       funções de conectividade com a névoa --------------------------------------
def connect_mqtt(broker, port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(f'{random.randint(0, 100)}')
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    
    return client

def subscribe (client, topico):
    def on_message(client, userdata, msg):
        print(f'{msg.payload.decode()}')
    
    client.subscribe(topico)
    client.on_message = on_message

def publish(client, topic, msg):
    client.publish(topic, msg)

def subMaioresConsumos (client):
    def on_message(client, userdata, msg):
        print(f'{msg.payload.decode()}')
        idNevoa = msg.topic.split('/')[-1]
        nevoaData = json.loads(msg.payload.decode())
        nevoaDB[idNevoa] = nevoaData    #   uma lista com os maiores consumos
    
    client.subscribe(f'{nevoas["topicPub"]}/consumo/#')
    client.on_message = on_message

#   -------------------------------------------------------------------------

#       funções de requisicoes para a névoa ---------------------------------
def maiorConsumo(param):
    print()
    # TODO
    # A nuvem irá enviar uma mensagem para o topico nuvem/consumo
    # contendo o valor n=param referente a quantidade max de hidrometros 
    # na lista de maiores consumidores que ela quer ver.
    # como resposta a nevoa retorna a lista em json dos maiores hidrometros.
    # da nuvem central a lista deve ir para uma pagina web 

def tempoReal(param):
    print()
    # TODO
    # Enviar uma mensagem para o topico nuvem/temporeal/:param
    # onde Param será o id do hidrometro que ele selecionou para ver.
    # a nevoa irá publicar em tempo real no topico desse hidrometro
    # a nuvem deve se inscrever e mandar os dados para a pagina web via websocket.

#   -----------------------------------------------------------------------------

def run ():
    clientNevoa = connect_mqtt(nevoas['broker'], nevoas['port'])
    subscribe(clientNevoa, nevoas['topicSub'])

if __name__ == "__main__":
    run()