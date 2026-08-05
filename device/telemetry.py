import time
import json
import random
from datetime import datetime, timezone
from pathlib import Path

from azure.iot.device import IoTHubDeviceClient, X509, Message

from config import IOT_HUB_HOSTNAME, DEVICE_ID, CERT_FILE, KEY_FILE


# Get project folder
BASE_DIR = Path(__file__).resolve().parent.parent

CERT_PATH = BASE_DIR / "certs" / "device-cert.pem"
KEY_PATH = BASE_DIR / "certs" / "device-key.pem"


print("BASE_DIR:", BASE_DIR)
print("CERT_FILE:", CERT_PATH)
print("KEY_FILE:", KEY_PATH)
print("CERT Exists:", CERT_PATH.exists())
print("KEY Exists:", KEY_PATH.exists())


# Create X509 authentication
x509 = X509(
    cert_file=str(CERT_PATH),
    key_file=str(KEY_PATH)
)


# Create IoT Hub client
client = IoTHubDeviceClient.create_from_x509_certificate(
    x509=x509,
    hostname=IOT_HUB_HOSTNAME,
    device_id=DEVICE_ID
)


def generate_sensor_data():

    temperature = round(random.uniform(20.0, 35.0), 2)
    humidity = round(random.uniform(40.0, 80.0), 2)
    pressure = round(random.uniform(990.0, 1030.0), 2)
    vibration = round(random.uniform(0.1, 1.0), 2)

    data = {
        "deviceId": DEVICE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "vibration": vibration
    }

    return data


try:

    print("Connecting to Azure IoT Hub...")

    client.connect()

    print("Connected to Azure IoT Hub.")
    print("Starting telemetry transmission...\n")

    while True:

        data = generate_sensor_data()

        message = Message(json.dumps(data))

        client.send_message(message)

        print("Telemetry sent:")
        print(data)
        print()

        time.sleep(2)


except KeyboardInterrupt:

    print("\nStopping sensor simulator...")


finally:

    client.disconnect()

    print("Disconnected from Azure IoT Hub.")