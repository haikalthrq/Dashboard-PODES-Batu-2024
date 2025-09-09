"""
Dashboard Podes 2024 Kota Batu
Aplikasi Streamlit untuk visualisasi data Potensi Desa (Podes) 2024
"""

import streamlit as st
import pandas as pd
from modules.data_loader import (
    load_podes_data, 
    get_category_indicators, 
    filter_data
)
from modules.ui_components import (
    create_sidebar_filters,
    create_dynamic_title,
    display_data_table,
    create_village_comparison,
    display_data_insights
)


def main():
    """Main application function"""
    
    # Page configuration
    st.set_page_config(
        page_title="Dashboard Podes 2024 - Kota Batu",
        page_icon="🏘️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<div class="main-header">🏘️ Dashboard Podes 2024 - Kota Batu</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Visualisasi Data Potensi Desa untuk Pengambilan Kebijakan</div>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner('Memuat data...'):
        df = load_podes_data()
    
    if df.empty:
        st.error("❌ Gagal memuat data. Pastikan file data_podes_2024.json tersedia.")
        st.stop()
    
    # Get category indicators
    category_indicators = get_category_indicators()
    
    # Create sidebar filters
    (selected_category, 
     selected_indicator_key, 
     selected_kecamatan, 
     selected_desa, 
     indicator_columns) = create_sidebar_filters(df, category_indicators)
    
    # Sidebar info
    st.sidebar.divider()
    st.sidebar.info(f"""
    📊 **Info Data:**
    - Total Desa: {len(df)}
    - Total Kecamatan: {df['NAMA_KEC'].nunique()}
    - Kategori: {selected_category}
    """)
    
    # Main content area
    # Create dynamic title
    selected_indicator_label = category_indicators[selected_category][selected_indicator_key]
    dynamic_title = create_dynamic_title(
        selected_category, 
        selected_indicator_label,
        selected_kecamatan, 
        selected_desa
    )
    
    st.header(dynamic_title)
    
    # Filter data based on selections
    filtered_df = filter_data(
        df, 
        selected_kecamatan, 
        selected_desa, 
        indicator_columns
    )
    
    if filtered_df.empty:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih.")
        st.info("💡 Coba ubah filter untuk melihat data.")
        return
    
    # Main content tabs for better organization
    tab1, tab2, tab3 = st.tabs(["📋 Data & Ranking", "🔍 Perbandingan Desa", "📊 Insight & Statistik"])
    
    with tab1:
        # Display data table with ranking capabilities
        display_data_table(filtered_df, selected_indicator_key, category_indicators)
    
    with tab2:
        # Village comparison mode
        create_village_comparison(filtered_df, indicator_columns, category_indicators)
    
    with tab3:
        # Data insights and statistics
        display_data_insights(filtered_df, selected_category, selected_indicator_key)
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📅 Data:** Podes 2024")
    with col2:
        st.markdown("**🏛️ Sumber:** BPS Kota Batu")
    with col3:
        st.markdown("**🎯 Tujuan:** Analisis Kebijakan")


def show_data_info():
    """Show data information in sidebar"""
    st.sidebar.divider()
    with st.sidebar.expander("ℹ️ Informasi Aplikasi"):
        st.write("""
        **Dashboard Podes 2024** adalah aplikasi untuk menganalisis data Potensi Desa di Kota Batu.
        
        **Fitur Utama:**
        - 📊 Filter berdasarkan kategori dan lokasi
        - 📋 Tabel interaktif dengan ranking otomatis
        - 🔍 Perbandingan antar desa
        - 📈 Insight dan statistik data
        
        **Cara Penggunaan:**
        1. Pilih kategori analisis
        2. Pilih indikator spesifik
        3. Filter berdasarkan lokasi (opsional)
        4. Lihat ranking dengan klik header tabel
        5. Bandingkan desa di tab perbandingan
        """)


if __name__ == "__main__":
    # Show data info
    show_data_info()
    
    # Run main application
    main()
