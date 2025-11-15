"""
Data Loading Module
Handles loading and preprocessing of solar generation and weather data
"""

import streamlit as st
import pandas as pd
import numpy as np


@st.cache_data
def load_data():
    """
    Load and preprocess solar generation and weather data
    
    Returns:
        tuple: (generation_data, weather_data, merged_df)
    """
    # Load CSV files
    generation_data = pd.read_csv('data/Plant_1_Generation_Data.csv')
    weather_data = pd.read_csv('data/Plant_1_Weather_Sensor_Data.csv')

    # Convert datetime columns
    generation_data['DATE_TIME'] = pd.to_datetime(
        generation_data['DATE_TIME'], 
        format='%d-%m-%Y %H:%M'
    )
    weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'])
    
    # Feature engineering for generation data
    generation_data['HOUR'] = generation_data['DATE_TIME'].dt.hour
    generation_data['DATE'] = generation_data['DATE_TIME'].dt.date
    generation_data['DAY'] = generation_data['DATE_TIME'].dt.day
    generation_data['MONTH'] = generation_data['DATE_TIME'].dt.month
    generation_data['MONTH_NAME'] = generation_data['DATE_TIME'].dt.strftime('%B')
    generation_data['DAY_OF_WEEK'] = generation_data['DATE_TIME'].dt.day_name()

    # Calculate efficiency metric
    generation_data['EFFICIENCY'] = np.where(
        generation_data['DC_POWER'] > 0,
        (generation_data['AC_POWER'] / generation_data['DC_POWER']) * 100,
        0
    )

    # Merge generation and weather datasets
    merged_df = pd.merge(
        generation_data,
        weather_data[[
            'DATE_TIME', 
            'PLANT_ID', 
            'AMBIENT_TEMPERATURE', 
            'MODULE_TEMPERATURE', 
            'IRRADIATION'
        ]],
        on=['DATE_TIME', 'PLANT_ID'],
        how='left'
    )

    return generation_data, weather_data, merged_df