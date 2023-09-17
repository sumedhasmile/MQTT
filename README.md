<h5>Below is the high-level diagram of the project</h5>
<img width=“1500” alt=“MQTT” src="https://github.com/sumedhasmile/MQTT/assets/63508421/46aaa968-e169-4106-b0e4-f8850bb8a003">

<h5>Publisher</h5>
The messages of humidity and temperature are published through the MQTT broker to the subscriber at 5-second intervals.

<h5>Subscriber</h5> The messages from the publisher are picked up based on sensor type, and stored in MongoDB and the latest 10 readings of particular sensor type are stored in Redis DB.

<h5>FastAPI</h5>
The messages are pulled from MongoDB for the range of timestamps and sensor type, whereas the latest 10 readings are pulled from Redis with sensor type as input.

<h3>To Run this code below are the steps to be followed using the terminal:</h3>

Clone this repository

https://github.com/sumedhasmile/MQTT.git

Go into the repository

$ cd MQTT

Build the Docker

$ docker-compose build

Run the Docker

$ docker-compose up -d

Go to the below URL of FastAPI using any browser

http://localhost:8080/docs

If want to fetch the data without the above built-in URL then below are the URLs for fetching data separately.

http://localhost:8080/get_last_ten_readings/{sensor-type}/ -> Here sensor-type is humidity or temperature

http://localhost:8080/get_readings/{sensor-type}/{start}/{end} -> here sensor-type is humidity/temperature, the start is start-date, the end is end-date in the ISO format (yyyy-mm-ddThh:mm:ss) eg:-2023-09-16T08:40:40
