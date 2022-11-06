'''
A névoa: 
- se conecta ao broker da nuvem (central)
- ouve requisicoes da nuvem (solicitadas a nuvem pela api)
- ouve atualização de status dos hidrometros (que sao enviadas ao topico da nevoa)
- publica para o servidor central as infos dos hidrometros
- publica para os hidrometros a mensagem de bloqueio quando necessário
'''
import random
import time
from paho.mqtt import client as mqtt_client
import json
from threading import Thread

# infos dos hidrometros -------------------------------------
'''
Hidrômetros neste nó (db)
Cada hidrômetro será uma entry no dicionário seguindo:
{codigoH, [
{
    codigo: int, 
    consumo: int (em m3),
    data: time (timestamp),
    bloqueado: boolean
}]}
'''
hidroDB= {}

#   brokers ---------------------------------------------------------------
central = {
    'broker': 'localhost',      # mudar para maquina central do larsid
    'port': 1883,
    'topicPub': "nuvem",     # como gerar id para cada no criado?
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

#       funcões de operações no banco de dados -------------------------------
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

def ultimoRegistro(hidroDB):
    ultimoRegistro = []
    # iterar sobre todas as chaves de hidroDB (todos os hidrometros)
    for k in hidroDB.keys():
    # pegar o registro mais recente (indice 0) de cada um deles -- cada registro é um dicionario
        ultimoRegistro.append(hidroDB[k][0])
    
    return ultimoRegistro

# publica automaticamente sua media parcial para a nuvem 
# (client: cliente da nuvem)
def pubMedia(client):
    total = 0
    while True:
        if (len(hidroDB.items())!=0):
            for k in hidroDB:
                total += hidroDB.get(k)[0].get('consumo')
            mediaNevoa = total / len(hidroDB.keys())
            msg = {
                'media': mediaNevoa,
                'hidrometros': hidroDB.keys()
            }
            # topico media : nuvem/media/:idnevoa
            print('Enviando media')
            client.publish(f'{central["topicPub"]}/media/{client._client_id.decode()}', f'{msg}')
            time.sleep(5)

def pubTempoReal (client, idHidro):
    if (idHidro != 'inexistente' & len(hidroDB[idHidro]) != 0):
        medicaoMaisRecente = json.dumps(hidroDB[idHidro][0])
        client.publish(client, f'{central["topicPub"]}/temporeal/{idHidro}', f'{medicaoMaisRecente}')


#       funções de conectividade com a nuvem e hidrometros ----------------------------
def connect_mqtt(broker, port, prefix):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(f'{prefix}-{random.randint(0, 100)}')
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    
    return client

'''
deve se inscrever no servidor central e no servidor dos hidrometros
e tratar as mensagens de acordo com a finalidade
client: instancia mqtt criada no método connect_mqtt
'''
def subscribe (client, topico):
    def on_message(client, userdata, msg):
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
        else:   # caso a mensagem venha da central
            match topico[1]:    
                case 'consumo':
                    # A nuvem irá enviar uma mensagem para o topico central/consumo
                    # contendo o valor n referente a quantidade max de hidrometros 
                    # na lista de maiores consumidores.
                    s = msg.payload.decode('utf-8')
                    try:
                        top_n = int(s)
                    except:
                        top_n = (len(hidroDB.keys())*0.3)
                    # deve enviar a lista com os 10 hidrometros de maior consumo daquele nó
                    ultimoRegistro = ultimoRegistro(hidroDB)
                    maiorConsumo = ultimoRegistro[0]['consumo']
                    maioresConsumos = []
                    for i in ultimoRegistro:
                        if ultimoRegistro[i]['consumo'] > maiorConsumo:
                            maiorConsumo = ultimoRegistro[i]['consumo']
                            # selecionar apenas os n registros com maior consumo da lista
                            maioresConsumos.append(ultimoRegistro[i])
                            # a seleção dos hidrometros que mais consomem é proporcional a 30% do total
                            if (len(maioresConsumos) >= top_n): break
                    # maioresConsumos = lista com os 10 maiores hidrometros
                    msg = {
                        'maiores': maioresConsumos
                    }
                    # TODO ordenar a lista de forma decrescente
                    publish(client, f'{central["topicPub"]}/consumo/{client._client_id.decode()}', json.dumps(msg))
                case 'temporeal':
                    try:
                        idHidro = int(topico[-1])
                    except:
                        idHidro = 'inexistente'
                    if (idHidro in hidroDB.keys()):
                        pubTempoReal(client, idHidro)
                    else:   # precaução já que a mensagem de temporeal da nuvem será enviada para a névoa que contém o hidrometro
                        publish(client, 'nuvem/temporeal', f'Hidrometro {idHidro} não existe.')
                    # O nó passa a ecoar automaticamente todas as medições de
                    # um determinado hidrometro n=param para a nuvem
                    print('Acompanha um hidrometro em tempo real')

                case 'limiteconsumo':
                    try:
                        LIMITE_CONSUMO = int(msg.payload.decode())
                    except:
                        pass
                    print('Atualizada a variável LIMITE_CONSUMO')
                case _:
                    print("Case default")

    client.subscribe(topico)
    client.on_message = on_message

def publishTest(client, topic):
    while True:
        client.publish(topic, f'\t{client._client_id.decode()}')
        time.sleep(2)

def publish(client, topic, msg):
    client.publish(topic, msg)
#   -----------------------------------------------------------------------------

def run():
    # conexões com nuvem    ------------------------------------------ 
    clientCentral = connect_mqtt(central['broker'], central['port'], 'n')
    clientCentral.loop_start()
    subscribe(clientCentral, central['topicSub'])
    # conexões com hidrometros    ------------------------------------ 
    time.sleep(2)
    clientHidro = connect_mqtt(hidrometros['broker'], hidrometros['port'], 'h')
    clientHidro.loop_start()
    subscribe(clientHidro, hidrometros['topicSub'])
    thread = Thread(target=pubMedia, args=(clientCentral,))
    thread.start()

if __name__ == "__main__":
    run()