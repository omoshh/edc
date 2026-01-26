import streamlit as st
import pandas as pd
import requests
import datetime

st.set_page_config(page_title="System Metrics", layout="wide")

if "df_metrics" not in st.session_state:
    st.session_state.df_metrics = None

REFRESH_OPTIONS = {
    "30s": 30,
    "1m": 60
}
METRICS = {
    "CPU (%)": "cpu_usage",
    "RAM (%)": "ram_usage",
    "Load Average": "load_average",
    "Bandwidth (Mb/s)": "network_bandwidth"
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
@st.cache_data(ttl=300)
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

# request from range
def get_metrics_in_range(start, end):
    par = {
        "start": str(start),
        "end": str(end)
    }
    try:
        response = requests.get(st.secrets["API_RANGE"], params=par)
        response.raise_for_status()
        json_data = response.json().get("data", [])
        if not json_data:
            return pd.DataFrame()
        data = pd.DataFrame(json_data)
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        return data
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()
    
# ui
st.divider()
st.header("Request metrics from a time interval:")
left_col, right_col = st.columns(2)
with left_col:  
    today_midnight = datetime.datetime.now(datetime.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start = st.datetime_input("Choose start", value=today_midnight, format="DD/MM/YYYY", max_value="now")
with right_col:
    end = st.datetime_input("Choose end", value="now", format="DD/MM/YYYY", max_value="now")

if st.button("Submit", type="primary"):
    if start and end:
        with st.spinner("Fetching data..."):
            st.session_state.df_metrics = get_metrics_in_range(start, end)
    else:
        st.warning("Select dates.")

if st.session_state.df_metrics is not None and not st.session_state.df_metrics.empty:
    data = st.session_state.df_metrics
    chart_data = data.set_index('timestamp')
    
    options = list(METRICS.keys())
    selected_labels = st.multiselect("Metrics", options=options, default=options)
    selected_columns = [METRICS[label] for label in selected_labels]

    if selected_columns:
        filtered_data = chart_data[selected_columns]
        # display metric names instead of db column names
        reverse_metrics = {v: k for k, v in METRICS.items()}
        renamed_data = filtered_data.rename(columns=reverse_metrics)
        tab1, tab2 = st.tabs(["Chart", "Dataframe"])
        with tab1:
            st.line_chart(renamed_data, height=300)
        with tab2:
            st.dataframe(renamed_data, use_container_width=True)
    else:
        st.info("Select metrics to visualize.")