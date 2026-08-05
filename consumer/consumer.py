from azure.eventhub import EventHubConsumerClient
from dotenv import load_dotenv
import json
import os
import csv
from pathlib import Path

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STRING")
EVENTHUB_NAME = os.getenv("EVENT_HUB_NAME")
CONSUMER_GROUP = os.getenv("CONSUMER_GROUP")


# --------------------------------------------------
# Data storage location
# --------------------------------------------------

DATA_DIR = BASE_DIR.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

CSV_FILE = DATA_DIR / "telemetry.csv"


# --------------------------------------------------
# Create CSV file if it does not exist
# --------------------------------------------------

if not CSV_FILE.exists():

    with open(CSV_FILE, "w", newline="") as file:

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
# Receive telemetry
# --------------------------------------------------

def on_event(partition_context, event):

    print("Telemetry received:")

    data = json.loads(event.body_as_str())

    print(data)
    print()


    # --------------------------------------------------
    # Save telemetry to CSV
    # --------------------------------------------------

    with open(CSV_FILE, "a", newline="") as file:

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


    # Update checkpoint
    partition_context.update_checkpoint(event)


# --------------------------------------------------
# Create Event Hub consumer
# --------------------------------------------------

client = EventHubConsumerClient.from_connection_string(

    conn_str=CONNECTION_STR,

    consumer_group=CONSUMER_GROUP,

    eventhub_name=EVENTHUB_NAME
)


# --------------------------------------------------
# Start consumer
# --------------------------------------------------

try:

    print("Starting telemetry consumer...")
    print("Waiting for messages...")
    print("Data will be saved to:")
    print(CSV_FILE)
    print()

    with client:

        client.receive(

            on_event=on_event,

            starting_position="-1"

        )

except KeyboardInterrupt:

    print()
    print("Stopping telemetry consumer...")

finally:

    client.close()