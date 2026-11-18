
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="UAC System Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("UAC System Capacity & Care Load Analytics")
st.caption("Monitoring System Workload, Intake Pressure and Care Trends")

@st.cache_data
def load_data():
    data = pd.read_csv("UAC_KPI_Analysis.csv")
    data["Date"] = pd.to_datetime(data["Date"])
    return data.sort_values("Date")

df = load_data()

st.sidebar.header("Dashboard Filters")

start_date = st.sidebar.date_input(
    "Start Date", df["Date"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date", df["Date"].max().date()
)

if start_date > end_date:
    st.error("Start date must be before end date.")
    st.stop()

filtered_df = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
].copy()

if filtered_df.empty:
    st.warning("No records available for this date range.")
    st.stop()

st.subheader("System Load Overview")

total_load = filtered_df["Total_Children_Under_Care"].dropna()

latest_load = total_load.iloc[-1] if not total_load.empty else np.nan
average_load = total_load.mean() if not total_load.empty else np.nan
maximum_load = total_load.max() if not total_load.empty else np.nan
average_pressure = filtered_df["Net_Intake_Pressure"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Latest System Load", f"{latest_load:,.0f}" if pd.notna(latest_load) else "N/A")
col2.metric("Average System Load", f"{average_load:,.0f}" if pd.notna(average_load) else "N/A")
col3.metric("Maximum System Load", f"{maximum_load:,.0f}" if pd.notna(maximum_load) else "N/A")
col4.metric("Average Intake Pressure", f"{average_pressure:,.2f}" if pd.notna(average_pressure) else "N/A")

st.divider()

fig = px.line(
    filtered_df,
    x="Date",
    y="Total_Children_Under_Care",
    title="Daily Total System Load"
)

st.plotly_chart(fig, use_container_width=True)

comparison_df = filtered_df[
    ["Date", "CBP_Custody", "HHS_Care"]
].melt(
    id_vars="Date",
    var_name="Care_Category",
    value_name="Children"
)

fig2 = px.line(
    comparison_df,
    x="Date",
    y="Children",
    color="Care_Category",
    title="CBP Custody vs HHS Care"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Dataset Preview")
st.dataframe(filtered_df, use_container_width=True)

st.success("System Load Overview generated successfully!")
