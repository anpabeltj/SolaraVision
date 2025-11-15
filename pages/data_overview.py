"""
Data Overview Module
Renders data overview and exploration interface
"""

import streamlit as st
from datetime import datetime
from modules.export_utils import export_dataframe_to_csv


def render_data_overview(generation_data, weather_data, merged_df):
    """
    Render the data overview page with dataset information
    
    Args:
        generation_data (pd.DataFrame): Generation dataset
        weather_data (pd.DataFrame): Weather dataset
        merged_df (pd.DataFrame): Merged dataset
    """
    tab1, tab2 = st.tabs(["📋 Data Overview", "🔗 Merged Data"])
    
    with tab1:
        _render_dataset_overview(generation_data, weather_data)
    
    with tab2:
        _render_merged_data(generation_data, weather_data, merged_df)


def _render_dataset_overview(generation_data, weather_data):
    """
    Render overview of individual datasets
    
    Args:
        generation_data (pd.DataFrame): Generation dataset
        weather_data (pd.DataFrame): Weather dataset
    """
    st.header("📋 Data Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚡ Generation Data")
        st.metric("Total Records", f"{len(generation_data):,}")
        st.metric("Number of Inverters", generation_data['SOURCE_KEY'].nunique())
        st.metric("Columns", len(generation_data.columns))

        st.write("**Column Information:**")
        st.write(list(generation_data.columns))
    
        st.write("**Sample Data:**")
        st.dataframe(generation_data.head(100), use_container_width=True)
        
        # Export button
        csv_gen = export_dataframe_to_csv(generation_data)
        st.download_button(
            label="📥 Download Full Generation Data (CSV)",
            data=csv_gen,
            file_name=f"generation_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    with col2:
        st.subheader("🌤️ Weather Data")
        st.metric("Total Records", f"{len(weather_data):,}")
        st.metric("Weather Sensors", weather_data['SOURCE_KEY'].nunique())
        st.metric("Columns", len(weather_data.columns))

        st.write("**Column Information:**")
        st.write(list(weather_data.columns))

        st.write("**Sample Data:**")
        st.dataframe(weather_data.head(100), use_container_width=True)
        
        # Export button
        csv_weather = export_dataframe_to_csv(weather_data)
        st.download_button(
            label="📥 Download Full Weather Data (CSV)",
            data=csv_weather,
            file_name=f"weather_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    st.markdown("---")
    _render_date_range_info(generation_data)


def _render_date_range_info(generation_data):
    """
    Render date range information
    
    Args:
        generation_data (pd.DataFrame): Generation dataset
    """
    st.subheader("📅 Date Range Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Start Date", str(generation_data['DATE_TIME'].min().date()))
    with col2:
        st.metric("End Date", str(generation_data['DATE_TIME'].max().date()))
    with col3:
        days = (generation_data['DATE_TIME'].max() - generation_data['DATE_TIME'].min()).days
        st.metric("Duration", f"{days} days")


def _render_merged_data(generation_data, weather_data, merged_df):
    """
    Render merged dataset information
    
    Args:
        generation_data (pd.DataFrame): Generation dataset
        weather_data (pd.DataFrame): Weather dataset
        merged_df (pd.DataFrame): Merged dataset
    """
    st.header("🔗 Merged Data")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Generation Records", f"{len(generation_data):,}")
    with col2:
        st.metric("Weather Records", f"{len(weather_data):,}")
    with col3:
        st.metric("Merged Records", f"{len(merged_df):,}")

    st.write("**Sample of Merged Data:**")
    st.dataframe(merged_df.head(100), use_container_width=True)
    
    # Export button
    csv_merged = export_dataframe_to_csv(merged_df)
    st.download_button(
        label="📥 Download Merged Data (CSV)",
        data=csv_merged,
        file_name=f"merged_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )