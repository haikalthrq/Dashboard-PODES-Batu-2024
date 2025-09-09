"""
Dashboard Podes 2024 Kota Batu - Landing Page
Halaman muka untuk aplikasi dashboard analisis data Potensi Desa
"""

import streamlit as st
from modules.data_loader import load_podes_data

# Page configuration
st.set_page_config(
    page_title="Dashboard Potensi Desa - Kota Batu",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    """Main landing page function"""
    
    # Custom CSS for professional landing page
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .description-box {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #1f77b4;
        margin: 2rem 0;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<div class="main-header">🏘️ Dashboard Interaktif Potensi Desa Kota Batu</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Analisis Data Podes 2024 untuk Perencanaan Berbasis Bukti</div>', unsafe_allow_html=True)
    
    # Description section
    st.markdown("""
    <div class="description-box">
    <h3>🎯 Tentang Platform</h3>
    <p style="font-size: 1.1rem; line-height: 1.6;">
    Platform analisis data terintegrasi yang memanfaatkan hasil Survei Potensi Desa (Podes) 2024 
    dari Badan Pusat Statistik (BPS). Dirancang khusus untuk memfasilitasi <strong>Pemerintah Kota Batu</strong> 
    dalam melakukan analisis komprehensif dan pengambilan kebijakan berbasis data faktual.
    </p>
    <p style="font-size: 1.1rem; line-height: 1.6;">
    Sistem menyediakan akses terstruktur dengan kemampuan filtering, visualisasi interaktif, 
    dan analisis komparatif untuk mendukung perencanaan pembangunan daerah yang efektif.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key features section
    st.markdown("### ✨ Fitur Utama Platform")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h4>📊 Pendidikan</h4>
        <p>Analisis fasilitas pendidikan: TK, SD, SMP, SMA</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
        <h4>🏥 Kesehatan</h4>
        <p>Infrastruktur kesehatan: RS, Puskesmas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
        <h4>🌐 Infrastruktur</h4>
        <p>Konektivitas: Sinyal Internet, Angkutan Umum</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
        <h4>⚠️ Lingkungan & Kebencanaan</h4>
        <p>Mitigasi: Peringatan Dini, Alat & Rambu Keselamatan, Pengelolaan Sampah</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Data preview section
    st.markdown("### 📊 Cakupan Data Podes 2024")
    
    try:
        df = load_podes_data()
        if not df.empty:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Desa", len(df), help="Jumlah desa yang tercakup dalam survei")
            with col2:
                st.metric("Total Kecamatan", df['nama_kecamatan'].nunique(), help="Jumlah kecamatan di Kota Batu")
            with col3:
                st.metric("Kategori Analisis", 4, help="Pendidikan, Kesehatan, Infrastruktur, Kebencanaan")
            with col4:
                st.metric("Total Indikator", 18, help="Indikator kuantitatif dan kualitatif termasuk persampahan")
    except:
        st.info("Data preview akan ditampilkan setelah sistem fully loaded")
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📅 Sumber Data:**  
        Survei Podes 2024 - BPS
        """)
    with col2:
        st.markdown("""
        **🏛️ Pengguna:**  
        Pemerintah Kota Batu
        """)
    with col3:
        st.markdown("""
        **🎯 Manfaat:**  
        Perencanaan berbasis data faktual untuk pelayanan publik berkualitas
        """)


if __name__ == "__main__":
    main()