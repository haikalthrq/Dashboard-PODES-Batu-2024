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


def show_landing_page():
    """Display the landing page"""
    
    # Page configuration for landing page
    st.set_page_config(
        page_title="Dashboard Podes 2024 - Kota Batu",
        page_icon="🏘️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for landing page
    st.markdown("""
    <style>
    .landing-header {
        font-size: 3.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .landing-subtitle {
        font-size: 1.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .landing-description {
        font-size: 1.1rem;
        color: #34495e;
        text-align: justify;
        line-height: 1.6;
        margin-bottom: 2rem;
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .big-button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        border: none;
        color: white;
        padding: 1rem 2rem;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 2rem 0;
        cursor: pointer;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stats-container {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Landing page content
    st.markdown('<div class="landing-header">🏘️ Dashboard Potensi Desa Kota Batu</div>', unsafe_allow_html=True)
    st.markdown('<div class="landing-subtitle">Visualisasi Data Podes 2024 untuk Pengambilan Kebijakan Berbasis Data</div>', unsafe_allow_html=True)
    
    # Hero image or icon
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://via.placeholder.com/600x300/1f77b4/ffffff?text=Kota+Batu+Dashboard", 
                caption="Dashboard Analisis Potensi Desa Kota Batu", 
                use_container_width=True)
    
    # Description section
    st.markdown("""
    <div class="landing-description">
    <h3>🎯 Tentang Dashboard</h3>
    <p>
    Dashboard Potensi Desa Kota Batu adalah aplikasi interaktif yang dirancang khusus untuk mendukung 
    <strong>Pemerintah Kota Batu</strong> dalam menganalisis data Survei Potensi Desa (Podes) 2024 
    dari Badan Pusat Statistik (BPS). Aplikasi ini menyediakan visualisasi data yang komprehensif 
    dan mudah dipahami untuk mendukung pengambilan kebijakan yang berbasis data faktual.
    </p>
    <p>
    Dengan menggunakan data resmi dari BPS, dashboard ini memungkinkan analisis mendalam terhadap 
    berbagai aspek potensi desa mulai dari <strong>pendidikan, kesehatan, mitigasi bencana, 
    hingga konektivitas ekonomi</strong>. Semua data disajikan secara transparan tanpa manipulasi 
    skor, sehingga dapat menjadi rujukan yang akurat untuk perencanaan pembangunan daerah.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key features
    st.markdown("### ✨ Fitur Utama Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
        <h4>📊 Analisis Multi-Kategori</h4>
        <p>Pendidikan, Kesehatan, Bencana & Lingkungan, Ekonomi & Konektivitas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
        <h4>🔍 Perbandingan Desa</h4>
        <p>Bandingkan potensi antar desa secara langsung dengan visualisasi interaktif</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
        <h4>📈 Ranking Otomatis</h4>
        <p>Sistem peringkat transparan berdasarkan data faktual tanpa skor agregat</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Data statistics preview
    st.markdown("### 📊 Cakupan Data Podes 2024")
    
    # Load data for preview
    try:
        df = load_podes_data()
        if not df.empty:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Desa", len(df), help="Jumlah desa yang tercakup dalam survei")
            with col2:
                st.metric("Total Kecamatan", df['NAMA_KEC'].nunique(), help="Jumlah kecamatan di Kota Batu")
            with col3:
                st.metric("Indikator Pendidikan", 4, help="TK, SD, SMP, SMA")
            with col4:
                st.metric("Indikator Kesehatan", 3, help="RS, Puskesmas, Puskesmas Rawat Inap")
    except:
        st.warning("Data preview tidak tersedia saat ini")
    
    st.markdown("---")
    
    # Call to action
    st.markdown("### 🚀 Mulai Analisis Data")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 MASUK KE DASHBOARD", key="enter_dashboard", 
                    help="Klik untuk mulai menganalisis data Podes 2024"):
            st.session_state.page = "dashboard"
            st.rerun()
    
    # Footer information
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📅 Sumber Data:**  
        Survei Podes 2024 - BPS
        """)
    with col2:
        st.markdown("""
        **🏛️ Untuk:**  
        Pemerintah Kota Batu
        """)
    with col3:
        st.markdown("""
        **🎯 Tujuan:**  
        Kebijakan Berbasis Data
        """)


def main():
    """Main dashboard function"""
    
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
    
    # Add back to landing page button in sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("� Kembali ke Halaman Utama", key="back_to_landing"):
        st.session_state.page = "landing"
        st.experimental_rerun()


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


def run_app():
    """Main application controller"""
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    
    # Route to appropriate page
    if st.session_state.page == "landing":
        show_landing_page()
    elif st.session_state.page == "dashboard":
        # Show data info in sidebar for dashboard
        show_data_info()
        # Run main dashboard
        main()


if __name__ == "__main__":
    run_app()
