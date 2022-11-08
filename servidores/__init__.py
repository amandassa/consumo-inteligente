from flask import Flask
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('nevoa')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
            topic=message.topic,
            payload=message.payload.decode(),
            qos=message.qos,
        )
    match dict.get('topic'):
        case 'hidrometro':
            print()
            # chamar função para salvar no db e ordenar
        case 'nuvem':
            print()
            # chamar função que envia dados necessarios para a nuvem
