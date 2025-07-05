import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="EV Fleet Battery Dashboard", layout="wide")

st.title("🔋 EV Fleet Battery Health Dashboard")
st.markdown("This dashboard shows a simulated fleet of electric vehicles over one year, analyzing battery health degradation using factors like usage, climate, and charging patterns.")

# Load data
summary_df = pd.read_csv("fleet_summary.csv")
daily_df = pd.read_csv("fleet_daily_data.csv")

# Sidebar filters
st.sidebar.header("📊 Filter Options")
selected_climate = st.sidebar.multiselect("Select Climate Zones", options=daily_df['climate'].unique(), default=daily_df['climate'].unique())
selected_charging = st.sidebar.multiselect("Charging Type", options=daily_df['charging'].unique(), default=daily_df['charging'].unique())

# Apply filters
filtered_df = daily_df[(daily_df['climate'].isin(selected_climate)) & (daily_df['charging'].isin(selected_charging))]

# Overview KPIs
avg_health = summary_df['battery_health'].mean()
critical_vehicles = summary_df[summary_df['health_status'] == '🔴 Critical'].shape[0]
healthy_vehicles = summary_df[summary_df['health_status'] == '🟢 Healthy'].shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("📉 Average Battery Health", f"{avg_health:.2f}%")
col2.metric("🚨 Critical Vehicles (<70%)", critical_vehicles)
col3.metric("✅ Healthy Vehicles (>85%)", healthy_vehicles)

# Line chart of average health over time
st.subheader("📈 Fleet Battery Health Over Time")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_df, x='day', y='battery_health', ci='sd', ax=ax)
ax.set_title("Average Battery Health Over Time")
ax.set_ylabel("Battery Health (%)")
st.pyplot(fig)

# Vehicle-wise status
st.subheader("🚗 Vehicle Health Status (Final Day)")
st.dataframe(summary_df.sort_values("battery_health"))

# Optional: download data
st.sidebar.download_button("📥 Download Daily Fleet Data", data=daily_df.to_csv(index=False), file_name="fleet_daily_data.csv")
st.sidebar.download_button("📥 Download Summary", data=summary_df.to_csv(index=False), file_name="fleet_summary.csv")
