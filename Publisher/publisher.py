import paho.mqtt.client as mqtt
import random
import time
import json
from datetime import datetime


broker_addr         = "mosquitto"
port                = 1883

temperature_topic   = "sensor/temperature"
humidity_topic      = "sensor/humidity"

client = mqtt.Client("Publisher")

def on_publish(client, userdata, mid):
    print(f"Message published with MID {mid}")


def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("Connected")
    else:
        print(f"Coulld not connect, return code: {return_code}")

# Set the callbacks, this function will be called when the message is published
client.on_publish = on_publish
client.on_connect = on_connect

def publish_message(topic_name, message):
    (result,mid) = client.publish(topic_name, json.dumps(message), qos=1)
    print(f"Published Message " + topic_name + " with message as " + str(message))
    return (result, mid)

client.connect(broker_addr,port)
client.loop_start()

try:
    while True:
        sensor_data = {
            "sensor_id" : "sensor_temperature_" + str(round(random.uniform(10,20))),
            "value" :  round(random.uniform(10,20),4),
            "timestamp" : datetime.now().isoformat()
        }

        #publish temperature data
        (result,mid) = publish_message(temperature_topic, sensor_data)
        if result != mqtt.MQTT_ERR_SUCCESS:
            print(f"Failed to publish temperature data with MID: {mid}")

        # modify message for humidity sensors
        sensor_data["sensor_id"] = "sensor_humidity_" + str(round(random.uniform(10,20)))
        sensor_data["value"] = round(random.uniform(30,40), 4)

        (result,mid) = publish_message(humidity_topic, sensor_data)
        if result != mqtt.MQTT_ERR_SUCCESS:
            print(f"Failed to publish humidity data with MID: {mid}")

        time.sleep(5)
finally:
    client.loop_stop()