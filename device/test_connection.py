from azure.iot.device import X509
from azure.iot.device import IoTHubDeviceClient

from config import *

print("Creating X509 authentication...")

x509 = X509(
    cert_file=CERT_FILE,
    key_file=KEY_FILE,
)

print("Creating IoT Hub client...")

client = IoTHubDeviceClient.create_from_x509_certificate(
    x509=x509,
    hostname=IOT_HUB_HOSTNAME,
    device_id=DEVICE_ID,
)

print("Connecting to Azure IoT Hub...")

client.connect()

print("SUCCESS!")
print("Connected to Azure IoT Hub.")

client.disconnect()

print("Disconnected.")