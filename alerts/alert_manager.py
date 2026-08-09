from datetime import datetime


def generate_alert(device_id, telemetry, anomaly_score):
    """
    Generate an alert when an anomaly is detected.
    """

    timestamp = datetime.now().astimezone().isoformat()

    print("\n" + "=" * 60)
    print("⚠️  ANOMALY DETECTED")
    print("=" * 60)

    print(f"Time          : {timestamp}")
    print(f"Device        : {device_id}")

    print(f"Temperature   : {telemetry['temperature']} °C")
    print(f"Humidity      : {telemetry['humidity']} %")
    print(f"Pressure      : {telemetry['pressure']} hPa")
    print(f"Vibration     : {telemetry['vibration']}")

    print(f"Anomaly Score : {anomaly_score}")

    print("=" * 60)


if __name__ == "__main__":

    # Test telemetry data
    test_telemetry = {
        "temperature": 79.72,
        "humidity": 20.24,
        "pressure": 990.52,
        "vibration": 0.95
    }

    generate_alert(
        device_id="pythondevice01",
        telemetry=test_telemetry,
        anomaly_score=-0.097850
    )