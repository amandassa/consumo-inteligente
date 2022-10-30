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
from traceback import print_tb
from paho.mqtt import client as mqtt_client
import json
from threading import Thread

# infos dos hidrometros -------------------------------------
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
hidroDB= {}

#   brokers ---------------------------------------------------------------
central = {
    'broker': 'localhost',      # mudar para maquina central do larsid
    'port': 1883,
    'topicPub': "nuvem/",     # como gerar id para cada no criado?
    'topicSub': "nuvem/#"
}
hidrometros = {
    'broker': 'localhost',  # mudar para maquina hidrometros do larsid
    'port': 1884,
    'topicPub': "hidrometros/bloqueio",
    'topicSub': "hidrometros/status/#"
}
# valores globais ------------------------------------------------------------
LIMITE_CONSUMO = 200

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

# Salva um novo status do hidrometro no DB
# cliente é a instacia mqtt criada na conexão com o broker que se quer ouvir
def salvarHidrometro(msg):     # o nó ouve do hidrometro
    codigoH = msg.topic.split('/')[-1]  # o codigo do hidrometro está no subtopico
    hidroData = json.loads(msg.payload.decode())     # converte a mensagem do hidrômetro em um dicionário
    if codigoH in hidroDB.keys():
        hidroDB[codigoH].insert(0, hidroData)
    else:
        hidroDB[codigoH] = [hidroData]
    return codigoH

'''
deve se inscrever no servidor central e no servidor dos hidrometros
e tratar as mensagens de acordo com a finalidade
client: instancia mqtt criada no método connect_mqtt
'''
def subscribe (client, topico):
    def on_message(client, userdata, msg):
        s = msg.payload.decode('utf-8')
        print(f'MENSAGEM DO HIDROMETRO\n{s}')
        topico = msg.topic.split('/')
        if (topico[0] == 'hidrometros'):
            match topico[1]:
                case 'status':
                    print(f'MENSAGEM DO HIDROMETRO\t{msg.payload.decode()}')
                    codigoH = salvarHidrometro(msg)
                    if (hidroDB[codigoH][0]['consumo'] > LIMITE_CONSUMO):   # checa consumo + recente
                        publish(client, f'{hidrometros["topicPub"]}/bloqueio/{codigoH}', '{"bloqueado":true}')
                case _:
                    pass
        else:
            match topico[1]:
                case 'consumo':
                    # deve enviar a lista com os 10 hidrometros de maior consumo daquele nó
                    # TODO busca e ordenação no banco para os n hidrometros de maior consumo.
                    
                    publish(client, f'nuvem/consumo/{client._client_id}', 'lista10maiores')
                case _:
                    print("Case default")

    client.subscribe(topico)
    client.on_message = on_message

# publica automaticamente sua media parcial para a nuvem 
# (client: cliente da nuvem)
# esta funcao pode ser invocada numa thread para melhor desempenho
# def pubMedia(client):
#     total, count = 0, 0, 0
#     while True:
#         if (len(hidroDB.items())!=0){
#             for k in hidroDB:
#                 total += hidroDB.get(k).get('consumo')
#                 count += 1
#             media = total / count
#             # topico media : nuvem/nos/media/:idnevoa
#             client.publish(f'{central["topicPub"]}/{media}/{client._client_id.decode()}')
#             time.sleep(5)

#         }


def publishTest(client, topic):
    while True:
        client.publish(topic, f'\t{client._client_id.decode()}')
        time.sleep(2)

def publish(client, topic, msg):
    client.publish(topic, msg)
    
def run():
    # conexões com nuvem    ------------------------------------------ 
    # clientCentral = connect_mqtt(central['broker'], central['port'], 'n')
    # clientCentral.loop_start()
    # subscribe(clientCentral, central['topicSub'])
    # conexões com hidrometros    ------------------------------------ 
    time.sleep(2)
    clientHidro = connect_mqtt(hidrometros['broker'], hidrometros['port'], 'h')
    clientHidro.loop_start()
    subscribe(clientHidro, hidrometros['topicSub'])
    publishTest(clientHidro, hidrometros['topicPub'])
    # pubMedia(clientCentral)

if __name__ == "__main__":
    run()