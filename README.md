<img width="1500" alt="MQTT" src="https://github.com/sumedhasmile/MQTT/assets/63508421/46aaa968-e169-4106-b0e4-f8850bb8a003">

Publisher:-   The messages of humidity and temperature are published through the MQTT broker to the subscriber at 5-second intervals. 
Subscriber:-  The messages from the publisher are picked up based on sensor type, stored in MongoDB and the latest 10 readings of particular sensor type are stored in Redis DB.
FASTAPI:-     The messages are pulled from MongoDB for the range of timestamps and sensor type, whereas the latest 10 readings are pulled from Redis with sensor type as input.

To Run this code below are the steps to be followed:-
1) Clone this repository
   https://github.com/sumedhasmile/MQTT.git
2) go into the repository
   
   cd MQTT
4) Build the Docker
   
   docker-compose build
5) Run the Docker
   
   docker-compose up -d
7) Go to the below URL of FASTAPI
   http://localhost:8080/docs 
If want to fetch the data without the above built-in URL then below are the URLs for fetching data separately
http://localhost:8080/get_last_ten_readings/{sensor-type}/ -> Here sensor-type is humidity or temperature
http://localhost:8080/get_readings/{sensor-type}/{start}/{end} -> here sensor-type is humidity/temperature, the start is start-date, the end is end-date in the ISO format (yyyy-mm-ddThh:mm:ss)eg:-2023-09-16T08:40:40
