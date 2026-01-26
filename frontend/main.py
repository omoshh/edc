import streamlit as st
import pandas as pd
import plotly
import requests
import datetime

st.set_page_config(page_title="System Metrics", layout="wide")

REFRESH_OPTIONS = {
    "30s": 30,
    "1m": 60
}

with st.sidebar:
    st.header("Settings")
    selected_label = st.selectbox(
        "Select update frequency",
        options=list(REFRESH_OPTIONS.keys()),
        index=0
    )
    freq_ms = REFRESH_OPTIONS[selected_label]
    st.info(f"Refreshes every {selected_label}")

# get metrics from API
def get_metrics():
    try:
        response = requests.get(st.secrets["API_METRICS"])
        response.raise_for_status() 
        df = pd.DataFrame([response.json()])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()

# main ui
@st.fragment(run_every=freq_ms)
def metrics():
    st.header("Current system metrics:")
    df = get_metrics()
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        latest = df.iloc[0] 

        col1.metric(label="CPU", value=f"{latest['cpu_usage']}%")
        col2.metric(label="Memory", value=f"{latest['ram_usage']}%")
        col3.metric(label="Load Average", value=f"{latest['load_average']}")
        col4.metric(label="Network Bandwidth", value=f"{latest['network_bandwidth']}Mb/s")
        d1, = st.columns(1)
        time_string = latest['timestamp'].strftime("%H:%M:%S")
        d1.metric(label="Measured at", value=time_string)
    else:
        st.warning("No data available. Check if the backend is running.")
metrics()

st.divider()
st.header("Request metrics from a time interval:")
left_col, right_col = st.columns(2)
with left_col:  
    start = st.datetime_input("Choose start", value=None, format="DD/MM/YYYY")
with right_col:
    end = st.datetime_input("Choose end", value=None, format="DD/MM/YYYY", max_value="now")

if st.button("Sumbit", type="primary"):
    if start != None and end != None:
        st.write("Choosen interval is from ", start, " to ", end)
    else:
        st.warning("Select dates.")