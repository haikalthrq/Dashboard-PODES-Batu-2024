"""
Data loader module for Podes 2024 dashboard
Handles data loading, caching, and basic preprocessing
"""

import json
import pandas as pd
import streamlit as st
from typing import Dict, List, Any


@st.cache_data
def load_podes_data() -> pd.DataFrame:
    """
    Load and cache Podes 2024 data from JSON file
    
    Returns:
        pd.DataFrame: Cleaned and processed Podes data
    """
    try:
        with open('data/data_podes_2024.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Ensure numeric columns are properly typed
        numeric_columns = [
            'jumlah_tk', 'jumlah_sd', 'jumlah_smp', 'jumlah_sma',
            'jumlah_rs', 'jumlah_puskesmas_inap', 'jumlah_puskesmas'
        ]
        
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    
    except FileNotFoundError:
        st.error("File data/data_podes_2024.json tidak ditemukan!")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()


def get_category_indicators() -> Dict[str, Dict[str, str]]:
    """
    Define indicator mapping for each category
    
    Returns:
        Dict: Mapping of categories to their indicators
    """
    return {
        "Pendidikan": {
            "jumlah_tk": "Jumlah TK",
            "jumlah_sd": "Jumlah SD", 
            "jumlah_smp": "Jumlah SMP",
            "jumlah_sma": "Jumlah SMA"
        },
        "Kesehatan": {
            "jumlah_rs": "Jumlah Rumah Sakit",
            "jumlah_puskesmas_inap": "Jumlah Puskesmas Rawat Inap",
            "jumlah_puskesmas": "Jumlah Puskesmas"
        },
        "Bencana & Lingkungan": {
            "label_mitigasi_dini": "Sistem Peringatan Dini",
            "label_mitigasi_alat": "Alat Keselamatan",
            "label_mitigasi_rambu": "Rambu Keselamatan"
        },
        "Ekonomi & Konektivitas": {
            "label_sinyal_internet": "Kualitas Sinyal Internet",
            "label_angkutan_umum": "Ketersediaan Angkutan Umum"
        }
    }


def get_kecamatan_list(df: pd.DataFrame) -> List[str]:
    """
    Get list of unique kecamatan from the data
    
    Args:
        df: DataFrame containing Podes data
        
    Returns:
        List[str]: List of kecamatan names
    """
    if df.empty:
        return []
    
    kecamatan_list = ["Semua Kecamatan"] + sorted(df['NAMA_KEC'].unique().tolist())
    return kecamatan_list


def get_desa_list(df: pd.DataFrame, selected_kecamatan: str) -> List[str]:
    """
    Get list of desa based on selected kecamatan
    
    Args:
        df: DataFrame containing Podes data
        selected_kecamatan: Selected kecamatan name
        
    Returns:
        List[str]: List of desa names
    """
    if df.empty:
        return []
    
    if selected_kecamatan == "Semua Kecamatan":
        return sorted(df['NAMA_DESA'].unique().tolist())
    else:
        filtered_df = df[df['NAMA_KEC'] == selected_kecamatan]
        return sorted(filtered_df['NAMA_DESA'].unique().tolist())


def filter_data(df: pd.DataFrame, 
                selected_kecamatan: str, 
                selected_desa: List[str],
                selected_indicators: List[str]) -> pd.DataFrame:
    """
    Filter data based on location and indicator selections
    
    Args:
        df: DataFrame containing Podes data
        selected_kecamatan: Selected kecamatan
        selected_desa: List of selected desa
        selected_indicators: List of selected indicator columns
        
    Returns:
        pd.DataFrame: Filtered data
    """
    if df.empty:
        return df
    
    filtered_df = df.copy()
    
    # Filter by kecamatan
    if selected_kecamatan != "Semua Kecamatan":
        filtered_df = filtered_df[filtered_df['NAMA_KEC'] == selected_kecamatan]
    
    # Filter by desa
    if selected_desa:
        filtered_df = filtered_df[filtered_df['NAMA_DESA'].isin(selected_desa)]
    
    # Select relevant columns
    base_columns = ['IDDESA', 'NAMA_KEC', 'NAMA_DESA']
    columns_to_show = base_columns + selected_indicators
    
    # Ensure all columns exist in the dataframe
    existing_columns = [col for col in columns_to_show if col in filtered_df.columns]
    
    return filtered_df[existing_columns]
