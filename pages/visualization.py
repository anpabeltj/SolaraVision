"""
Visualization Module
Renders interactive visualizations and analysis charts
"""

import streamlit as st
import plotly.express as px
from datetime import datetime
from modules.export_utils import export_dataframe_to_csv


def render_visualization_analysis(filtered_df):
    """
    Render the visualization and analysis page with interactive charts
    
    Args:
        filtered_df (pd.DataFrame): Filtered solar data
    """
    st.header("🌞 Interactive Visualization & Analysis")
    st.markdown("Explore daily and seasonal power generation trends, weather relationships, and inverter-level performance.")

    # Render each visualization section
    _render_daily_trend(filtered_df)
    _render_hourly_pattern(filtered_df)
    _render_monthly_trend(filtered_df)
    _render_weather_analysis(filtered_df)
    _render_inverter_performance(filtered_df)
    _render_efficiency_analysis(filtered_df)


def _render_daily_trend(filtered_df):
    """Render daily power generation trend"""
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
    
    # Export button
    col1, col2 = st.columns([3, 1])
    with col2:
        csv_daily = export_dataframe_to_csv(daily_gen)
        st.download_button(
            label="📥 Export Data (CSV)",
            data=csv_daily,
            file_name=f"daily_generation_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="daily_csv"
        )
    
    st.markdown("---")


def _render_hourly_pattern(filtered_df):
    """Render average hourly power generation pattern"""
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
    
    # Export button
    col1, col2 = st.columns([3, 1])
    with col2:
        csv_hourly = export_dataframe_to_csv(hourly_pattern)
        st.download_button(
            label="📥 Export Data (CSV)",
            data=csv_hourly,
            file_name=f"hourly_pattern_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="hourly_csv"
        )
    
    st.markdown("---")


def _render_monthly_trend(filtered_df):
    """Render monthly power generation trend"""
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
    
    # Export button
    col1, col2 = st.columns([3, 1])
    with col2:
        csv_monthly = export_dataframe_to_csv(monthly_gen)
        st.download_button(
            label="📥 Export Data (CSV)",
            data=csv_monthly,
            file_name=f"monthly_generation_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="monthly_csv"
        )
    
    st.markdown("---")


def _render_weather_analysis(filtered_df):
    """Render weather vs power analysis"""
    st.subheader("🌡️ Relationship Between Weather and Power Output")
    
    # Sample data for better performance
    sample_df = filtered_df.sample(n=min(5000, len(filtered_df)), random_state=42)
    fig_weather = px.scatter(
        sample_df,
        x='IRRADIATION',
        y='AC_POWER',
        color='MODULE_TEMPERATURE',
        title="Irradiation vs AC Power (Color = Module Temperature)",
        labels={
            'IRRADIATION': 'Irradiation (W/m²)', 
            'AC_POWER': 'AC Power (kW)', 
            'MODULE_TEMPERATURE': 'Module Temp (°C)'
        },
        trendline="ols"
    )
    st.plotly_chart(fig_weather, use_container_width=True)
    
    # Export button
    col1, col2 = st.columns([3, 1])
    with col2:
        weather_export = filtered_df[['IRRADIATION', 'AC_POWER', 'MODULE_TEMPERATURE']].dropna()
        csv_weather = export_dataframe_to_csv(weather_export)
        st.download_button(
            label="📥 Export Data (CSV)",
            data=csv_weather,
            file_name=f"weather_vs_power_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="weather_csv"
        )
    
    st.markdown("---")


def _render_inverter_performance(filtered_df):
    """Render inverter-level performance comparison"""
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
    
    # Export button
    col1, col2 = st.columns([3, 1])
    with col2:
        csv_inverter = export_dataframe_to_csv(inverter_perf)
        st.download_button(
            label="📥 Export Data (CSV)",
            data=csv_inverter,
            file_name=f"inverter_performance_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="inverter_csv"
        )
    
    st.markdown("---")


def _render_efficiency_analysis(filtered_df):
    """Render efficiency vs temperature analysis"""
    st.subheader("♻️ Efficiency vs Module Temperature")
    
    # Sample data for better performance
    sample_eff_df = filtered_df.sample(n=min(5000, len(filtered_df)), random_state=42)
    fig_efficiency = px.scatter(
        sample_eff_df,
        x='MODULE_TEMPERATURE',
        y='EFFICIENCY',
        color='IRRADIATION',
        title="Efficiency vs Module Temperature (Color = Irradiation)",
        labels={
            'MODULE_TEMPERATURE': 'Module Temp (°C)', 
            'EFFICIENCY': 'Efficiency (%)', 
            'IRRADIATION': 'Irradiation (W/m²)'
        },
        trendline="ols"
    )
    st.plotly_chart(fig_efficiency, use_container_width=True)
    
    # Export button
    col1, col2 = st.columns([3, 1])
    with col2:
        efficiency_export = filtered_df[['MODULE_TEMPERATURE', 'EFFICIENCY', 'IRRADIATION']].dropna()
        csv_efficiency = export_dataframe_to_csv(efficiency_export)
        st.download_button(
            label="📥 Export Data (CSV)",
            data=csv_efficiency,
            file_name=f"efficiency_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="efficiency_csv"
        )