from typing import Union
from fastapi import FastAPI, Query, HTTPException, Path
from pymongo import MongoClient
from datetime import datetime
import redis
import json

app = FastAPI()

mongo_uri               = "mongodb://mqtt-mongodb:27017"
mongo_client            = MongoClient(mongo_uri)
db                      = mongo_client["sensor_data"]

temperature_collection  = "temperature"
humidity_collection     = "hummidity"

redis_host              = "redis-mqtt"
redis_port              = 6379
redis_client            = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

ALLOWED_SENSOR_TYPES    = {"temperature", "humidity"}

def is_valid_sensor_type(sensor_type: str) -> bool:
    return sensor_type in ALLOWED_SENSOR_TYPES

# Endpoint to get sensor readings for a sensor given the timestamp range
@app.get("/get_readings/{sensor_type}/")
async def get_readings_for_range( sensor_type: str = Path(..., description="Sensor type"),
                            start: datetime = Query(..., description="Start timestamp"),
                            end: datetime = Query(..., description="End timestamp")):
    
    if not is_valid_sensor_type(sensor_type):
        raise HTTPException(status_code=400, detail="Invalid sensor type")
    
    try:
        start_dateTime = datetime.fromisoformat(str(start)).isoformat()
        end_dateTime = datetime.fromisoformat(str(end)).isoformat()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")
    
    query = {
        "timestamp": {"$gte": start_dateTime, "$lte": end_dateTime}
    }
    collection  = db[sensor_type]
    
    readings = list(collection.find(query))
    serialized_readings = [json.loads(json.dumps(reading, default=str)) for reading in readings]
   
    return serialized_readings

# Endpoint to get last ten readings for a sensor form redis
@app.get("/get_last_ten_readings/{sensor_type}/")
async def get_reading_for_sensor(sensor_type: str = Path(..., description="Sensor type")):

    if not is_valid_sensor_type(sensor_type):
        raise HTTPException(status_code=400, detail="Invalid sensor type")

    redis_key = f"{sensor_type}_sensor_reading"
    readings = redis_client.lrange(redis_key, 0, -1)
    

    parsed_readings = [json.loads(reading) for reading in readings]
    
    return parsed_readings