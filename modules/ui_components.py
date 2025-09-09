"""
UI Components module for Podes 2024 dashboard
Contains functions for creating sidebar filters and visualization components
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Tuple


def create_sidebar_filters(df: pd.DataFrame, 
                          category_indicators: Dict[str, Dict[str, str]]) -> Tuple[str, str, str, List[str], List[str]]:
    """
    Create sidebar filters for the dashboard
    
    Args:
        df: DataFrame containing Podes data
        category_indicators: Dictionary mapping categories to indicators
        
    Returns:
        Tuple containing selected values for category, indicator, kecamatan, desa, and indicator columns
    """
    st.sidebar.header("🎛️ Panel Kontrol")
    
    # Category filter
    categories = list(category_indicators.keys())
    selected_category = st.sidebar.selectbox(
        "📊 Kategori Analisis:",
        categories,
        help="Pilih kategori data yang ingin dianalisis"
    )
    
    # Dynamic indicator filter based on selected category
    indicators = category_indicators[selected_category]
    selected_indicator_key = st.sidebar.selectbox(
        "📈 Indikator:",
        list(indicators.keys()),
        format_func=lambda x: indicators[x],
        help="Pilih indikator spesifik untuk analisis"
    )
    selected_indicator_label = indicators[selected_indicator_key]
    
    st.sidebar.divider()
    
    # Location filters
    st.sidebar.subheader("📍 Filter Lokasi")
    
    # Import functions from data_loader
    from modules.data_loader import get_kecamatan_list, get_desa_list
    
    # Kecamatan filter
    kecamatan_list = get_kecamatan_list(df)
    selected_kecamatan = st.sidebar.selectbox(
        "Kecamatan:",
        kecamatan_list,
        help="Pilih kecamatan atau 'Semua Kecamatan' untuk melihat semua data"
    )
    
    # Desa filter (multiselect)
    desa_list = get_desa_list(df, selected_kecamatan)
    selected_desa = st.sidebar.multiselect(
        "Desa (opsional):",
        desa_list,
        help="Pilih desa tertentu atau kosongkan untuk melihat semua desa"
    )
    
    # Get relevant indicator columns for the selected category
    indicator_columns = list(indicators.keys())
    
    return selected_category, selected_indicator_key, selected_kecamatan, selected_desa, indicator_columns


def create_dynamic_title(selected_category: str, 
                        selected_indicator_label: str,
                        selected_kecamatan: str,
                        selected_desa: List[str]) -> str:
    """
    Create dynamic title based on current filters
    
    Args:
        selected_category: Selected category
        selected_indicator_label: Selected indicator label
        selected_kecamatan: Selected kecamatan
        selected_desa: List of selected desa
        
    Returns:
        str: Dynamic title string
    """
    title_parts = [f"Data {selected_category}"]
    
    if selected_indicator_label:
        title_parts.append(f"- {selected_indicator_label}")
    
    if selected_kecamatan != "Semua Kecamatan":
        title_parts.append(f"di Kecamatan {selected_kecamatan}")
    else:
        title_parts.append("di Kota Batu")
    
    if selected_desa:
        if len(selected_desa) == 1:
            title_parts.append(f"(Desa {selected_desa[0]})")
        elif len(selected_desa) <= 3:
            title_parts.append(f"({', '.join(selected_desa)})")
        else:
            title_parts.append(f"({len(selected_desa)} desa terpilih)")
    
    return " ".join(title_parts)


def display_data_table(filtered_df: pd.DataFrame, 
                      selected_indicator_key: str,
                      category_indicators: Dict[str, Dict[str, str]]) -> pd.DataFrame:
    """
    Display interactive data table with sorting capabilities
    
    Args:
        filtered_df: Filtered DataFrame to display
        selected_indicator_key: Currently selected indicator key
        category_indicators: Dictionary mapping categories to indicators
        
    Returns:
        pd.DataFrame: The displayed dataframe for further processing
    """
    if filtered_df.empty:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
        return filtered_df
    
    # Prepare display dataframe with readable column names
    display_df = filtered_df.copy()
    
    # Rename columns to more readable format
    column_mapping = {
        'nama_kecamatan': 'Kecamatan',
        'nama_desa': 'Desa',
        'jumlah_tk': 'Jumlah TK',
        'jumlah_sd': 'Jumlah SD',
        'jumlah_smp': 'Jumlah SMP', 
        'jumlah_sma': 'Jumlah SMA',
        'jumlah_rs': 'Jumlah RS',
        'jumlah_puskesmas': 'Jumlah Puskesmas',
        'status_peringatan_dini': 'Sistem Peringatan Dini',
        'status_alat_keselamatan': 'Alat Keselamatan',
        'status_rambu_evakuasi': 'Rambu Keselamatan',
        'kekuatan_sinyal': 'Kualitas Sinyal Internet',
        'jenis_sinyal_internet': 'Jenis Sinyal Internet'
    }
    
    # Only rename columns that exist in the dataframe
    existing_mappings = {k: v for k, v in column_mapping.items() if k in display_df.columns}
    display_df = display_df.rename(columns=existing_mappings)
    
    # Remove id_desa for display
    if 'id_desa' in display_df.columns:
        display_df = display_df.drop('id_desa', axis=1)
    
    st.subheader("📋 Tabel Data Interaktif")
    st.info("💡 Klik pada header kolom untuk mengurutkan data (ranking otomatis)")
    
    # Display the interactive dataframe
    st.dataframe(
        display_df,
        width='stretch',
        hide_index=True
    )
    
    # Display data summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Desa", len(display_df))
    with col2:
        st.metric("Total Kecamatan", display_df['Kecamatan'].nunique() if 'Kecamatan' in display_df.columns else 0)
    with col3:
        # Show summary for the main indicator if it's numeric
        if selected_indicator_key in filtered_df.columns:
            if pd.api.types.is_numeric_dtype(filtered_df[selected_indicator_key]):
                total_value = filtered_df[selected_indicator_key].sum()
                readable_name = column_mapping.get(selected_indicator_key, selected_indicator_key)
                st.metric(f"Total {readable_name}", int(total_value))
    
    return filtered_df


def create_village_comparison(filtered_df: pd.DataFrame,
                            indicator_columns: List[str],
                            category_indicators: Dict[str, Dict[str, str]]) -> None:
    """
    Create village comparison section
    
    Args:
        filtered_df: Filtered DataFrame
        indicator_columns: List of indicator columns for current category
        category_indicators: Dictionary mapping categories to indicators
    """
    if filtered_df.empty or len(filtered_df) < 2:
        return
    
    st.divider()
    st.subheader("🔍 Mode Perbandingan Desa")
    
    # Village selector for comparison
    village_options = filtered_df['nama_desa'].tolist()
    selected_villages = st.multiselect(
        "Pilih desa untuk dibandingkan (minimal 2):",
        village_options,
        help="Pilih 2 atau lebih desa untuk melihat perbandingan data"
    )
    
    if len(selected_villages) >= 2:
        comparison_df = filtered_df[filtered_df['nama_desa'].isin(selected_villages)]
        
        st.write(f"**Perbandingan {len(selected_villages)} Desa:**")
        
        # Create metrics comparison
        cols = st.columns(len(selected_villages))
        
        for idx, village in enumerate(selected_villages):
            village_data = comparison_df[comparison_df['nama_desa'] == village].iloc[0]
            
            with cols[idx]:
                st.write(f"**{village}**")
                st.write(f"*Kecamatan: {village_data['nama_kecamatan']}*")
                
                # Display metrics for each indicator
                for indicator_key in indicator_columns:
                    if indicator_key in village_data:
                        # Get readable name
                        readable_name = None
                        for category, indicators in category_indicators.items():
                            if indicator_key in indicators:
                                readable_name = indicators[indicator_key]
                                break
                        
                        if readable_name is None:
                            readable_name = indicator_key
                        
                        value = village_data[indicator_key]
                        
                        # Display metric based on data type
                        if pd.api.types.is_numeric_dtype(type(value)) and not pd.isna(value):
                            st.metric(readable_name, int(value))
                        else:
                            st.write(f"**{readable_name}:** {value}")
        
        # Create comparison chart for numeric indicators
        numeric_indicators = []
        for indicator in indicator_columns:
            if indicator in comparison_df.columns:
                if pd.api.types.is_numeric_dtype(comparison_df[indicator]):
                    numeric_indicators.append(indicator)
        
        if numeric_indicators:
            st.subheader("📊 Grafik Perbandingan")
            
            # Let user select which indicator to visualize
            if len(numeric_indicators) > 1:
                chart_indicator = st.selectbox(
                    "Pilih indikator untuk grafik:",
                    numeric_indicators,
                    format_func=lambda x: category_indicators.get(next(iter(category_indicators.keys())), {}).get(x, x)
                )
            else:
                chart_indicator = numeric_indicators[0]
            
            # Create bar chart
            chart_data = comparison_df[['nama_desa', chart_indicator]].copy()
            
            fig = px.bar(
                chart_data,
                x='nama_desa',
                y=chart_indicator,
                title=f"Perbandingan {category_indicators.get(next(iter(category_indicators.keys())), {}).get(chart_indicator, chart_indicator)}",
                labels={'nama_desa': 'Desa', chart_indicator: 'Jumlah'}
            )
            
            fig.update_layout(
                xaxis_title="Desa",
                yaxis_title="Jumlah",
                showlegend=False
            )
            
            st.plotly_chart(fig, width='stretch')


def display_data_insights(filtered_df: pd.DataFrame,
                         selected_category: str,
                         selected_indicator_key: str) -> None:
    """
    Display data insights and statistics
    
    Args:
        filtered_df: Filtered DataFrame
        selected_category: Selected category
        selected_indicator_key: Selected indicator key
    """
    if filtered_df.empty:
        return
    
    st.divider()
    st.subheader("📊 Insight Data")
    
    # Basic statistics for numeric indicators
    if selected_indicator_key in filtered_df.columns:
        if pd.api.types.is_numeric_dtype(filtered_df[selected_indicator_key]):
            col1, col2, col3 = st.columns(3)
            
            data_series = filtered_df[selected_indicator_key]
            
            with col1:
                st.metric("Maksimum", int(data_series.max()))
            with col2:
                st.metric("Minimum", int(data_series.min()))
            with col3:
                st.metric("Median", f"{data_series.median():.1f}")
            
            # Show top 5 villages for this indicator
            if len(filtered_df) > 1:
                st.write("**Top 5 Desa dengan nilai tertinggi:**")
                top_villages = filtered_df.nlargest(5, selected_indicator_key)[['nama_desa', 'nama_kecamatan', selected_indicator_key]]
                
                # Rename columns for display
                display_cols = {
                    'nama_desa': 'Desa',
                    'nama_kecamatan': 'Kecamatan',
                    selected_indicator_key: selected_indicator_key.replace('_', ' ').title()
                }
                top_villages = top_villages.rename(columns=display_cols)
                
                st.dataframe(top_villages, hide_index=True, width='stretch')
        
        # For categorical data, show distribution
        else:
            st.write("**Distribusi data:**")
            value_counts = filtered_df[selected_indicator_key].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(value_counts.to_frame('Jumlah Desa'))
            
            with col2:
                # Create pie chart for categorical data
                fig = px.pie(
                    values=value_counts.values,
                    names=value_counts.index,
                    title="Distribusi Data"
                )
                st.plotly_chart(fig, width='stretch')
