from kafka_producer import send_telemetry

test_data = {
    "device_id": "pythondevice01",
    "temperature": 25.5,
    "humidity": 60.2,
    "pressure": 1012.3,
    "vibration": 0.12
}

send_telemetry(test_data)