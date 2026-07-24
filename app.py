import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="6G Agricultural IoT Engine", layout="wide")

st.title("Serverless 6G Food Safety Pipeline")
st.caption("Ultra-Low Latency Telemetry Ingestion & Dynamic Resource Management")

st.sidebar.header("Network Configuration")
selected_network = st.sidebar.selectbox("Active Protocol", ["6G Ultra-Reliable Low-Latency (URLLC)", "5G Legacy Baseline"])
anomaly_trigger = st.sidebar.slider("Simulate Biological Anomaly (Cold-Chain Breach)", 1, 10, 5)
run_simulation = st.sidebar.button("Initialize 6G Telemetry Engine")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: Massive IoT Sensors -> Edge Resource Triage -> AWS Core")

if run_simulation:
    st.subheader(f"Active Monitoring Protocol: {selected_network}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_velocity = col1.empty()
    metric_latency = col2.empty()
    metric_temp = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(1616)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    network_latency = []
    sensor_temp = []
    
    base_latency = 0.5 if "6G" in selected_network else 15.0
    base_temp = 4.0 
    
    for i in range(100):
        velocity = int(np.random.uniform(80000, 120000)) if "6G" in selected_network else int(np.random.uniform(10000, 20000))
        
        if i < 35:
            current_temp = base_temp + np.random.uniform(-0.5, 0.5)
            current_lat = base_latency + np.random.uniform(-0.1, 0.2) if "6G" in selected_network else base_latency + np.random.uniform(-2.0, 5.0)
            status = "STABLE"
        elif i >= 35 and i < 60:
            current_temp = base_temp + (i - 35) * (0.8 * anomaly_trigger) + np.random.uniform(-1.0, 1.0)
            current_lat = base_latency + np.random.uniform(0.1, 0.3) if "6G" in selected_network else base_latency + 25.0 + np.random.uniform(-5.0, 10.0)
            status = "BREACH DETECTED"
        else:
            current_temp = current_temp + np.random.uniform(-1.0, 1.0)
            current_lat = base_latency + np.random.uniform(0.0, 0.2) if "6G" in selected_network else base_latency + 10.0 + np.random.uniform(-2.0, 5.0)
            status = "ISOLATION PROTOCOL ACTIVE"
            
        network_latency.append(current_lat)
        sensor_temp.append(current_temp)
        
        metric_velocity.metric("Telemetry Velocity", f"{velocity:,} Nodes/s")
        metric_latency.metric("Edge-to-Cloud Latency", f"{current_lat:.2f} ms")
        metric_temp.metric("Cold-Chain Temperature", f"{current_temp:.1f} °C", f"{(current_temp - base_temp):.1f} °C")
        
        if status == "BREACH DETECTED":
            metric_status.metric("Resource Management", "PRIORITY UPLINK", "Anomaly")
        elif status == "ISOLATION PROTOCOL ACTIVE":
            metric_status.metric("Resource Management", "ACTUATORS DEPLOYED", "Secured")
        else:
            metric_status.metric("Resource Management", "BACKGROUND BATCHING", "Normal")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=sensor_temp, mode='lines', name='Biological Sensor Temp (°C)', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=network_latency, mode='lines', name='Ingestion Latency (ms)', yaxis='y2', line=dict(color='blue', dash='dot')))
        
        fig.update_layout(
            title="6G Agricultural Telemetry: Food Safety Monitoring vs Cloud Ingestion Latency",
            xaxis=dict(title="High-Frequency Stream Timestamp"),
            yaxis=dict(title="Temperature (°C)"),
            yaxis2=dict(title="Latency (ms)", overlaying='y', side='right', range=[0, 50]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if status == "BREACH DETECTED" and i == 35:
            log_placeholder.error(f"FOOD SAFETY ALERT: Critical cold-chain failure detected at {time_steps[i].strftime('%H:%M:%S')}. Edge node dynamically elevating compute priority. Sub-millisecond AWS payload executed.")
        elif status == "ISOLATION PROTOCOL ACTIVE" and i == 60:
            log_placeholder.success(f"ORCHESTRATION SUCCESS: 6G network maintained ultra-low latency during anomaly spike. Contaminated batch autonomously isolated.")
        elif status == "STABLE" and i % 5 == 0:
            log_placeholder.info(f"Log: Telemetry tick {i} ingested. Edge resource manager actively batching redundant data to preserve 6G bandwidth.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The serverless 6G pipeline successfully prioritized and processed critical food safety anomalies with ultra-low latency.")
else:
    st.info("Click 'Initialize 6G Telemetry Engine' in the sidebar to simulate high-velocity agricultural data ingestion.")