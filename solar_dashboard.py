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
    st.header("Interactive Visualization")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p><b>SolaraVision - 2025</b></p>
</div>
""", unsafe_allow_html=True)