import os

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IOT_HUB_HOSTNAME = "rohithub.azure-devices.net"
DEVICE_ID = "pythondevice01"

CERT_FILE = os.path.join(BASE_DIR, "certs", "device-cert.pem")
KEY_FILE = os.path.join(BASE_DIR, "certs", "device-key.pem")

print("BASE_DIR:", BASE_DIR)
print("CERT_FILE:", CERT_FILE)
print("KEY_FILE:", KEY_FILE)
print("CERT Exists:", os.path.exists(CERT_FILE))
print("KEY Exists:", os.path.exists(KEY_FILE))