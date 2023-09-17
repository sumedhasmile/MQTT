import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
import redis
import logging

# MQTT Broker Configuration
broker_addr = "mosquitto"
port = 1883

temperature_topic = "sensor/temperature"
humidity_topic = "sensor/humidity"

# MongoDB Configuration
mongo_uri = "mongodb://mqtt-mongodb:27017"
mongo_client = MongoClient(mongo_uri)
db = mongo_client["sensor_data"]

# Redis Configuration
redis_host = "redis-mqtt"
redis_port = 6379
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and set its level to INFO
file_handler = logging.FileHandler('mqtt_subscriber.log')
file_handler.setLevel(logging.INFO)


# Create a formatter and set the formatter for the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

def save_latest_ten_readings_to_redis(sensor_id, value, timestamp, topic_name):
    try:
        readings = {
            "sensor_id": sensor_id,
            "value": value,
            "timestamp": timestamp
        }

        # Convert the dict to a JSON string
        json_reading = json.dumps(readings)

        # Inserts message to the front of the list for a topic
        redis_list_key = f"{topic_name}_sensor_reading"
        redis_client.lpush(redis_list_key, json_reading)

        # When a new message is inserted using the above lpush method, it is inserted at the beginning,
        # and it is trimmed to keep only the first 10 messages (10th message is discarded)
        redis_client.ltrim(redis_list_key, 0, 9)
        logger.info("Saved data in Redis: %s", readings)
    except Exception as e:
        logger.error("Error saving data to Redis: %s", e)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker with code %d", rc)
        client.subscribe([(temperature_topic, 1), (humidity_topic, 1)])
    else:
        logger.error("Could not connect to MQTT broker, return code: %d", rc)

def on_message(client, userdata, message):
    try:
        save_to_db(message)
        logger.info("Message stored in MongoDB: %s", str(message.payload.decode("utf-8")))
    except Exception as exp:
        logger.error("Error in saving data to database: %s", exp)

def save_to_db(message):
    try:
        payload = json.loads(message.payload)
        collection_name = "temperature" if message.topic == temperature_topic else "humidity"
        collection = db[collection_name]

        # Save to the database
        collection.insert_one(payload)
        logger.info("Saved %s data to Database. Payload: %s", collection_name, payload)

        # Save latest 10 readings to Redis
        save_latest_ten_readings_to_redis(payload["sensor_id"], payload["value"], payload["timestamp"], collection_name)
    except Exception as e:
        logger.error("Error saving data to database: %s", e)

client = mqtt.Client("Subscriber")

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_addr, port)

logger.info("MQTT Subscriber started")
client.loop_forever()
