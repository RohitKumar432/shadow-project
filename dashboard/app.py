import streamlit as st
import pandas as pd
import os

# -----------------------------
# Dashboard Configuration
# -----------------------------
st.set_page_config(
    page_title="IoT Telemetry Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("IoT Telemetry Dashboard")
st.write("Real-time monitoring of IoT sensor data")

# Path to telemetry CSV
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(BASE_DIR, "data", "telemetry.csv")


# -----------------------------
# Load Data
# -----------------------------
def load_data():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame()

    df = pd.read_csv(CSV_FILE)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


# -----------------------------
# Dashboard
# -----------------------------
@st.fragment(run_every="3s")
def dashboard():

    df = load_data()

    if df.empty:
        st.warning("No telemetry data available yet.")
        return

    # Latest reading
    latest = df.iloc[-1]

    # -----------------------------
    # Latest Sensor Values
    # -----------------------------
    st.subheader("Latest Sensor Reading")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Temperature",
        f"{latest['temperature']:.2f} °C"
    )

    col2.metric(
        "Humidity",
        f"{latest['humidity']:.2f} %"
    )

    col3.metric(
        "Pressure",
        f"{latest['pressure']:.2f} hPa"
    )

    col4.metric(
        "Vibration",
        f"{latest['vibration']:.2f}"
    )

    # -----------------------------
    # Temperature Chart
    # -----------------------------
    st.subheader("Temperature")

    temperature_data = df.set_index("timestamp")[["temperature"]]

    st.line_chart(temperature_data)

    # -----------------------------
    # Humidity Chart
    # -----------------------------
    st.subheader("Humidity")

    humidity_data = df.set_index("timestamp")[["humidity"]]

    st.line_chart(humidity_data)

    # -----------------------------
    # Pressure Chart
    # -----------------------------
    st.subheader("Pressure")

    pressure_data = df.set_index("timestamp")[["pressure"]]

    st.line_chart(pressure_data)

    # -----------------------------
    # Vibration Chart
    # -----------------------------
    st.subheader("Vibration")

    vibration_data = df.set_index("timestamp")[["vibration"]]

    st.line_chart(vibration_data)

    # -----------------------------
    # Raw Telemetry Data
    # -----------------------------
    st.subheader("Telemetry Data")

    st.dataframe(
        df.tail(20),
        use_container_width=True
    )


dashboard()