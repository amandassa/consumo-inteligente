import random
from paho.mqtt import client as mqtt_client
import json

# infos dos hidrometros
'''
Hidrômetros neste nó (db)
Cada hidrômetro será uma entry no dicionário seguindo:
codigo: int, 
consumo: int (em m3),
data: time (timestamp),
bloqueado: boolean
'''
hidrometros = {}

# Alterar futuramente para credenciais do broker central
broker = 'broker.emqx.io'
port = 1883
topic = "nuvem/nos/#"
username = 'emqx'
password = 'public'
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# cliente é a instacia mqtt criada na conexão com o broker que se quer ouvir
def handleHidrometro(cliente, msg):     # o nó ouve do hidrometro
    codigoH = msg.topic.split('/')
    hidroData = json.loads(msg.payload.decode())     # converte a mensagem do hidrômetro em um dicionário
    hidrometros[codigoH] = hidroData

'''
deve se inscrever no servidor central e tratar as mensagens de acordo com a finalidade
cliente: instancia mqtt criada no método connect_mqtt
'''
def subCentral (client):
    client.subscribe(topic)     # se inscreve no topico da nuvem. o nó publica neste tópico
    def on_message(client, userdata, msg):
        topico = msg.topic.split('/')
        match topico[1]:
            case "bloqueio":
                print("Case bloqueios")
                # deve ver qual tipo de bloqueio,
                # qual hidrometro deve ser bloqueado e enviar a mensagem ao hidrometro
            case "hidrometros":
                print("Case hidrometros")
                # deve enviar a lista com os 10 hidrometros de maior consumo daquele nó
                # -- isso pode ser feito automaticamente periodicamente mas ainda não foi decidido.
            case _:
                print("Case default")