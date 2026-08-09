import random
import time
from datetime import datetime

from kafka_producer import send_telemetry


def generate_sensor_data():
    temperature = round(random.uniform(20, 35), 2)
    humidity = round(random.uniform(40, 80), 2)
    pressure = round(random.uniform(990, 1030), 2)
    vibration = round(random.uniform(0.1, 1.0), 2)

    data = {
        "deviceId": "pythondevice01",
        "timestamp": datetime.now().astimezone().isoformat(),
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "vibration": vibration
    }

    return data


while True:
    sensor_data = generate_sensor_data()

    print("Sensor data:", sensor_data)

    send_telemetry(sensor_data)

    time.sleep(2)