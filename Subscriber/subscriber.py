import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json
import redis

broker_addr         = "mqtt.eclipseprojects.io"
port                = 1883

temperature_topic   = "sensor/temperature"
humidity_topic      = "sensor/humidity"



def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker with code {rc}")
        client.subscribe([(temperature_topic, 1), (humidity_topic, 1)])
    else:
        print(f"could not connect, return code: {rc}")

def on_message(client, userdata, message):
    print(" Message recieved", str(message.payload.decode("utf-8")))
    

client = mqtt.Client("Subscriber")

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_addr)

client.loop_forever()