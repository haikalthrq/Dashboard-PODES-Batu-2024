"""
Dashboard Analisis - Halaman Utama Analisis Data Podes 2024
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from modules.data_loader import load_podes_data, get_kecamatan_list, get_desa_list
from modules.analysis import (
    get_updated_category_indicators,
    filter_and_analyze_data,
    create_comparison_analysis,
    get_ranking_data,
    reset_filters
)
from enhanced_viz import create_enhanced_quantitative_visualization, create_enhanced_qualitative_visualization

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
    
    # Determine default index for selectbox
    default_index = 0  # Default to "Semua Desa/Kelurahan"
    if st.session_state.filters['desa'] and len(st.session_state.filters['desa']) > 0:
        if st.session_state.filters['desa'][0] in desa_list:
            default_index = desa_list.index(st.session_state.filters['desa'][0])
    
    selected_desa = st.sidebar.selectbox(
        "Desa/Kelurahan:",
        desa_list,
        index=default_index,
        help="Pilih desa untuk analisis spesifik atau 'Semua Desa/Kelurahan' untuk melihat semua desa"
    )
    
    # Convert to list format for compatibility with existing code
    if selected_desa == "Semua Desa/Kelurahan":
        st.session_state.filters['desa'] = []
    else:
        st.session_state.filters['desa'] = [selected_desa]
    
    # Info about comparison feature
    st.sidebar.info("💡 Untuk perbandingan antar desa, scroll ke bawah ke bagian 'Perbandingan Antar Desa'")
    
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
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                f"Total {indicator_label}",
                f"{kpis['total']:,}",
                help=f"Total {indicator_label} di seluruh area yang difilter"
            )
        
        with col2:
            st.metric(
                "Desa Terbaik",
                kpis.get('top_village', 'Tidak ada'),
                help="Desa dengan nilai tertinggi"
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
    """Display village comparison with grouped bar chart visualization"""
    
    st.markdown("#### 🔍 **Perbandingan Antar Desa**")
    
    # Village selection with dedicated filter
    available_villages = []
    for _, row in filtered_df.iterrows():
        village_label = f"{row['nama_desa']} ({row['nama_kecamatan']})"
        available_villages.append(village_label)
    
    selected_villages = st.multiselect(
        "Pilih desa untuk dibandingkan (maksimal 4):",
        options=sorted(list(set(available_villages))),
        max_selections=4,
        help="Pilih 2-4 desa untuk perbandingan yang optimal"
    )
    
    if len(selected_villages) < 2:
        st.info("ℹ️ Pilih minimal 2 desa untuk melakukan perbandingan.")
        return
    
    # Get data for selected villages
    selected_village_names = [village.split(' (')[0] for village in selected_villages]
    comparison_df = filtered_df[filtered_df['nama_desa'].isin(selected_village_names)].copy()
    
    if comparison_df.empty:
        st.error("❌ Data tidak ditemukan untuk desa yang dipilih.")
        return
    
    # Get current category indicators
    current_category = None
    current_indicators = {}
    for category, indicators in category_indicators.items():
        for indicator_key in indicator_columns:
            if indicator_key in indicators:
                current_category = category
                current_indicators = indicators
                break
        if current_category:
            break
    
    if not current_indicators:
        st.error("❌ Indikator tidak ditemukan untuk kategori ini.")
        return
    
    # Filter available indicators (only those with data)
    available_indicators = {}
    for key, label in current_indicators.items():
        if key in comparison_df.columns and comparison_df[key].notna().any():
            available_indicators[key] = label
    
    if not available_indicators:
        st.warning("⚠️ Tidak ada indikator dengan data tersedia untuk desa yang dipilih.")
        return
    
    # Indicator selection for comparison
    selected_indicator_keys = st.multiselect(
        "Pilih indikator untuk dibandingkan:",
        options=list(available_indicators.keys()),
        format_func=lambda x: available_indicators[x],
        default=list(available_indicators.keys())[:3] if len(available_indicators) >= 3 else list(available_indicators.keys())
    )
    
    if not selected_indicator_keys:
        st.info("ℹ️ Pilih minimal 1 indikator untuk perbandingan.")
        return
    
    # Create village labels for display
    comparison_df['village_label'] = comparison_df['nama_desa'] + ' (' + comparison_df['nama_kecamatan'] + ')'
    
    # Separate quantitative and qualitative indicators
    quantitative_indicators = []
    qualitative_indicators = []
    
    for key in selected_indicator_keys:
        if key in comparison_df.columns:
            unique_values = comparison_df[key].nunique()
            if unique_values > 10 or comparison_df[key].dtype in ['int64', 'float64']:
                quantitative_indicators.append(key)
            else:
                qualitative_indicators.append(key)
    
    # Display quantitative indicators with grouped bar chart
    if quantitative_indicators:
        st.markdown("#### 📊 **Perbandingan Indikator Kuantitatif**")
        
        # Prepare data for grouped bar chart
        plot_data = []
        for _, row in comparison_df.iterrows():
            for indicator_key in quantitative_indicators:
                if pd.notna(row[indicator_key]):
                    plot_data.append({
                        'Desa': row['village_label'],
                        'Indikator': available_indicators[indicator_key],
                        'Nilai': row[indicator_key],
                        'indicator_key': indicator_key
                    })
        
        if plot_data:
            plot_df = pd.DataFrame(plot_data)
            
            # Create grouped bar chart
            fig = px.bar(
                plot_df,
                x='Desa',
                y='Nilai',
                color='Indikator',
                barmode='group',
                title="Perbandingan Indikator Kuantitatif Antar Desa",
                height=500
            )
            
            fig.update_layout(
                xaxis_title="Desa",
                yaxis_title="Nilai",
                legend_title="Indikator",
                xaxis={'tickangle': 45}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary table for quantitative
            with st.expander("📋 **Tabel Data Kuantitatif**"):
                summary_data = {}
                for _, row in comparison_df.iterrows():
                    village_data = {'Desa': row['village_label']}
                    for key in quantitative_indicators:
                        if pd.notna(row[key]):
                            village_data[available_indicators[key]] = row[key]
                        else:
                            village_data[available_indicators[key]] = "N/A"
                    summary_data[row['village_label']] = village_data
                
                if summary_data:
                    summary_df = pd.DataFrame(list(summary_data.values()))
                    st.dataframe(summary_df, use_container_width=True)
    
    # Display qualitative indicators
    if qualitative_indicators:
        st.markdown("#### 🎯 **Perbandingan Indikator Kualitatif**")
        
        cols = st.columns(min(len(qualitative_indicators), 2))
        
        for i, indicator_key in enumerate(qualitative_indicators):
            with cols[i % 2]:
                st.markdown(f"**{available_indicators[indicator_key]}**")
                
                # Create comparison table for this indicator
                indicator_data = []
                for _, row in comparison_df.iterrows():
                    if pd.notna(row[indicator_key]):
                        indicator_data.append({
                            'Desa': row['village_label'],
                            'Nilai': row[indicator_key]
                        })
                
                if indicator_data:
                    indicator_df = pd.DataFrame(indicator_data)
                    
                    # Create simple bar chart for this qualitative indicator
                    value_counts = indicator_df['Nilai'].value_counts()
                    
                    fig_qual = px.bar(
                        x=indicator_df['Desa'],
                        y=[1] * len(indicator_df),  # Just for visual representation
                        color=indicator_df['Nilai'],
                        title=f"Distribusi: {available_indicators[indicator_key]}",
                        height=300
                    )
                    
                    fig_qual.update_layout(
                        xaxis_title="Desa",
                        yaxis_title="",
                        showlegend=True,
                        yaxis={'showticklabels': False}
                    )
                    
                    st.plotly_chart(fig_qual, use_container_width=True)
                    
                    # Show simple comparison table
                    st.dataframe(indicator_df, use_container_width=True, height=200)
                else:
                    st.info("Tidak ada data tersedia untuk indikator ini.")
    
    # Overall summary
    with st.expander("📊 **Ringkasan Lengkap Perbandingan**"):
        summary_comparison = comparison_df[['village_label'] + selected_indicator_keys].copy()
        summary_comparison.columns = ['Desa'] + [available_indicators[key] for key in selected_indicator_keys]
        st.dataframe(summary_comparison, use_container_width=True)


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
        df, selected_kecamatan, st.session_state.filters['desa'], selected_indicator_key, category_indicators, selected_category
    )
    
    if filtered_df.empty:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih.")
        st.info("💡 Coba ubah filter untuk melihat data.")
        return
    
    # Display KPI cards
    st.subheader("📈 Ringkasan Data")
    display_kpi_cards(kpis, indicator_label)
    
    st.divider()
    
    # Main content: Dynamic Visualization Flow
    if selected_indicator_key == "Semua":
        display_all_indicators_overview(filtered_df, selected_category, category_indicators)
    else:
        display_single_indicator_analysis(filtered_df, selected_indicator_key, indicator_label, category_indicators)
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📅 Data:** Podes 2024 - BPS")
    with col2:
        st.markdown(f"**📊 Total Desa Dianalisis:** {len(filtered_df)}")
    with col3:
        st.markdown(f"**🎯 Kategori:** {selected_category}")


def display_all_indicators_overview(df, category, category_indicators):
    """Display overview of all indicators in a category"""
    st.markdown("### 📊 **Ringkasan Seluruh Indikator**")
    
    indicators = category_indicators[category]
    
    # Split into quantitative and qualitative
    quantitative_indicators = {}
    qualitative_indicators = {}
    
    for key, label in indicators.items():
        if key in df.columns:
            unique_values = df[key].nunique()
            if unique_values > 10 or df[key].dtype in ['int64', 'float64']:
                quantitative_indicators[key] = label
            else:
                qualitative_indicators[key] = label
    
    # Display quantitative indicators
    if quantitative_indicators:
        st.markdown("#### 📈 **Indikator Kuantitatif**")
        for key, label in quantitative_indicators.items():
            with st.expander(f"📊 {label}"):
                create_enhanced_quantitative_visualization(df, key, label)
    
    # Display qualitative indicators  
    if qualitative_indicators:
        st.markdown("#### 📋 **Indikator Kualitatif**")
        for key, label in qualitative_indicators.items():
            with st.expander(f"🎯 {label}"):
                create_enhanced_qualitative_visualization(df, key, label)
    
    # Add village comparison section for all indicators view
    st.markdown("---")
    st.markdown("### 🔍 **Perbandingan Antar Desa**")
    st.info("💡 Fitur ini memungkinkan Anda membandingkan beberapa desa berdasarkan indikator dalam kategori ini.")
    
    # Get all indicator keys for this category
    all_indicator_keys = list(indicators.keys())
    display_village_comparison(df, all_indicator_keys, category_indicators)


def display_single_indicator_analysis(df, indicator_key, indicator_label, category_indicators):
    """Display detailed analysis for a single indicator"""
    st.markdown(f"### 🎯 **Analisis: {indicator_label}**")
    
    if indicator_key not in df.columns:
        st.error(f"Kolom '{indicator_key}' tidak ditemukan dalam data.")
        return
    
    # Determine if indicator is quantitative or qualitative
    unique_values = df[indicator_key].nunique()
    is_quantitative = unique_values > 10 or df[indicator_key].dtype in ['int64', 'float64']
    
    # Display appropriate visualization
    if is_quantitative:
        create_enhanced_quantitative_visualization(df, indicator_key, indicator_label)
    else:
        create_enhanced_qualitative_visualization(df, indicator_key, indicator_label)
    
    # Add village comparison section
    st.markdown("---")
    st.markdown("### 🔍 **Perbandingan Antar Desa**")
    
    # Get all indicator columns for this category
    all_indicators = {}
    for category, indicators in category_indicators.items():
        if indicator_key in indicators:
            all_indicators = indicators
            break
    
    display_village_comparison(df, list(all_indicators.keys()), category_indicators)


def create_quantitative_visualization(df, column, title):
    """Create visualizations for quantitative indicators"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Horizontal bar chart: Top 15 dan Bottom 5
        st.markdown("#### 🏆 **Peringkat Desa**")
        
        # Remove NaN values and sort
        clean_df = df[[column, 'nama_desa', 'nama_kecamatan']].dropna()
        
        if clean_df.empty:
            st.warning(f"⚠️ Tidak ada data yang valid untuk indikator '{title}'")
            return
            
        sorted_df = clean_df.sort_values(column, ascending=False)
        
        # Get top 15 and bottom 5 (or less if data is limited)
        total_data = len(sorted_df)
        
        if total_data == 0:
            st.warning(f"⚠️ Tidak ada data untuk indikator '{title}'")
            return
        elif total_data == 1:
            # Only one record, show it
            combined_df = sorted_df.copy()
            combined_df['label'] = combined_df['nama_desa'] + ' (' + combined_df['nama_kecamatan'] + ')'
            combined_df['color'] = ['Data Tunggal']
            color_map = {'Data Tunggal': '#2E86AB'}
        elif total_data <= 20:
            # If we have 20 or fewer records, show all
            combined_df = sorted_df.copy()
            combined_df['label'] = combined_df['nama_desa'] + ' (' + combined_df['nama_kecamatan'] + ')'
            combined_df['color'] = [f'Semua Data ({total_data})'] * total_data
            color_map = {f'Semua Data ({total_data})': '#2E86AB'}
        else:
            # More than 20 records, show top 15 and bottom 5
            top_15 = sorted_df.head(15)
            bottom_5 = sorted_df.tail(5)
            
            # Combine and create labels
            combined_df = pd.concat([top_15, bottom_5])
            combined_df = combined_df.drop_duplicates()  # Remove any duplicates
            combined_df['label'] = combined_df['nama_desa'] + ' (' + combined_df['nama_kecamatan'] + ')'
            
            # Create color labels based on actual data length
            colors = []
            top_count = len(top_15)
            bottom_count = len(bottom_5)
            
            # Add colors for top entries
            colors.extend(['Top 15'] * top_count)
            # Add colors for bottom entries (only if they're different from top)
            if bottom_count > 0 and len(combined_df) > top_count:
                colors.extend(['Bottom 5'] * (len(combined_df) - top_count))
            
            combined_df['color'] = colors[:len(combined_df)]
            color_map = {'Top 15': '#2E86AB', 'Bottom 5': '#F24236'}
        
        # Create horizontal bar chart
        fig = px.bar(
            combined_df, 
            x=column, 
            y='label',
            color='color',
            orientation='h',
            title=f"Peringkat Desa: {title}",
            color_discrete_map=color_map,
            height=600
        )
        
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title=title,
            yaxis_title="Desa",
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Histogram: Distribution analysis
        st.markdown("#### 📊 **Distribusi Data**")
        
        if clean_df.empty:
            st.warning(f"⚠️ Tidak ada data yang valid untuk distribusi '{title}'")
            return
        
        fig_hist = px.histogram(
            clean_df,
            x=column,
            nbins=min(20, len(clean_df[column].unique()) if len(clean_df[column].unique()) > 1 else 10),
            title=f"Distribusi {title}",
            color_discrete_sequence=['#A23B72']
        )
        
        fig_hist.update_layout(
            xaxis_title=title,
            yaxis_title="Jumlah Desa",
            bargap=0.1
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # Optional data table in expander
    with st.expander("📋 **Lihat Data Lengkap**"):
        display_df = sorted_df[['nama_desa', 'nama_kecamatan', column]].copy()
        display_df['Peringkat'] = range(1, len(display_df) + 1)
        display_df = display_df[['Peringkat', 'nama_desa', 'nama_kecamatan', column]]
        display_df.columns = ['Peringkat', 'Desa', 'Kecamatan', title]
        st.dataframe(display_df, use_container_width=True, height=400)


def create_qualitative_visualization(df, column, title):
    """Create visualizations for qualitative indicators"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Donut chart: Proportions
        st.markdown("#### 🍩 **Proporsi Data**")
        
        # Count values and remove NaN
        value_counts = df[column].value_counts().dropna()
        
        if value_counts.empty:
            st.warning(f"⚠️ Tidak ada data yang valid untuk indikator '{title}'")
            return
        
        # Create donut chart
        fig = go.Figure(data=[go.Pie(
            labels=value_counts.index,
            values=value_counts.values,
            hole=0.4,
            textinfo='label+percent',
            textposition='inside'
        )])
        
        fig.update_layout(
            title=f"Proporsi {title}",
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add summary statistics
        st.markdown("#### 📊 **Ringkasan**")
        total_valid = value_counts.sum()
        st.metric("Total Data Valid", total_valid)
        st.metric("Kategori Unik", len(value_counts))
        
    with col2:
        # Bar chart: Count by category
        st.markdown("#### 📊 **Jumlah per Kategori**")
        
        if value_counts.empty:
            st.warning(f"⚠️ Tidak ada data yang valid untuk grafik '{title}'")
            return
        
        fig_bar = px.bar(
            x=value_counts.index,
            y=value_counts.values,
            title=f"Distribusi {title}",
            color=value_counts.values,
            color_continuous_scale='viridis'
        )
        
        fig_bar.update_layout(
            xaxis_title="Kategori",
            yaxis_title="Jumlah Desa",
            showlegend=False
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Percentage breakdown
        st.markdown("#### 🎯 **Persentase Detail**")
        total_valid = value_counts.sum()
        for category, count in value_counts.items():
            percentage = (count / total_valid) * 100
            st.write(f"**{category}:** {count} desa ({percentage:.1f}%)")
    
    # Optional data table in expander
    with st.expander("📋 **Lihat Data per Desa**"):
        display_df = df[['nama_desa', 'nama_kecamatan', column]].dropna()
        display_df.columns = ['Desa', 'Kecamatan', title]
        
        # Group by category for better organization
        for category in value_counts.index:
            category_df = display_df[display_df[title] == category]
            if not category_df.empty:
                st.markdown(f"**{category}** ({len(category_df)} desa)")
                st.dataframe(category_df, use_container_width=True, height=200)


if __name__ == "__main__":
    main()
