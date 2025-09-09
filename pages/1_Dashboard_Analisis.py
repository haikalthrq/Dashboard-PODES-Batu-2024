"""
Dashboard Analisis - Halaman Utama Analisis Data Podes 2024
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import load_podes_data, get_kecamatan_list, get_desa_list
from modules.analysis import (
    get_updated_category_indicators,
    filter_and_analyze_data,
    create_comparison_analysis,
    get_ranking_data,
    reset_filters
)

# Page configuration
st.set_page_config(
    page_title="Dashboard Analisis - Podes 2024",
    page_icon="📊",
    layout="wide"
)

def create_sidebar_controls(df: pd.DataFrame, category_indicators: dict):
    """Create sidebar controls with all filters and reset button"""
    
    st.sidebar.header("🎛️ Panel Kontrol")
    
    # Initialize session state for filters if not exists
    if 'filters' not in st.session_state:
        st.session_state.filters = reset_filters()
    
    # Category filter
    categories = list(category_indicators.keys())
    selected_category = st.sidebar.selectbox(
        "📊 Filter Kategori Utama:",
        categories,
        index=categories.index(st.session_state.filters['kategori']) if st.session_state.filters['kategori'] in categories else 0,
        help="Pilih kategori data yang ingin dianalisis"
    )
    
    # Update session state
    st.session_state.filters['kategori'] = selected_category
    
    # Dynamic indicator filter
    indicators = category_indicators[selected_category]
    indicator_keys = list(indicators.keys())
    
    # Add "Semua" option to the beginning of the list
    indicator_options = ["Semua"] + indicator_keys
    
    # Find current indicator index
    current_indicator = st.session_state.filters['indikator']
    if current_indicator not in indicator_options:
        current_indicator = "Semua"
        st.session_state.filters['indikator'] = current_indicator
    
    # Create format function that handles "Semua" option
    def format_indicator(key):
        if key == "Semua":
            return f"📊 Semua Indikator {selected_category}"
        else:
            return indicators[key]
    
    selected_indicator_key = st.sidebar.selectbox(
        "📈 Filter Indikator Spesifik:",
        indicator_options,
        format_func=format_indicator,
        index=indicator_options.index(current_indicator),
        help="Pilih indikator spesifik untuk analisis detail, atau 'Semua' untuk melihat semua indikator"
    )
    
    st.session_state.filters['indikator'] = selected_indicator_key
    
    st.sidebar.divider()
    
    # Location filters
    st.sidebar.subheader("📍 Filter Lokasi")
    
    # Kecamatan filter
    kecamatan_list = get_kecamatan_list(df)
    selected_kecamatan = st.sidebar.selectbox(
        "Kecamatan:",
        kecamatan_list,
        index=kecamatan_list.index(st.session_state.filters['kecamatan']) if st.session_state.filters['kecamatan'] in kecamatan_list else 0,
        help="Pilih kecamatan atau 'Semua Kecamatan'"
    )
    
    st.session_state.filters['kecamatan'] = selected_kecamatan
    
    # Desa filter  
    desa_list = get_desa_list(df, selected_kecamatan)
    selected_desa = st.sidebar.multiselect(
        "Desa/Kelurahan:",
        desa_list,
        default=st.session_state.filters['desa'],
        help="Filter tambahan untuk analisis spesifik desa (opsional)"
    )
    
    st.session_state.filters['desa'] = selected_desa
    
    # Info about comparison feature
    st.sidebar.info("💡 Untuk perbandingan desa, gunakan filter dedicated di tab 'Perbandingan Desa'")
    
    st.sidebar.divider()
    
    # Reset button
    if st.sidebar.button("🔄 Reset Filter", help="Kembalikan semua filter ke kondisi awal"):
        st.session_state.filters = reset_filters()
        st.rerun()
    
    return selected_category, selected_indicator_key, selected_kecamatan, selected_desa


def display_kpi_cards(kpis: dict, indicator_label: str):
    """Display KPI cards based on indicator type"""
    
    if not kpis:
        st.warning("Tidak dapat menghitung KPI untuk indikator ini")
        return
    
    if kpis['type'] == 'summary':
        # Summary KPIs for "Semua" indicator
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Desa",
                f"{kpis['total_villages']:,}",
                help="Total desa yang dianalisis"
            )
        
        with col2:
            st.metric(
                "Total Kecamatan",
                f"{kpis['total_kecamatan']:,}",
                help="Total kecamatan yang dianalisis"
            )
        
        with col3:
            st.metric(
                "Kategori",
                kpis.get('category', 'N/A'),
                help="Kategori yang sedang dianalisis"
            )
        
        with col4:
            st.metric(
                "Jumlah Indikator",
                f"{kpis.get('indicators_count', 0)}",
                help="Jumlah indikator dalam kategori ini"
            )
    
    elif kpis['type'] == 'quantitative':
        # Quantitative KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                f"Total {indicator_label}",
                f"{kpis['total']:,}",
                help=f"Total {indicator_label} di seluruh area yang difilter"
            )
        
        with col2:
            st.metric(
                "Rata-rata per Desa",
                f"{kpis['average']:.1f}",
                help="Nilai rata-rata per desa"
            )
        
        with col3:
            st.metric(
                "Desa Terbaik",
                kpis.get('top_village', 'Tidak ada'),
                help="Desa dengan nilai tertinggi"
            )
        
        with col4:
            villages_with = kpis.get('villages_with_facility', 0)
            total_villages = villages_with + kpis.get('villages_without_facility', 0)
            percentage = (villages_with / total_villages * 100) if total_villages > 0 else 0
            st.metric(
                "Desa Memiliki Fasilitas",
                f"{villages_with} ({percentage:.1f}%)",
                help="Jumlah dan persentase desa yang memiliki fasilitas ini"
            )
    
    else:
        # Qualitative KPIs
        value_counts = kpis.get('value_counts', {})
        percentages = kpis.get('percentages', {})
        
        cols = st.columns(len(value_counts))
        
        for i, (value, count) in enumerate(value_counts.items()):
            with cols[i]:
                percentage = percentages.get(value, 0)
                st.metric(
                    f"Status: {value}",
                    f"{count} desa ({percentage:.1f}%)",
                    help=f"Jumlah desa dengan status {value}"
                )


def display_all_indicators_table(filtered_df: pd.DataFrame, selected_category: str, category_indicators: dict):
    """Display table with all indicators for the selected category"""
    
    if filtered_df.empty:
        st.warning("Tidak ada data untuk ditampilkan")
        return
    
    st.subheader("📋 Tabel Semua Indikator")
    st.info(f"💡 Menampilkan semua indikator untuk kategori {selected_category}")
    
    # Get all indicators for the current category
    indicators = category_indicators[selected_category]
    
    # Prepare display columns
    base_columns = ['nama_kecamatan', 'nama_desa']
    indicator_columns = list(indicators.keys())
    
    # Check which columns actually exist in the dataframe
    available_columns = base_columns + [col for col in indicator_columns if col in filtered_df.columns]
    
    if len(available_columns) == len(base_columns):
        st.warning(f"Tidak ada data indikator yang tersedia untuk kategori {selected_category}")
        return
    
    # Create display dataframe
    display_df = filtered_df[available_columns].copy()
    
    # Create column mapping for better display names
    column_mapping = {
        'nama_kecamatan': 'Kecamatan',
        'nama_desa': 'Desa'
    }
    
    # Add indicator column mappings
    for col in indicator_columns:
        if col in display_df.columns:
            column_mapping[col] = indicators[col]
    
    display_df = display_df.rename(columns=column_mapping)
    
    # Display the table
    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )
    
    # Show summary statistics
    st.subheader("📊 Ringkasan Statistik")
    numeric_cols = []
    for col in indicator_columns:
        if col in filtered_df.columns and pd.api.types.is_numeric_dtype(filtered_df[col]):
            numeric_cols.append(col)
    
    if numeric_cols:
        summary_data = []
        for col in numeric_cols:
            col_label = indicators[col]
            summary_data.append({
                'Indikator': col_label,
                'Total': filtered_df[col].sum(),
                'Rata-rata': round(filtered_df[col].mean(), 1),
                'Maksimum': filtered_df[col].max(),
                'Minimum': filtered_df[col].min()
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, width="stretch", hide_index=True)


def display_ranking_table(filtered_df: pd.DataFrame, selected_indicator: str, indicator_label: str):
    """Display interactive ranking table"""
    
    if filtered_df.empty:
        st.warning("Tidak ada data untuk ditampilkan")
        return
    
    st.subheader("📋 Tabel Peringkat Interaktif")
    
    # Handle "Semua" case - show all indicators in the category
    if selected_indicator == "Semua":
        st.info("💡 Menampilkan semua indikator dalam kategori yang dipilih")
        
        # Get all relevant columns for the category (this will be passed from the calling function)
        base_columns = ['nama_kecamatan', 'nama_desa']
        
        # For now, show basic info - we'll need to determine which columns to show
        # based on the current category from the calling function
        display_df = filtered_df[base_columns].copy()
        
        # Rename columns for better display
        column_mapping = {
            'nama_kecamatan': 'Kecamatan',
            'nama_desa': 'Desa'
        }
        display_df = display_df.rename(columns=column_mapping)
        
        st.info("📝 Untuk melihat data spesifik, silakan pilih indikator tertentu dari filter di sidebar")
        
    else:
        st.info("💡 Klik pada header kolom untuk mengurutkan data dan melihat peringkat")
        
        # Prepare display dataframe
        display_columns = ['nama_kecamatan', 'nama_desa', selected_indicator]
        display_df = filtered_df[display_columns].copy()
        
        # Rename columns for better display
        column_mapping = {
            'nama_kecamatan': 'Kecamatan',
            'nama_desa': 'Desa',
            selected_indicator: indicator_label
        }
        display_df = display_df.rename(columns=column_mapping)
    
    # Display the table
    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )
    
    # Show additional ranking info for numeric data (only for specific indicators)
    if selected_indicator != "Semua" and pd.api.types.is_numeric_dtype(filtered_df[selected_indicator]):
        st.subheader("🏆 Top 5 Peringkat")
        top_5 = get_ranking_data(filtered_df, selected_indicator, 5)
        
        if not top_5.empty:
            top_5_display = top_5.rename(columns={
                'nama_kecamatan': 'Kecamatan',
                'nama_desa': 'Desa',
                selected_indicator: indicator_label
            })
            st.dataframe(top_5_display, hide_index=True, width="stretch")


def display_village_comparison(filtered_df: pd.DataFrame, 
                             indicator_columns: list,
                             category_indicators: dict):
    """Display village comparison with dedicated filter"""
    
    st.subheader("🔍 Perbandingan Desa")
    
    # Dedicated village selection filter
    st.markdown("#### 📍 Pilih Desa untuk Perbandingan")
    st.info("💡 Pilih maksimal 4 desa/kelurahan untuk perbandingan yang optimal")
    
    # Get available villages from filtered data
    available_villages = sorted(filtered_df['nama_desa'].unique().tolist())
    
    if len(available_villages) < 2:
        st.warning("Tidak cukup desa untuk perbandingan. Minimal 2 desa diperlukan.")
        return
    
    # Multi-select with maximum 4 villages
    comparison_villages = st.multiselect(
        "Pilih desa/kelurahan untuk dibandingkan:",
        options=available_villages,
        default=available_villages[:min(2, len(available_villages))],
        max_selections=4,
        help="Pilih 2-4 desa untuk perbandingan yang efektif"
    )
    
    if len(comparison_villages) < 2:
        st.warning("⚠️ Silakan pilih minimal 2 desa untuk melakukan perbandingan")
        return
    
    # Filter data for selected villages only
    comparison_df = filtered_df[filtered_df['nama_desa'].isin(comparison_villages)]
    
    if comparison_df.empty:
        st.warning("Tidak ada data untuk desa yang dipilih")
        return
    
    comparison_data = create_comparison_analysis(
        comparison_df, comparison_villages, indicator_columns, category_indicators
    )
    
    if not comparison_data:
        st.warning("Tidak dapat membuat perbandingan")
        return
    
    # Show selected villages info
    st.success(f"✅ Membandingkan {len(comparison_villages)} desa: {', '.join(comparison_villages)}")
    
    # Display comparison in responsive columns
    cols = st.columns(len(comparison_villages))
    
    for i, village in enumerate(comparison_villages):
        with cols[i]:
            st.markdown(f"#### 🏘️ {village}")
            village_data = comparison_data.get(village, {})
            
            if 'Kecamatan' in village_data:
                st.markdown(f"**📍 Kecamatan:** {village_data['Kecamatan']}")
                st.divider()
            
            # Display metrics for each indicator
            for indicator_name, value in village_data.items():
                if indicator_name != 'Kecamatan':
                    if pd.api.types.is_numeric_dtype(type(value)) and not pd.isna(value):
                        st.metric(indicator_name, int(value))
                    else:
                        st.markdown(f"**{indicator_name}:** {value}")
    
    # Create comparison chart for numeric indicators
    st.markdown("#### 📊 Grafik Perbandingan")
    numeric_indicators = []
    for indicator in indicator_columns:
        if indicator in comparison_df.columns:
            if pd.api.types.is_numeric_dtype(comparison_df[indicator]):
                numeric_indicators.append(indicator)
    
    if numeric_indicators:
        # Select indicator for chart
        selected_chart_indicator = st.selectbox(
            "Pilih indikator untuk grafik perbandingan:",
            options=numeric_indicators,
            format_func=lambda x: get_indicator_label(x, category_indicators)
        )
        
        # Create bar chart
        chart_data = comparison_df[['nama_desa', selected_chart_indicator]].copy()
        indicator_label = get_indicator_label(selected_chart_indicator, category_indicators)
        
        chart_data = chart_data.rename(columns={
            'nama_desa': 'Desa',
            selected_chart_indicator: indicator_label
        })
        
        st.bar_chart(
            chart_data.set_index('Desa'),
            height=400
        )
    else:
        st.info("📊 Tidak ada indikator numerik untuk ditampilkan dalam grafik")


def get_indicator_label(indicator_key: str, category_indicators: dict) -> str:
    """Helper function to get indicator label from category indicators"""
    for category, indicators in category_indicators.items():
        if indicator_key in indicators:
            return indicators[indicator_key]
    return indicator_key


def main():
    """Main dashboard function"""
    
    # Header
    st.title("📊 Dashboard Analisis Data Podes 2024")
    st.markdown("### Analisis Interaktif Potensi Desa Kota Batu")
    
    # Load data
    with st.spinner('Memuat data...'):
        df = load_podes_data()
    
    if df.empty:
        st.error("❌ Gagal memuat data. Pastikan file data tersedia.")
        st.stop()
    
    # Get category indicators
    category_indicators = get_updated_category_indicators()
    
    # Create sidebar controls
    (selected_category, 
     selected_indicator_key, 
     selected_kecamatan, 
     selected_desa) = create_sidebar_controls(df, category_indicators)
    
    # Get indicator label and title
    if selected_indicator_key == "Semua":
        indicator_label = f"Semua Indikator {selected_category}"
        title_parts = [f"Analisis {selected_category}: {indicator_label}"]
    else:
        indicator_label = category_indicators[selected_category][selected_indicator_key]
        title_parts = [f"Analisis {selected_category}: {indicator_label}"]
    
    if selected_kecamatan != "Semua Kecamatan":
        title_parts.append(f"di Kecamatan {selected_kecamatan}")
    else:
        title_parts.append("di Kota Batu")
    
    dynamic_title = " ".join(title_parts)
    st.header(dynamic_title)
    
    # Filter and analyze data
    filtered_df, kpis = filter_and_analyze_data(
        df, selected_kecamatan, selected_desa, selected_indicator_key, category_indicators, selected_category
    )
    
    if filtered_df.empty:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih.")
        st.info("💡 Coba ubah filter untuk melihat data.")
        return
    
    # Display KPI cards
    st.subheader("📈 Ringkasan Data")
    display_kpi_cards(kpis, indicator_label)
    
    st.divider()
    
    # Get relevant indicator columns for current category
    indicator_columns = list(category_indicators[selected_category].keys())
    
    # Main content in tabs
    tab1, tab2 = st.tabs(["📋 Tabel Peringkat", "🔍 Perbandingan Desa"])
    
    with tab1:
        if selected_indicator_key == "Semua":
            display_all_indicators_table(filtered_df, selected_category, category_indicators)
        else:
            display_ranking_table(filtered_df, selected_indicator_key, indicator_label)
    
    with tab2:
        display_village_comparison(
            filtered_df, indicator_columns, category_indicators
        )
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📅 Data:** Podes 2024 - BPS")
    with col2:
        st.markdown(f"**📊 Total Desa Dianalisis:** {len(filtered_df)}")
    with col3:
        st.markdown(f"**🎯 Kategori:** {selected_category}")


if __name__ == "__main__":
    main()
