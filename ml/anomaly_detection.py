import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest
import joblib

import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from alerts.alert_manager import generate_alert


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "data" / "telemetry.csv"
MODEL_FILE = BASE_DIR / "ml" / "model.pkl"
OUTPUT_FILE = BASE_DIR / "data" / "anomaly_results.csv"


# --------------------------------------------------
# Load telemetry data
# --------------------------------------------------

print("Loading telemetry data...")
print("File:", CSV_FILE)

df = pd.read_csv(CSV_FILE)

print()
print("Total records:", len(df))


# --------------------------------------------------
# Select sensor features
# --------------------------------------------------

features = [
    "temperature",
    "humidity",
    "pressure",
    "vibration"
]

X = df[features]


# --------------------------------------------------
# Train Isolation Forest
# --------------------------------------------------

print()
print("Training anomaly detection model...")

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(X)


# --------------------------------------------------
# Predict anomalies
# --------------------------------------------------

df["anomaly_prediction"] = model.predict(X)

# Isolation Forest:
# 1  = Normal
# -1 = Anomaly

df["anomaly"] = df["anomaly_prediction"].apply(
    lambda x: "Anomaly" if x == -1 else "Normal"
)


# --------------------------------------------------
# Calculate anomaly score
# --------------------------------------------------

df["anomaly_score"] = model.decision_function(X)


# --------------------------------------------------
# Generate alerts for anomalies
# --------------------------------------------------

print()
print("Checking for anomalies and generating alerts...")

for _, row in df[df["anomaly"] == "Anomaly"].iterrows():

    telemetry = {
        "temperature": row["temperature"],
        "humidity": row["humidity"],
        "pressure": row["pressure"],
        "vibration": row["vibration"]
    }

    generate_alert(
        device_id=row["deviceId"],
        telemetry=telemetry,
        anomaly_score=row["anomaly_score"]
    )


# --------------------------------------------------
# Save model
# --------------------------------------------------

joblib.dump(model, MODEL_FILE)


# --------------------------------------------------
# Save results
# --------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)


# --------------------------------------------------
# Display results
# --------------------------------------------------

normal_count = (df["anomaly"] == "Normal").sum()
anomaly_count = (df["anomaly"] == "Anomaly").sum()

print()
print("====================================")
print("ANOMALY DETECTION COMPLETE")
print("====================================")

print("Normal records :", normal_count)
print("Anomaly records:", anomaly_count)

print()
print("Model saved to:")
print(MODEL_FILE)

print()
print("Results saved to:")
print(OUTPUT_FILE)

print()
print("Sample results:")

print(
    df[
        [
            "timestamp",
            "deviceId",
            "temperature",
            "humidity",
            "pressure",
            "vibration",
            "anomaly",
            "anomaly_score"
        ]
    ].tail(10)
)