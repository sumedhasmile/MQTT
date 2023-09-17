import paho.mqtt.client as mqtt
import random
import time
import json
from datetime import datetime
import logging

# MQTT Broker Configuration
broker_addr = "mosquitto"
port = 1883

# MQTT Topics
temperature_topic = "sensor/temperature"
humidity_topic = "sensor/humidity"

# MQTT Client Configuration
client = mqtt.Client("Publisher")

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and set its level to INFO
file_handler = logging.FileHandler('mqtt_publisher.log')
file_handler.setLevel(logging.INFO)

# Create a formatter and set the formatter for the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

def on_publish(client, userdata, mid):
    logger.info(f"Message published with MID {mid}")

def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        logger.info("Connected")
    else:
        logger.error(f"Could not connect, return code: {return_code}")

# Set the callbacks
client.on_publish = on_publish
client.on_connect = on_connect

def publish_sensor_data(sensor_topic, sensor_id_prefix, value_range):
    try:
        while True:
            sensor_data = {
                "sensor_id": f"{sensor_id_prefix}_{round(random.uniform(10, 20))}",
                "value": round(random.uniform(*value_range), 4),
                "timestamp": datetime.now().isoformat()
            }

            (result, mid) = publish_message(sensor_topic, sensor_data)
            if result != mqtt.MQTT_ERR_SUCCESS:
                logger.error(f"Failed to publish data for {sensor_topic} with MID: {mid}")

            time.sleep(5)
    except KeyboardInterrupt:
        logger.info(f"Stopping publishing for {sensor_topic}")

def publish_message(topic_name, message):
    (result, mid) = client.publish(topic_name, json.dumps(message), qos=1)
    logger.info(f"Published Message {topic_name} with message as {message}")
    return (result, mid)

client.connect(broker_addr, port)
client.loop_start()

try:
    # Publish temperature data
    publish_sensor_data(temperature_topic, "sensor_temperature", (10, 20))

    # Publish humidity data
    publish_sensor_data(humidity_topic, "sensor_humidity", (30, 40))

except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
