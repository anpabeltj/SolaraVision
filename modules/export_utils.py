"""
Export Utilities Module
Handles data export functionality for CSV and image formats
"""

import pandas as pd


def export_dataframe_to_csv(df, filename="data_export.csv"):
    """
    Convert dataframe to CSV format for download
    
    Args:
        df (pd.DataFrame): Dataframe to export
        filename (str): Default filename for the export
        
    Returns:
        bytes: CSV data encoded as bytes
    """
    return df.to_csv(index=False).encode('utf-8')


def export_figure_to_image(fig, filename="chart_export.png"):
    """
    Convert plotly figure to PNG image bytes
    
    Args:
        fig: Plotly figure object
        filename (str): Default filename for the export
        
    Returns:
        bytes: PNG image data as bytes
    """
    img_bytes = fig.to_image(format="png", width=1200, height=600)
    return img_bytes