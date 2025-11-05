"""
KPI Calculator Module
Calculates key performance indicators from solar data
"""

import pandas as pd


def calculate_kpis(df):
    """
    Calculate key performance indicators from the dataframe
    
    Args:
        df (pd.DataFrame): Solar data dataframe
        
    Returns:
        dict: Dictionary containing all calculated KPIs
    """
    kpis = {
        # Energy Generation KPIs
        'total_energy': df['AC_POWER'].sum(),
        'daily_avg_energy': df.groupby('DATE')['AC_POWER'].sum().mean(),
        
        # Efficiency KPIs
        'avg_efficiency': df['EFFICIENCY'].mean(),
        'max_efficiency': df['EFFICIENCY'].max(),
        'min_efficiency': df['EFFICIENCY'].min(),
        
        # Temperature KPIs
        'avg_module_temp': df['MODULE_TEMPERATURE'].mean(),
        'max_module_temp': df['MODULE_TEMPERATURE'].max(),
        'min_module_temp': df['MODULE_TEMPERATURE'].min(),
        'avg_ambient_temp': df['AMBIENT_TEMPERATURE'].mean(),
        
        # Irradiation KPIs
        'max_irradiance': df['IRRADIATION'].max(),
        'avg_irradiance': df['IRRADIATION'].mean(),
        
        # System KPIs
        'total_inverters': df['SOURCE_KEY'].nunique(),
        'peak_power_time': df.loc[df['AC_POWER'].idxmax(), 'HOUR'] if len(df) > 0 else 0,
        'total_days': df['DATE'].nunique()
    }
    
    return kpis