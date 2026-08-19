import os
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
TELEMETRY_FILE = DATA_DIR / "telemetry.csv"
ANOMALY_FILE = DATA_DIR / "anomaly_results.csv"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="IoT Telemetry Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }

        .metric-card {
            padding: 10px;
        }

        .section-title {
            font-size: 1.4rem;
            font-weight: 650;
            margin-top: 1rem;
            margin-bottom: 0.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📡 IoT Telemetry Dashboard</div>',
    unsafe_allow_html=True,
)

st.markdown(
    "Real-time monitoring and anomaly detection of IoT sensor data",
)

st.divider()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_csv(file_path):
    """
    Load a CSV safely.
    Returns an empty DataFrame if the file does not exist
    or cannot be read.
    """

    if not file_path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error reading {file_path.name}: {e}")
        return pd.DataFrame()


def convert_timestamp(df):
    """
    Convert timestamps using utc=True.

    This fixes:
    Mixed timezones detected.
    """

    if df.empty:
        return df

    if "timestamp" in df.columns:

        try:
            df["timestamp"] = pd.to_datetime(
                df["timestamp"],
                utc=True,
                errors="coerce",
            )

            # Remove rows where timestamp conversion failed
            df = df.dropna(subset=["timestamp"])

        except Exception as e:
            st.warning(f"Timestamp conversion warning: {e}")

    return df


def find_column(df, possible_names):
    """
    Find a column using several possible names.
    """

    for name in possible_names:
        if name in df.columns:
            return name

    return None


# ============================================================
# LOAD TELEMETRY DATA
# ============================================================

telemetry_df = load_csv(TELEMETRY_FILE)

if not telemetry_df.empty:
    telemetry_df = convert_timestamp(telemetry_df)


# ============================================================
# LOAD ANOMALY DATA
# ============================================================

anomaly_df = load_csv(ANOMALY_FILE)

if not anomaly_df.empty:
    anomaly_df = convert_timestamp(anomaly_df)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Dashboard Controls")

auto_refresh = st.sidebar.checkbox(
    "Auto refresh",
    value=False,
)

rows_to_display = st.sidebar.slider(
    "Rows to display",
    min_value=5,
    max_value=100,
    value=20,
)


if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()


# ============================================================
# TELEMETRY SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">📊 Telemetry Overview</div>',
    unsafe_allow_html=True,
)


if telemetry_df.empty:

    st.warning("No telemetry data available yet.")

    telemetry_available = False

else:

    telemetry_available = True

    temperature_col = find_column(
        telemetry_df,
        ["temperature", "Temperature", "temp"],
    )

    humidity_col = find_column(
        telemetry_df,
        ["humidity", "Humidity"],
    )

    pressure_col = find_column(
        telemetry_df,
        ["pressure", "Pressure"],
    )

    vibration_col = find_column(
        telemetry_df,
        ["vibration", "Vibration"],
    )

    device_col = find_column(
        telemetry_df,
        ["deviceId", "device_id", "device", "Device"],
    )

    total_records = len(telemetry_df)

    if device_col:
        unique_devices = telemetry_df[device_col].nunique()
    else:
        unique_devices = 0

    latest_time = None

    if "timestamp" in telemetry_df.columns and not telemetry_df.empty:
        latest_time = telemetry_df["timestamp"].max()


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Telemetry Records",
            f"{total_records:,}",
        )

    with col2:
        st.metric(
            "Devices",
            unique_devices,
        )

    with col3:

        if temperature_col:
            latest_temperature = telemetry_df[
                temperature_col
            ].iloc[-1]

            st.metric(
                "Latest Temperature",
                f"{latest_temperature:.2f} °C",
            )

        else:
            st.metric(
                "Latest Temperature",
                "N/A",
            )

    with col4:

        if latest_time is not None:
            st.metric(
                "Latest Reading",
                latest_time.strftime("%H:%M:%S"),
            )

        else:
            st.metric(
                "Latest Reading",
                "N/A",
            )


# ============================================================
# LATEST TELEMETRY DATA
# ============================================================

st.markdown(
    '<div class="section-title">📋 Latest Telemetry Data</div>',
    unsafe_allow_html=True,
)


if telemetry_available:

    latest_data = telemetry_df.tail(
        rows_to_display
    ).copy()

    # Display timestamps in readable format
    if "timestamp" in latest_data.columns:

        latest_data["timestamp"] = latest_data[
            "timestamp"
        ].dt.strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )

    st.dataframe(
        latest_data,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info("Telemetry table will appear when telemetry data is available.")


# ============================================================
# TELEMETRY CHARTS
# ============================================================

if telemetry_available:

    st.markdown(
        '<div class="section-title">📈 Telemetry Trends</div>',
        unsafe_allow_html=True,
    )

    chart_df = telemetry_df.copy()

    if "timestamp" in chart_df.columns:
        chart_df = chart_df.set_index("timestamp")


    # Temperature
    if temperature_col:

        st.subheader("Temperature")

        temperature_chart = chart_df[
            [temperature_col]
        ].tail(200)

        st.line_chart(
            temperature_chart,
            use_container_width=True,
        )


    # Humidity
    if humidity_col:

        st.subheader("Humidity")

        humidity_chart = chart_df[
            [humidity_col]
        ].tail(200)

        st.line_chart(
            humidity_chart,
            use_container_width=True,
        )


    # Pressure
    if pressure_col:

        st.subheader("Pressure")

        pressure_chart = chart_df[
            [pressure_col]
        ].tail(200)

        st.line_chart(
            pressure_chart,
            use_container_width=True,
        )


    # Vibration
    if vibration_col:

        st.subheader("Vibration")

        vibration_chart = chart_df[
            [vibration_col]
        ].tail(200)

        st.line_chart(
            vibration_chart,
            use_container_width=True,
        )


# ============================================================
# ANOMALY DETECTION SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">🚨 Anomaly Detection Summary</div>',
    unsafe_allow_html=True,
)


if anomaly_df.empty:

    st.warning("No anomaly results available yet.")

    anomaly_available = False

else:

    anomaly_available = True

    status_col = find_column(
        anomaly_df,
        [
            "prediction",
            "status",
            "anomaly",
            "Anomaly",
            "label",
        ],
    )

    score_col = find_column(
        anomaly_df,
        [
            "anomaly_score",
            "anomalyScore",
            "score",
            "Anomaly Score",
        ],
    )


    # --------------------------------------------------------
    # Calculate anomaly count
    # --------------------------------------------------------

    anomaly_count = 0

    if status_col:

        values = (
            anomaly_df[status_col]
            .astype(str)
            .str.lower()
        )

        anomaly_count = values.str.contains(
            "anomaly"
        ).sum()

        # Also handle common ML labels
        anomaly_count += (
            values == "-1"
        ).sum()


    normal_count = len(anomaly_df) - anomaly_count


    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total ML Results",
            f"{len(anomaly_df):,}",
        )

    with col2:

        st.metric(
            "Anomalies Detected",
            f"{anomaly_count:,}",
        )

    with col3:

        st.metric(
            "Normal Records",
            f"{normal_count:,}",
        )


# ============================================================
# ANOMALY DETECTION HISTORY
# ============================================================

st.markdown(
    '<div class="section-title">🔎 Anomaly Detection History</div>',
    unsafe_allow_html=True,
)


if anomaly_available:

    anomaly_display = anomaly_df.tail(
        rows_to_display
    ).copy()


    if "timestamp" in anomaly_display.columns:

        anomaly_display["timestamp"] = (
            anomaly_display["timestamp"]
            .dt.strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
        )


    st.dataframe(
        anomaly_display,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "Anomaly detection history will appear when ML results are available."
    )


# ============================================================
# ANOMALY SCORE CHART
# ============================================================

if anomaly_available and score_col:

    st.markdown(
        '<div class="section-title">📉 Anomaly Score</div>',
        unsafe_allow_html=True,
    )

    score_df = anomaly_df.copy()

    score_df[score_col] = pd.to_numeric(
        score_df[score_col],
        errors="coerce",
    )

    score_df = score_df.dropna(
        subset=[score_col]
    )

    if "timestamp" in score_df.columns:

        score_df = score_df.set_index(
            "timestamp"
        )


    score_chart = score_df[
        [score_col]
    ].tail(200)

    st.line_chart(
        score_chart,
        use_container_width=True,
    )


# ============================================================
# RECENT ANOMALIES
# ============================================================

if anomaly_available and status_col:

    st.markdown(
        '<div class="section-title">🚨 Recent Anomalies</div>',
        unsafe_allow_html=True,
    )

    status_values = (
        anomaly_df[status_col]
        .astype(str)
        .str.lower()
    )

    recent_anomalies = anomaly_df[
        status_values.str.contains("anomaly")
        | (status_values == "-1")
    ].tail(20).copy()


    if not recent_anomalies.empty:

        if "timestamp" in recent_anomalies.columns:

            recent_anomalies[
                "timestamp"
            ] = recent_anomalies[
                "timestamp"
            ].dt.strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )

        st.dataframe(
            recent_anomalies,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.success(
            "No recent anomalies detected."
        )


# ============================================================
# DATA FILE STATUS
# ============================================================

st.markdown(
    '<div class="section-title">📁 Data Pipeline Status</div>',
    unsafe_allow_html=True,
)


col1, col2 = st.columns(2)


with col1:

    if TELEMETRY_FILE.exists():

        telemetry_size = (
            TELEMETRY_FILE.stat().st_size
        )

        st.success(
            f"Telemetry data connected\n\n"
            f"`{TELEMETRY_FILE.name}` — "
            f"{telemetry_size:,} bytes"
        )

    else:

        st.error(
            "telemetry.csv not found"
        )


with col2:

    if ANOMALY_FILE.exists():

        anomaly_size = (
            ANOMALY_FILE.stat().st_size
        )

        st.success(
            f"Anomaly data connected\n\n"
            f"`{ANOMALY_FILE.name}` — "
            f"{anomaly_size:,} bytes"
        )

    else:

        st.error(
            "anomaly_results.csv not found"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "IoT Telemetry Monitoring & Anomaly Detection System"
)


# ============================================================
# OPTIONAL AUTO REFRESH
# ============================================================

if auto_refresh:

    try:

        from streamlit_autorefresh import st_autorefresh

        st_autorefresh(
            interval=5000,
            key="iot_dashboard_refresh",
        )

    except ImportError:

        st.sidebar.warning(
            "Install streamlit-autorefresh for automatic refresh."
        )