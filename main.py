from flask import Flask
from flask_mqtt import Mqtt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = os.getenv('MQTT_BROKER_URL')
app.config['MQTT_BROKER_PORT'] = int(os.getenv('MQTT_BROKER_PORT'))
app.config['MQTT_USERNAME'] = os.getenv('MQTT_USERNAME')
app.config['MQTT_PASSWORD'] = os.getenv('MQTT_PASSWORD')
app.config['MQTT_CLIENT_ID'] = os.getenv('MQTT_CLIENT_ID')
app.config['MQTT_REFRESH_TIME'] = float(os.getenv('MQTT_REFRESH_TIME'))
mqtt = Mqtt(app)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('Controle de Acesso')

@app.route('/send_signal')
def send_signal():
    mqtt.publish('Controle de Acesso', 'Abra')
    return "Porta Aberta"

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)


if __name__ == '__main__':
    app.run(debug=True, port=3002)
