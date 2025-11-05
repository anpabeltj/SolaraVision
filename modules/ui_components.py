"""
UI Components Module
Reusable UI components for the dashboard
"""

import streamlit as st


def render_header():
    """Render the application header with title and team information"""
    st.title("☀️ SolaraVision - Solar Energy Analysis Dashboard")
    st.markdown("""
    <div style='text-align: left; color: #666; padding: 1rem; background-color: #f0f2f6; border-radius: 10px;'>
        <p><b>Team Members:</b></p>
        <p>1. Muhammad Naufal Alif Islami - 22008960</p>
        <p>2. Anpabelt Trah Javala - 24000761</p>
        <p>3. Muhammad Hafizuddin Bin Norraihizulkfli - 21001216</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")


def render_kpi_card(label, value, delta=None, icon="📊"):
    """
    Render a KPI metric card
    
    Args:
        label (str): Label for the metric
        value: Value to display
        delta: Optional delta value to show change
        icon (str): Icon to display with the label
    """
    st.metric(label=f"{icon} {label}", value=value, delta=delta)


def render_sidebar_filters(merged_df):
    """
    Render sidebar filters and navigation
    
    Args:
        merged_df (pd.DataFrame): Merged dataframe for filter options
        
    Returns:
        tuple: (selection, date_range, inverter_filter)
    """
    st.sidebar.title("🎛️ Navigation & Filters")
    
    # Navigation selection
    selection = st.sidebar.selectbox("Go to", [
        "Summary Dashboard",
        "Visualization & Analysis",
        "Data Overview"
    ])
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Filter Controls")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [merged_df['DATE_TIME'].min().date(), merged_df['DATE_TIME'].max().date()]
    )
    
    # Inverter filter
    inverter_filter = st.sidebar.multiselect(
        "Select Inverter (SOURCE_KEY)",
        options=merged_df['SOURCE_KEY'].unique(),
        default=merged_df['SOURCE_KEY'].unique()
    )
    
    return selection, date_range, inverter_filter


def apply_filters(df, date_range, inverter_filter):
    """
    Apply filters to the dataframe
    
    Args:
        df (pd.DataFrame): Dataframe to filter
        date_range (tuple): Start and end dates
        inverter_filter (list): List of inverter IDs to include
        
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    filtered_df = df[
        (df['DATE_TIME'].dt.date >= date_range[0]) &
        (df['DATE_TIME'].dt.date <= date_range[1]) &
        (df['SOURCE_KEY'].isin(inverter_filter))
    ]
    return filtered_df


def render_footer():
    """Render the application footer"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><b>SolaraVision - 2025</b></p>
        <p>Solar Energy Analysis and Optimization Dashboard</p>
    </div>
    """, unsafe_allow_html=True)