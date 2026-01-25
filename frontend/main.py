import streamlit as st
import pandas as pd
import plotly
from backend import api
import requests
import datetime

st.set_page_config(page_title="System Metrics", layout="wide")

REFRESH_OPTIONS = {
    "5s": 5,
    "10s": 10,
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
        response = requests.get("http://localhost:8000/metrics")
        response.raise_for_status() 
        df = pd.DataFrame([response.json()])
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()

# main ui
@st.fragment(run_every=freq_ms)
def metrics():
    st.header("Current system metrics:")
    # refresh metrics every 5 seconds
    df = get_metrics()
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        latest = df.iloc[0] 

        col1.metric(label="CPU", value=f"{latest['cpu_usage']}%")
        col2.metric(label="Memory", value=f"{latest['memory_usage']}%")
        col3.metric(label="Load Average", value=f"{latest['load_average']}%")
        col4.metric(label="Network Bandwidth", value=f"{latest['network_bandwidth']}Mb/s")
        d1, = st.columns(1)
        time_string = latest['datetime'].strftime("%H:%M:%S")
        d1.metric(label="Measured at", value=time_string)
        st.dataframe(df, width="stretch", hide_index=True, 
            column_config={ 
                    "datetime":
                    st.column_config.DatetimeColumn(
                        "Time",
                        format="DD-MM-YYYY, HH:mm:ss",
                    ),
                    "cpu_usage": 
                    st.column_config.ProgressColumn(
                        "CPU Load",
                        help="System CPU usage percentage",
                        format="%f%%",
                        min_value=0,
                        max_value=100,
                        color="orange"
                    ),
                    "memory_usage": st.column_config.ProgressColumn(
                        "RAM Usage",
                        format="%f%%",
                        min_value=0,
                        max_value=100,
                        color="yellow"
                    ),
                    "load_average": st.column_config.ProgressColumn(
                        "Load Average",
                        help="Load average over last 1 minute",
                        format="%f%%",
                        min_value=0,
                        max_value=100,
                    ),
                    "network_bandwidth": st.column_config.NumberColumn(
                        "Network Bandwidth",
                        format="%f MBps",
                    )
        })
    else:
        st.warning("No data available. Check if the backend is running.")
metrics()

st.divider()
left_col, right_col = st.columns(2)
with left_col:  
    start = st.datetime_input("Choose start", value=None, format="DD/MM/YYYY")
with right_col:
    end = st.datetime_input("Choose end", value=None, format="DD/MM/YYYY")
if start != None and end != None:
    st.write("Choosen interval is from ", start, " to ", end)