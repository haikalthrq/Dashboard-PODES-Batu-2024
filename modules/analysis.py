"""
Analysis module for Podes 2024 dashboard
Handles data analysis, filtering, and comparison operations
"""

import pandas as pd
import streamlit as st
from typing import List, Dict, Tuple, Any


def get_updated_category_indicators() -> Dict[str, Dict[str, str]]:
    """
    Updated indicator mapping for the new category structure
    
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
            "jumlah_puskesmas": "Jumlah Puskesmas"
        },
        "Infrastruktur & Konektivitas": {
            "kekuatan_sinyal": "Kualitas Sinyal Internet",
            "jenis_sinyal_internet": "Jenis Sinyal Internet"
        },
        "Lingkungan & Kebencanaan": {
            "status_peringatan_dini": "Sistem Peringatan Dini",
            "status_alat_keselamatan": "Alat Keselamatan",
            "status_rambu_evakuasi": "Rambu Keselamatan",
            "status_tps": "Tempat Penampungan Sampah (TPS)",
            "status_tps3r": "Tempat Penampungan Sampah 3R (TPS3R)",
            "status_dilakukan_pemilahan_sampah": "Pemilahan Sampah",
            "kebiasaan_pemilahan_sampah": "Kebiasaan Pemilahan Sampah",
            "warga_terlibat_olah_sampah": "Partisipasi Warga Pengolahan Sampah",
            "status_buang_sampah_dibakar": "Status Pembakaran Sampah"
        }
    }


def calculate_kpi_metrics(df: pd.DataFrame, indicator_key: str, indicator_label: str) -> Dict[str, Any]:
    """
    Calculate KPI metrics for the selected indicator
    
    Args:
        df: DataFrame containing the data
        indicator_key: The column key for the indicator
        indicator_label: Human-readable label for the indicator
        
    Returns:
        Dict: KPI metrics including totals and top performers
    """
    if df.empty or indicator_key not in df.columns:
        return {}
    
    kpis = {}
    data_series = df[indicator_key]
    
    # Check if indicator is numeric or categorical
    if pd.api.types.is_numeric_dtype(data_series):
        # Quantitative indicators
        kpis['type'] = 'quantitative'
        kpis['total'] = int(data_series.sum())
        kpis['median'] = round(data_series.median(), 1)
        kpis['max_value'] = int(data_series.max())
        kpis['min_value'] = int(data_series.min())
        
        # Find top performing village
        if kpis['max_value'] > 0:
            top_village = df.loc[data_series.idxmax()]
            kpis['top_village'] = f"{top_village['nama_desa']} ({kpis['max_value']})"
            kpis['top_village_name'] = top_village['nama_desa']
            kpis['top_village_kec'] = top_village['nama_kecamatan']
        else:
            kpis['top_village'] = "Tidak ada"
        
    else:
        # Qualitative indicators
        kpis['type'] = 'qualitative'
        value_counts = data_series.value_counts()
        kpis['value_counts'] = value_counts.to_dict()
        
        # Calculate percentages
        total_villages = len(df)
        kpis['percentages'] = {}
        for value, count in value_counts.items():
            kpis['percentages'][value] = round((count / total_villages) * 100, 1)
        
        # Most common value
        kpis['most_common'] = value_counts.index[0] if len(value_counts) > 0 else "N/A"
        kpis['most_common_count'] = value_counts.iloc[0] if len(value_counts) > 0 else 0
    
    return kpis


def filter_and_analyze_data(df: pd.DataFrame, 
                           selected_kecamatan: str,
                           selected_desa: List[str],
                           selected_indicator: str,
                           category_indicators: Dict[str, Dict[str, str]],
                           selected_category: str = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Filter data and perform analysis
    
    Args:
        df: Source dataframe
        selected_kecamatan: Selected kecamatan filter
        selected_desa: List of selected villages
        selected_indicator: Selected indicator key
        category_indicators: Category indicator mapping
        
    Returns:
        Tuple of filtered dataframe and analysis results
    """
    filtered_df = df.copy()
    
    # Apply kecamatan filter
    if selected_kecamatan != "Semua Kecamatan":
        filtered_df = filtered_df[filtered_df['nama_kecamatan'] == selected_kecamatan]
    
    # Apply desa filter if any selected
    if selected_desa:
        # Handle both string and list cases
        if isinstance(selected_desa, str):
            filtered_df = filtered_df[filtered_df['nama_desa'] == selected_desa]
        elif isinstance(selected_desa, list) and len(selected_desa) > 0:
            filtered_df = filtered_df[filtered_df['nama_desa'].isin(selected_desa)]
    
    # Handle "Semua" case for indicators
    if selected_indicator == "Semua":
        # Get all indicators for the current category
        current_indicators = category_indicators.get(selected_category, {})
        
        # Calculate summary metrics for all indicators in the category
        kpis = {
            'type': 'summary',
            'total_villages': len(filtered_df),
            'total_kecamatan': filtered_df['nama_kecamatan'].nunique() if len(filtered_df) > 0 else 0,
            'indicator_type': 'multiple',
            'category': selected_category,
            'indicators_count': len(current_indicators)
        }
        
        return filtered_df, kpis
    
    # Get indicator label for single indicator
    indicator_label = None
    for category, indicators in category_indicators.items():
        if selected_indicator in indicators:
            indicator_label = indicators[selected_indicator]
            break
    
    if indicator_label is None:
        indicator_label = selected_indicator
    
    # Calculate KPIs for single indicator
    kpis = calculate_kpi_metrics(filtered_df, selected_indicator, indicator_label)
    kpis = calculate_kpi_metrics(filtered_df, selected_indicator, indicator_label)
    
    return filtered_df, kpis


def create_comparison_analysis(df: pd.DataFrame, 
                             selected_villages: List[str],
                             indicator_columns: List[str],
                             category_indicators: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    """
    Create village comparison analysis
    
    Args:
        df: Source dataframe
        selected_villages: List of villages to compare
        indicator_columns: List of relevant indicator columns
        category_indicators: Category indicator mapping
        
    Returns:
        Dict: Comparison analysis results
    """
    if len(selected_villages) < 2:
        return {}
    
    comparison_df = df[df['nama_desa'].isin(selected_villages)].copy()
    
    comparison_data = {}
    for village in selected_villages:
        village_data = comparison_df[comparison_df['nama_desa'] == village].iloc[0]
        comparison_data[village] = {}
        
        for indicator_key in indicator_columns:
            if indicator_key in village_data:
                # Get readable name
                readable_name = None
                for category, indicators in category_indicators.items():
                    if indicator_key in indicators:
                        readable_name = indicators[indicator_key]
                        break
                
                if readable_name is None:
                    readable_name = indicator_key.replace('_', ' ').title()
                
                comparison_data[village][readable_name] = village_data[indicator_key]
                comparison_data[village]['Kecamatan'] = village_data['nama_kecamatan']
    
    return comparison_data


def get_ranking_data(df: pd.DataFrame, 
                    indicator_key: str, 
                    top_n: int = 5) -> pd.DataFrame:
    """
    Get top N villages for a specific indicator
    
    Args:
        df: Source dataframe
        indicator_key: Indicator column to rank by
        top_n: Number of top villages to return
        
    Returns:
        DataFrame: Top N villages
    """
    if df.empty or indicator_key not in df.columns:
        return pd.DataFrame()
    
    # For numeric data, get top values
    if pd.api.types.is_numeric_dtype(df[indicator_key]):
        ranking_df = df.nlargest(top_n, indicator_key)[['nama_desa', 'nama_kecamatan', indicator_key]]
    else:
        # For categorical data, show distribution
        ranking_df = df[['nama_desa', 'nama_kecamatan', indicator_key]]
    
    return ranking_df


def reset_filters() -> Dict[str, Any]:
    """
    Reset all filters to default values
    
    Returns:
        Dict: Default filter values
    """
    return {
        'kategori': 'Pendidikan',
        'indikator': 'Semua',
        'kecamatan': 'Semua Kecamatan',
        'desa': []
    }
