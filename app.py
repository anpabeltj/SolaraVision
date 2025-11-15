"""
SolaraVision - Main Application
Solar Energy Analysis and Optimization Dashboard
"""

import streamlit as st
from modules.data_loader import load_data
from modules.ui_components import render_header, render_sidebar_filters, apply_filters, render_footer
from views.summary_dashboard import render_summary_dashboard
from views.visualization import render_visualization_analysis
from views.data_overview import render_data_overview

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="SolaraVision",
    page_icon="☀",
    layout="wide",
)

# ========== MAIN APPLICATION ==========
def main():
    """Main application function"""
    # Render header
    render_header()
    
    # Load data
    with st.spinner("Loading data..."):
        generation_data, weather_data, merged_df = load_data()
    
    # Render sidebar and get filters
    selection, date_range, inverter_filter = render_sidebar_filters(merged_df)
    
    # Apply filters
    filtered_df = apply_filters(merged_df, date_range, inverter_filter)
    
    # Display warning if no data after filtering
    if len(filtered_df) == 0:
        st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
        return
    
    # Route to appropriate page
    if selection == "Summary Dashboard":
        render_summary_dashboard(filtered_df)
    elif selection == "Visualization & Analysis":
        render_visualization_analysis(filtered_df)
    elif selection == "Data Overview":
        render_data_overview(generation_data, weather_data, merged_df)
    
    # Render footer
    render_footer()

# ========== RUN APPLICATION ==========
if __name__ == "__main__":
    main()