import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
import redis

broker_addr         = "mosquitto"
port                = 1883

temperature_topic   = "sensor/temperature"
humidity_topic      = "sensor/humidity"

mongo_uri           = "mongodb://mqtt-mongodb:27017"
mongo_client        = MongoClient(mongo_uri)
db                  = mongo_client["sensor_data"]

redis_host          = "redis-mqtt"
redis_port          = 6379
redis_client        = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

def save_latest_ten_readings_to_redis(sensor_id,value,timestamp,topic_name):
    readings = {
        "sensor_id" : sensor_id,
        "value"     : value,
        "timestamp" : timestamp
    }

    # convert the dict to json string
    json_reading = json.dumps(readings)

    # inserts message to the front of the list for a topic
    redis_list_key = f"{topic_name}_sensor_reading"
    redis_client.lpush(redis_list_key, json_reading)

    # when a new message is inserted using the above lpush method it is inserted at the begining and it is trimmed using 
    # the below function call, only the first 10 messages are saved 10th message is discarded
    redis_client.ltrim(redis_list_key, 0, 9)
    print("Saved data in redis",readings)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker with code {rc}")
        client.subscribe([(temperature_topic, 1), (humidity_topic, 1)])
    else:
        print(f"could not connect, return code: {rc}")

def on_message(client, userdata, message):
    try:
        save_to_db(message)
        print(" Message stored:- ", str(message.payload.decode("utf-8")))
    except Exception as exp:
        print(f"Error in saving data to database",exp)

    
def save_to_db(message):

    payload         = json.loads(message.payload)
    collection_name = "temperature" if message.topic == temperature_topic else "humidity"
    collection      = db[collection_name]

    # save to database
    collection.insert_one(payload)
    print(f"Saved {collection_name} data to Database. Payload: {payload}")

    # save latest 10 readings to redis
    save_latest_ten_readings_to_redis(payload["sensor_id"],payload["value"],payload["timestamp"],collection_name)


client = mqtt.Client("Subscriber")

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_addr,port)

client.loop_forever()