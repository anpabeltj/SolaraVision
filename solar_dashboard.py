import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="SolaraVision",
    layout="wide",
)

# Title
st.title("Solar Energy Analysis and Optimization Dashboard")
st.markdown("""
<div style='text-align: left; color: #666; padding: 1rem;'>
    <p><b>Team Members :</b></p>
    <p>1. Muhammad Naufal Alif Islami - 22008960</p>
    <p>2. Anpabelt Trah Javala - 24000761</p>
    <p>3. Muhammad Hafizuddin Bin Norraihizulkfli - 21001216</p>
</div>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    generation_data = pd.read_csv('Plant_1_Generation_Data.csv')
    weather_data = pd.read_csv('Plant_1_Weather_Sensor_Data.csv')

    # Convert datetime
    generation_data['DATE_TIME'] = pd.to_datetime(generation_data['DATE_TIME'], format='%d-%m-%Y %H:%M')
    weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'])
    
    # Feature engineering
    generation_data['HOUR'] = generation_data['DATE_TIME'].dt.hour
    generation_data['DATE'] = generation_data['DATE_TIME'].dt.date
    generation_data['DAY'] = generation_data['DATE_TIME'].dt.day
    generation_data['MONTH'] = generation_data['DATE_TIME'].dt.month
    generation_data['MONTH_NAME'] = generation_data['DATE_TIME'].dt.strftime('%B')
    generation_data['DAY_OF_WEEK'] = generation_data['DATE_TIME'].dt.day_name()

    # Calculate efficiency
    generation_data['EFFICIENCY'] = np.where(
        generation_data['DC_POWER'] > 0,
        (generation_data['AC_POWER'] / generation_data['DC_POWER']) * 100,
        0
    )

    # Merge datasets
    merged_df = pd.merge(
        generation_data,
        weather_data[['DATE_TIME', 'PLANT_ID', 'AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION']],
        on=['DATE_TIME', 'PLANT_ID'],
        how='left'
    )

    return generation_data, weather_data, merged_df

# Load data
generation_data, weather_data, merged_df = load_data()

st.sidebar.title("Navigation")
selection = st.sidebar.selectbox("Go to", [
    "Summary Dashboard",
    "Visualization & Analysis",
    "Data Overview"
])


if selection == "Data Overview":
    tab1, tab2 = st.tabs(["Data Overview", "Merged Data"])
    with tab1:
        st.header("Data Overview")
    
        col1, col2 = st.columns(2)
    
        with col1:
            st.subheader("Generation Data")
            st.metric("Total Records", f"{len(generation_data):,}")
            st.metric("Number of Inverters", generation_data['SOURCE_KEY'].nunique())
            st.metric("Columns", len(generation_data.columns))

            st.write("**Column Information:**")
            col_info = generation_data.columns
            st.write(col_info)
        
            st.write("**Sample Data:**")
            st.write(generation_data)
    
        with col2:
            st.subheader("Weather Data")
            st.metric("Total Records", f"{len(weather_data):,}")
            st.metric("Weather Sensors", weather_data['SOURCE_KEY'].nunique())
            st.metric("Columns", len(weather_data.columns))

            st.write("**Column Information:**")
            col_info_weather = weather_data.columns
            st.write(col_info_weather)

            st.write("**Sample Data:**")
            st.write(weather_data)
    
        st.markdown("---")
        st.subheader("Date Range")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Start Date", str(generation_data['DATE_TIME'].min().date()))
        with col2:
            st.metric("End Date", str(generation_data['DATE_TIME'].max().date()))
        with col3:
            days = (generation_data['DATE_TIME'].max() - generation_data['DATE_TIME'].min()).days
            st.metric("Duration", f"{days} days")

    with tab2:
        st.header("Merged Data")
    
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Generation Records", f"{len(generation_data):,}")
        with col2:
            st.metric("Weather Records", f"{len(weather_data):,}")
        with col3:
            st.metric("Merged Records", f"{len(merged_df):,}")
    
        st.write("**Sample of Merged Data:**")
        st.write(merged_df)

if selection == "Summary Dashboard":
    st.header("Dashboard")
    
if selection == "Visualization & Analysis":
    st.header("🌞 Interactive Visualization & Analysis")
    st.markdown("Explore daily and seasonal power generation trends, weather relationships, and inverter-level performance.")

    # --- Sidebar Filters ---
    st.sidebar.subheader("📅 Filter Controls")
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [merged_df['DATE_TIME'].min().date(), merged_df['DATE_TIME'].max().date()]
    )
    inverter_filter = st.sidebar.multiselect(
        "Select Inverter (SOURCE_KEY)",
        options=merged_df['SOURCE_KEY'].unique(),
        default=merged_df['SOURCE_KEY'].unique()
    )

    # Apply filters
    filtered_df = merged_df[
        (merged_df['DATE_TIME'].dt.date >= date_range[0]) &
        (merged_df['DATE_TIME'].dt.date <= date_range[1]) &
        (merged_df['SOURCE_KEY'].isin(inverter_filter))
    ]

    # --- Daily Trend Visualization ---
    st.subheader("☀️ Daily Power Generation Trend")
    daily_gen = filtered_df.groupby('DATE', as_index=False)['AC_POWER'].sum()
    fig_daily = px.line(
        daily_gen,
        x='DATE',
        y='AC_POWER',
        title="Daily AC Power Generation",
        labels={'AC_POWER': 'Total AC Power (kW)', 'DATE': 'Date'},
        markers=True
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    # --- Hourly Pattern (Average by Hour) ---
    st.subheader("🕒 Average Hourly Power Generation Pattern")
    hourly_pattern = filtered_df.groupby('HOUR', as_index=False)['AC_POWER'].mean()
    fig_hourly = px.line(
        hourly_pattern,
        x='HOUR',
        y='AC_POWER',
        title="Average Hourly AC Power Generation",
        labels={'AC_POWER': 'Average AC Power (kW)', 'HOUR': 'Hour of Day'},
        markers=True
    )
    st.plotly_chart(fig_hourly, use_container_width=True)

    # --- Seasonal Trend ---
    st.subheader("🌤️ Monthly Power Generation Trend")
    monthly_gen = filtered_df.groupby('MONTH_NAME', as_index=False)['AC_POWER'].sum()
    fig_month = px.bar(
        monthly_gen,
        x='MONTH_NAME',
        y='AC_POWER',
        title="Monthly AC Power Generation",
        labels={'AC_POWER': 'Total AC Power (kW)', 'MONTH_NAME': 'Month'},
    )
    st.plotly_chart(fig_month, use_container_width=True)

    # --- Weather vs Power ---
    st.subheader("🌡️ Relationship Between Weather and Power Output")
    fig_weather = px.scatter(
        filtered_df,
        x='IRRADIATION',
        y='AC_POWER',
        color='MODULE_TEMPERATURE',
        title="Irradiation vs AC Power (Color = Module Temperature)",
        labels={'IRRADIATION': 'Irradiation (W/m²)', 'AC_POWER': 'AC Power (kW)', 'MODULE_TEMPERATURE': 'Module Temp (°C)'},
        trendline="ols"
    )
    st.plotly_chart(fig_weather, use_container_width=True)

    # --- Inverter-level Comparison ---
    st.subheader("⚡ Inverter-level Performance")
    inverter_perf = filtered_df.groupby('SOURCE_KEY', as_index=False)['AC_POWER'].sum()
    fig_inverter = px.bar(
        inverter_perf,
        x='SOURCE_KEY',
        y='AC_POWER',
        title="Total AC Power by Inverter",
        labels={'SOURCE_KEY': 'Inverter ID', 'AC_POWER': 'Total AC Power (kW)'},
    )
    st.plotly_chart(fig_inverter, use_container_width=True)

    # --- Efficiency vs Temperature ---
    st.subheader("♻️ Efficiency vs Module Temperature")
    fig_efficiency = px.scatter(
        filtered_df,
        x='MODULE_TEMPERATURE',
        y='EFFICIENCY',
        color='IRRADIATION',
        title="Efficiency vs Module Temperature (Color = Irradiation)",
        labels={'MODULE_TEMPERATURE': 'Module Temp (°C)', 'EFFICIENCY': 'Efficiency (%)', 'IRRADIATION': 'Irradiation (W/m²)'},
        trendline="ols"
    )
    st.plotly_chart(fig_efficiency, use_container_width=True)


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p><b>SolaraVision - 2025</b></p>
</div>
""", unsafe_allow_html=True)
