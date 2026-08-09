from kafka import KafkaProducer
import json

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "iot-telemetry"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)


def send_telemetry(data):
    try:
        producer.send(KAFKA_TOPIC, value=data)
        producer.flush()

        print("Sent to Kafka:", data)

    except Exception as e:
        print("Kafka error:", e)