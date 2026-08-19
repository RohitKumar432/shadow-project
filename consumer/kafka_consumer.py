from kafka import KafkaConsumer
import json
import csv
from pathlib import Path
import sys

# --------------------------------------------------
# Project root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

from ml.live_detector import process_telemetry


# --------------------------------------------------
# Kafka configuration
# --------------------------------------------------

KAFKA_BROKER = "127.0.0.1:9092"
KAFKA_TOPIC = "iot-telemetry"


# --------------------------------------------------
# Data storage location
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

DATA_DIR.mkdir(exist_ok=True)

CSV_FILE = DATA_DIR / "telemetry.csv"


# --------------------------------------------------
# Create CSV file if it does not exist
# --------------------------------------------------

if not CSV_FILE.exists():

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "deviceId",
            "temperature",
            "humidity",
            "pressure",
            "vibration"
        ])


# --------------------------------------------------
# Create Kafka consumer
# --------------------------------------------------

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="iot-csv-consumer",
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)


# --------------------------------------------------
# Start consuming
# --------------------------------------------------

print("Starting Kafka consumer...")
print("Broker:", KAFKA_BROKER)
print("Topic:", KAFKA_TOPIC)
print("Saving data to:", CSV_FILE)
print()
print("Waiting for telemetry...")
print()


try:

    for message in consumer:

        data = message.value

        print("Telemetry received:")
        print(data)

        # ------------------------------------------
        # Save telemetry to CSV
        # ------------------------------------------

        with open(
            CSV_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                data.get("timestamp"),
                data.get("deviceId"),
                data.get("temperature"),
                data.get("humidity"),
                data.get("pressure"),
                data.get("vibration")
            ])

        print("Saved to:", CSV_FILE)
        print()

        
        # ------------------------------------------
        # Run live ML anomaly detection
        # ------------------------------------------

        print("Running live anomaly detection...")

        process_telemetry(data)

        print()


except KeyboardInterrupt:

    print()
    print("Stopping Kafka consumer...")

finally:

    consumer.close()