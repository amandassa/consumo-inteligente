'''
A névoa: 
- se conecta ao broker da nuvem (central)
- ouve requisicoes da nuvem (solicitadas a nuvem pela api)
- ouve atualização de status dos hidrometros (que sao enviadas ao topico da nevoa)
- publica para o servidor central as infos dos hidrometros
- publica para os hidrometros a mensagem de bloqueio quando necessário
'''
from concurrent.futures import thread
from itertools import count
import random
import time
from paho.mqtt import client as mqtt_client
import json
from threading import Thread

# infos dos hidrometros
'''
Hidrômetros neste nó (db)
Cada hidrômetro será uma entry no dicionário seguindo:
codigoH, 
{
    codigo: int, 
    consumo: int (em m3),
    data: time (timestamp),
    bloqueado: boolean
}
'''
hidrometros = {}

central = {
    'broker': 'localhost',      # mudar para maquina central do larsid
    'port': 1883,
    'topicPub': "nuvem/nos",     # como gerar id para cada no criado?
    'topicSub': "nuvem/nos/#"
}
hidrometros = {
    'broker': 'localhost',  # mudar para maquina hidrometros do larsid
    'port': 1884,
    'topicPub': "hidrometros/",     # como gerar id para cada no criado?
    'topicSub': "hidrometros/#"
}
# username = 'emqx'
# password = 'public'
# generate client ID with pub prefix randomly
# client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt(broker, port, prefix):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(f'{prefix}-{random.randint(0, 1000)}')
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    
    return client

# cliente é a instacia mqtt criada na conexão com o broker que se quer ouvir
def handleHidrometro(msg):     # o nó ouve do hidrometro
    codigoH = msg.topic.split('/')[-1]
    hidroData = json.loads(msg.payload.decode())     # converte a mensagem do hidrômetro em um dicionário
    hidrometros[codigoH] = hidroData

'''
deve se inscrever no servidor central e tratar as mensagens de acordo com a finalidade
client: instancia mqtt criada no método connect_mqtt
topicos e subtopicos da nuvem: 
    /nos : mensagens da nuvem para os nós
    /api : mensagens da api para a nuvem
'''
def subscribe (client, topico):
    def on_message(client, userdata, msg):
        topico = msg.topic.split('/')
        match topico[0]:
            case 'hidrometros':
                handleHidrometro(msg)
                # TODO adicionar verificação de consumo para o bloqueio
                print(f'hidrometros\t:\t{msg.payload.decode()}')

            case 'nuvem':
                print(f'de nuvem para nos\t:\t{msg.payload.decode()}')
                # deve enviar a lista com os 10 hidrometros de maior consumo daquele nó
                # -- isso pode ser feito automaticamente periodicamente mas ainda não foi decidido.
            case _:
                print("Case default")

    client.subscribe(topico)     # se inscreve no topico da nuvem referente aos nos.
    client.on_message = on_message

# publica automaticamente sua media parcial para a nuvem 
# (client: cliente da nuvem)
# esta funcao pode ser invocada numa thread para melhor desempenho
def pubMedia(client):
    total, count, media = 0, 0, 0
    while True:
        for k in hidrometros:
            total += hidrometros[k]['consumo']
            count += 1
        media = total / count
        # topico media : nuvem/nos/media/:idnevoa
        client.publish(f'{central["topicPub"]}/{media}/{client._client_id.decode()}')
        time.sleep(5)
    

def publish(client, topic, msg):
    client.publish(topic, f'{client._client_id.decode()}')
    time.sleep(2)
    
def run():
    # conexões com nuvem    ------------------------------------------ 
    clientCentral = connect_mqtt(central['broker'], central['port'], 'n')
    clientCentral.loop_start()
    subscribe(clientCentral, central['topicSub'])
    # conexões com hidrometros    ------------------------------------ 
    time.sleep(2)
    clientHidro = connect_mqtt(hidrometros['broker'], hidrometros['port'], 'h')
    clientHidro.loop_start()
    print(clientHidro._client_id)
    subscribe(clientHidro, hidrometros['topicSub'])
    pubMedia(clientCentral)

if __name__ == "__main__":
    run()