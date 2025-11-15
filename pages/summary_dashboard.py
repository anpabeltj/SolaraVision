"""
Summary Dashboard Module
Renders the summary dashboard with KPIs and quick insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from modules.kpi_calculator import calculate_kpis
from modules.export_utils import export_dataframe_to_csv
from modules.ui_components import render_kpi_card


def render_summary_dashboard(filtered_df):
    """
    Render the summary dashboard with comprehensive KPIs
    
    Args:
        filtered_df (pd.DataFrame): Filtered solar data
    """
    st.header("📊 Summary Dashboard")
    st.markdown("### Key Performance Indicators")
    
    # Calculate KPIs
    kpis = calculate_kpis(filtered_df)
    
    # Row 1: Energy Generation KPIs
    st.subheader("⚡ Energy Generation")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_kpi_card("Total Energy Generated", f"{kpis['total_energy']:,.2f} kWh", icon="⚡")
    with col2:
        render_kpi_card("Daily Avg Energy", f"{kpis['daily_avg_energy']:,.2f} kWh", icon="📅")
    with col3:
        render_kpi_card("Peak Power Time", f"{int(kpis['peak_power_time'])}:00", icon="🕐")
    with col4:
        render_kpi_card("Analysis Period", f"{kpis['total_days']} days", icon="📆")
    
    st.markdown("---")
    
    # Row 2: Efficiency KPIs
    st.subheader("♻️ System Efficiency")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_kpi_card("Average Efficiency", f"{kpis['avg_efficiency']:.2f}%", icon="♻️")
    with col2:
        render_kpi_card("Maximum Efficiency", f"{kpis['max_efficiency']:.2f}%", icon="⬆️")
    with col3:
        render_kpi_card("Minimum Efficiency", f"{kpis['min_efficiency']:.2f}%", icon="⬇️")
    with col4:
        render_kpi_card("Active Inverters", f"{kpis['total_inverters']}", icon="🔌")
    
    st.markdown("---")
    
    # Row 3: Temperature KPIs
    st.subheader("🌡️ Temperature Analysis")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_kpi_card("Avg Module Temp", f"{kpis['avg_module_temp']:.2f}°C", icon="🌡️")
    with col2:
        render_kpi_card("Max Module Temp", f"{kpis['max_module_temp']:.2f}°C", icon="🔥")
    with col3:
        render_kpi_card("Min Module Temp", f"{kpis['min_module_temp']:.2f}°C", icon="❄️")
    with col4:
        render_kpi_card("Avg Ambient Temp", f"{kpis['avg_ambient_temp']:.2f}°C", icon="🌤️")
    
    st.markdown("---")
    
    # Row 4: Irradiation KPIs
    st.subheader("☀️ Irradiation Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        render_kpi_card("Maximum Irradiance", f"{kpis['max_irradiance']:.2f} W/m²", icon="☀️")
    with col2:
        render_kpi_card("Average Irradiance", f"{kpis['avg_irradiance']:.2f} W/m²", icon="🌅")
    
    st.markdown("---")
    
    # Quick Insights Section
    _render_quick_insights(filtered_df)
    
    # Export Section
    st.markdown("---")
    _render_export_section(filtered_df, kpis)


def _render_quick_insights(filtered_df):
    """
    Render quick insights charts
    
    Args:
        filtered_df (pd.DataFrame): Filtered solar data
    """
    st.subheader("💡 Quick Insights")
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily generation chart
        daily_gen = filtered_df.groupby('DATE', as_index=False)['AC_POWER'].sum()
        fig_daily_mini = px.line(
            daily_gen,
            x='DATE',
            y='AC_POWER',
            title="Daily Energy Generation Trend",
            labels={'AC_POWER': 'AC Power (kWh)', 'DATE': 'Date'}
        )
        fig_daily_mini.update_layout(height=300)
        st.plotly_chart(fig_daily_mini, use_container_width=True)
        
    with col2:
        # Efficiency distribution
        fig_eff_dist = px.histogram(
            filtered_df,
            x='EFFICIENCY',
            title="Efficiency Distribution",
            labels={'EFFICIENCY': 'Efficiency (%)'},
            nbins=30
        )
        fig_eff_dist.update_layout(height=300)
        st.plotly_chart(fig_eff_dist, use_container_width=True)


def _render_export_section(filtered_df, kpis):
    """
    Render export section for downloading data
    
    Args:
        filtered_df (pd.DataFrame): Filtered solar data
        kpis (dict): Calculated KPIs
    """
    st.subheader("📥 Export Summary Data")
    col1, col2 = st.columns(2)
    
    with col1:
        # Export KPIs to CSV
        kpi_df = pd.DataFrame(list(kpis.items()), columns=['Metric', 'Value'])
        csv_kpi = export_dataframe_to_csv(kpi_df, "summary_kpis.csv")
        st.download_button(
            label="📊 Download KPIs (CSV)",
            data=csv_kpi,
            file_name=f"summary_kpis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Export daily summary
        daily_summary = filtered_df.groupby('DATE').agg({
            'AC_POWER': 'sum',
            'EFFICIENCY': 'mean',
            'MODULE_TEMPERATURE': 'mean',
            'IRRADIATION': 'mean'
        }).reset_index()
        csv_daily = export_dataframe_to_csv(daily_summary, "daily_summary.csv")
        st.download_button(
            label="📅 Download Daily Summary (CSV)",
            data=csv_daily,
            file_name=f"daily_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )