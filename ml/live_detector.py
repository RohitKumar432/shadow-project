import pandas as pd
from pathlib import Path
import joblib
import sys

# ============================================================
# Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_FILE = PROJECT_ROOT / "ml" / "model.pkl"
OUTPUT_FILE = PROJECT_ROOT / "data" / "anomaly_results.csv"

# Allow importing alert manager
sys.path.insert(0, str(PROJECT_ROOT))

from alerts.alert_manager import generate_alert


# ============================================================
# Load trained model
# ============================================================

print("Loading trained anomaly detection model...")

model = joblib.load(MODEL_FILE)

print("Model loaded successfully.")
print("Model:", MODEL_FILE)


# ============================================================
# Sensor features
# ============================================================

FEATURES = [
    "temperature",
    "humidity",
    "pressure",
    "vibration"
]


# ============================================================
# Create anomaly results file if required
# ============================================================

if not OUTPUT_FILE.exists():

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    pd.DataFrame(
        columns=[
            "timestamp",
            "deviceId",
            "temperature",
            "humidity",
            "pressure",
            "vibration",
            "anomaly",
            "anomaly_score"
        ]
    ).to_csv(
        OUTPUT_FILE,
        index=False
    )


# ============================================================
# Process one telemetry record
# ============================================================

def process_telemetry(data):

    # --------------------------------------------------------
    # Create DataFrame for model prediction
    # --------------------------------------------------------

    input_data = pd.DataFrame(
        [[
            data["temperature"],
            data["humidity"],
            data["pressure"],
            data["vibration"]
        ]],
        columns=FEATURES
    )

    # --------------------------------------------------------
    # Predict
    # --------------------------------------------------------

    prediction = model.predict(input_data)[0]

    # Isolation Forest:
    #  1  = Normal
    # -1  = Anomaly

    if prediction == -1:
        anomaly_status = "Anomaly"
    else:
        anomaly_status = "Normal"

    # --------------------------------------------------------
    # Calculate anomaly score
    # --------------------------------------------------------

    anomaly_score = model.decision_function(
        input_data
    )[0]

    # --------------------------------------------------------
    # Create result
    # --------------------------------------------------------

    result = {
        "timestamp": data.get("timestamp"),
        "deviceId": data.get("deviceId"),
        "temperature": data.get("temperature"),
        "humidity": data.get("humidity"),
        "pressure": data.get("pressure"),
        "vibration": data.get("vibration"),
        "anomaly": anomaly_status,
        "anomaly_score": anomaly_score
    }

    # --------------------------------------------------------
    # Save result
    # --------------------------------------------------------

    result_df = pd.DataFrame([result])

    result_df.to_csv(
        OUTPUT_FILE,
        mode="a",
        header=False,
        index=False
    )

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print()
    print("ML RESULT")
    print("-" * 50)
    print("Device        :", data.get("deviceId"))
    print("Temperature   :", data.get("temperature"))
    print("Humidity      :", data.get("humidity"))
    print("Pressure      :", data.get("pressure"))
    print("Vibration     :", data.get("vibration"))
    print("Status        :", anomaly_status)
    print("Anomaly Score :", round(anomaly_score, 6))
    print("-" * 50)

    # --------------------------------------------------------
    # Generate alert
    # --------------------------------------------------------

    if anomaly_status == "Anomaly":

        telemetry = {
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "pressure": data.get("pressure"),
            "vibration": data.get("vibration")
        }

        generate_alert(
            device_id=data.get("deviceId"),
            telemetry=telemetry,
            anomaly_score=anomaly_score
        )

    return result