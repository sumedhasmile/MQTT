# Use an official Python runtime as a parent image
FROM python:3.10

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# Set the working directory to /app
WORKDIR /mqtt_subscriber

# Copy the current directory contents into the container at /app
COPY . /mqtt_subscriber

RUN pip install paho-mqtt pymongo redis

# Run subscriber.py when the container launches
CMD ["python", "subscriber.py"]