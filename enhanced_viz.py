"""
Enhanced visualization functions with simplified ranking system
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_enhanced_quantitative_visualization(df, column, title):
    """Create enhanced visualizations with simplified ranking system"""
    # Remove NaN values and check data availability
    clean_df = df[[column, 'nama_desa', 'nama_kecamatan']].dropna()
    
    if clean_df.empty:
        st.warning(f"⚠️ Tidak ada data valid untuk indikator '{title}'")
        return
    
    # Calculate enhanced metrics
    unique_values = clean_df[column].nunique()
    total_desa = len(clean_df)
    
    # Create ranking with additional context
    sorted_df = clean_df.sort_values(column, ascending=False)
    sorted_df = sorted_df.copy()
    sorted_df['rank'] = range(1, len(sorted_df) + 1)
    
    max_val = clean_df[column].max()
    min_val = clean_df[column].min()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 **Ranking Desa**")
        
        if unique_values == 1:
            # Special handling for uniform data
            st.info(f"✨ Semua desa memiliki nilai seragam: **{clean_df[column].iloc[0]}**")
            
            # Create a simple visualization showing all desa with same value
            fig = px.bar(
                x=[clean_df[column].iloc[0]] * len(clean_df),
                y=[f"{row['nama_desa']}" for _, row in clean_df.iterrows()],
                orientation='h',
                title=f"Nilai Seragam: {title}",
                color_discrete_sequence=['#2E86AB']
            )
            fig.update_layout(
                xaxis_title=title,
                yaxis_title="Desa",
                height=max(300, total_desa * 25),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            # Enhanced ranking visualization
            # Show top performers
            display_df = sorted_df.head(min(12, total_desa)).copy()
            display_df['label'] = (display_df['nama_desa'] + 
                                  ' (' + display_df['nama_kecamatan'] + ')\n' +
                                  'Rank #' + display_df['rank'].astype(str))
            
            # Reverse the order so rank #1 appears at the top
            display_df = display_df.iloc[::-1]
            
            fig = px.bar(
                display_df,
                x=column,
                y='label',
                orientation='h',
                title=f"Ranking Teratas: {title}",
                color_discrete_sequence=['#2E86AB'],
                height=max(400, len(display_df) * 35)
            )
            
            fig.update_layout(
                xaxis_title=f"{title} (Nilai)",
                yaxis_title="Desa",
                yaxis={'categoryorder': 'array', 'categoryarray': display_df['label'].tolist()},
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Statistical insights and data summary
        st.markdown("#### 📊 **Statistik Kunci & Ringkasan Data**")
        stats = clean_df[column].describe()
        
        # First row - main statistics
        stat_cols = st.columns(3)
        with stat_cols[0]:
            st.metric("🎯 Tertinggi", f"{int(stats['max'])}")
        
        with stat_cols[1]:
            st.metric("📉 Terendah", f"{int(stats['min'])}")
        
        with stat_cols[2]:
            total_value = clean_df[column].sum()
            st.metric("🔢 Total", f"{int(total_value)}")
        
        # Second row - data summary
        summary_cols = st.columns(3)
        with summary_cols[0]:
            st.metric("🏘️ Total Desa", total_desa)
        
        with summary_cols[1]:
            st.metric("📊 Desa dengan Data", len(clean_df))
        
        with summary_cols[2]:
            st.metric("🔢 Variasi Nilai", unique_values)
    
    with col2:
        st.markdown("#### 📈 **Analisis Distribusi**")
        
        if unique_values > 2:
            # Distribution chart
            fig_dist = px.histogram(
                clean_df,
                x=column,
                nbins=min(10, unique_values),
                title=f"Distribusi {title}",
                color_discrete_sequence=['#A23B72']
            )
            
            fig_dist.update_layout(
                xaxis_title=title,
                yaxis_title="Jumlah Desa",
                bargap=0.1
            )
            
            st.plotly_chart(fig_dist, use_container_width=True)
        else:
            # Simple value distribution
            value_dist = clean_df[column].value_counts()
            fig_simple = px.bar(
                x=value_dist.index,
                y=value_dist.values,
                title=f"Distribusi Nilai: {title}",
                color_discrete_sequence=['#A23B72']
            )
            
            fig_simple.update_layout(
                xaxis_title=title,
                yaxis_title="Jumlah Desa"
            )
            
            st.plotly_chart(fig_simple, use_container_width=True)
    
    # Enhanced data table with ranking
    with st.expander("📋 **Tabel Lengkap dengan Ranking**"):
        # Prepare simplified display with ranking
        table_df = sorted_df[['rank', 'nama_desa', 'nama_kecamatan', column]].copy()
        table_df.columns = ['Rank', 'Desa', 'Kecamatan', title]
        
        st.dataframe(table_df, use_container_width=True, height=400, hide_index=True)
        
        # Add insights
        st.markdown("**💡 Insights:**")
        top_performer = table_df.iloc[0]
        st.write(f"🏆 **Peringkat Teratas:** {top_performer['Desa']} ({top_performer['Kecamatan']}) dengan nilai {top_performer[title]}")
        
        if len(table_df) > 1:
            bottom_performer = table_df.iloc[-1]
            st.write(f"📈 **Potensi Pengembangan:** {bottom_performer['Desa']} ({bottom_performer['Kecamatan']}) dengan nilai {bottom_performer[title]}")


def create_enhanced_qualitative_visualization(df, column, title):
    """Create enhanced visualizations for qualitative indicators"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced donut chart with better styling
        st.markdown("#### 🍩 **Distribusi Kategori**")
        
        # Count values and remove NaN
        value_counts = df[column].value_counts().dropna()
        
        if value_counts.empty:
            st.warning(f"⚠️ Tidak ada data valid untuk '{title}'")
            return
        
        total_valid = value_counts.sum()
        
        # Create donut chart with Go for better control
        colors = px.colors.qualitative.Set3[:len(value_counts)]
        
        fig = go.Figure(data=[go.Pie(
            labels=value_counts.index,
            values=value_counts.values,
            hole=.4,
            marker_colors=colors,
            textinfo='label+percent+value',
            texttemplate='%{label}<br>%{value} desa<br>(%{percent})'
        )])
        
        fig.update_layout(
            title=f"Distribusi {title}",
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.01),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary metrics
        st.markdown("#### 📊 **Ringkasan Kategori**")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.metric("🎯 Total Kategori", len(value_counts))
            st.metric("📊 Total Data Valid", total_valid)
        
        with col_b:
            most_common = value_counts.index[0]
            most_common_pct = (value_counts.iloc[0] / total_valid * 100).round(1)
            st.metric("👑 Kategori Dominan", most_common)
            st.metric("📈 Persentase Dominan", f"{most_common_pct}%")

    with col2:
        # Enhanced bar chart with ranking
        st.markdown("#### 📊 **Ranking Kategori**")
        
        # Create ranking bar chart with proper ordering
        # Sort in descending order (highest count first)
        sorted_counts = value_counts.sort_values(ascending=False)
        
        fig_bar = px.bar(
            x=sorted_counts.values,
            y=sorted_counts.index,
            orientation='h',
            title=f"Jumlah Desa per Kategori: {title}",
            color=sorted_counts.values,
            color_continuous_scale='viridis',
            text=sorted_counts.values
        )
        
        # Reverse order so highest count appears at top
        y_categories = sorted_counts.index.tolist()
        y_categories.reverse()
        
        fig_bar.update_traces(texttemplate='%{text} desa', textposition='outside')
        fig_bar.update_layout(
            xaxis_title="Jumlah Desa",
            yaxis_title="Kategori",
            showlegend=False,
            yaxis={'categoryorder': 'array', 'categoryarray': y_categories}
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Geographic distribution by kecamatan
        st.markdown("#### 🗺️ **Distribusi per Kecamatan**")
        
        if 'nama_kecamatan' in df.columns:
            # Cross-tabulation
            crosstab = pd.crosstab(df['nama_kecamatan'], df[column], margins=True)
            
            # Create stacked bar chart
            fig_stack = px.bar(
                crosstab.iloc[:-1, :-1],  # Exclude margins
                title=f"Distribusi {title} per Kecamatan",
                color_discrete_sequence=colors
            )
            
            fig_stack.update_layout(
                xaxis_title="Kecamatan",
                yaxis_title="Jumlah Desa",
                legend_title=title
            )
            
            st.plotly_chart(fig_stack, use_container_width=True)
        
    # Enhanced data table with geographic context
    with st.expander("📋 **Data Detail per Desa**"):
        # Group by category for better organization
        for category in value_counts.index:
            category_df = df[df[column] == category][['nama_desa', 'nama_kecamatan', column]].copy()
            category_df.columns = ['Desa', 'Kecamatan', title]
            
            if not category_df.empty:
                st.markdown(f"**{category}** ({len(category_df)} desa)")
                st.dataframe(category_df, use_container_width=True, height=150)
                st.write("")  # Space between categories
        
        # Summary by kecamatan
        if 'nama_kecamatan' in df.columns:
            st.markdown("**📊 Ringkasan per Kecamatan:**")
            kec_summary = df.groupby('nama_kecamatan')[column].value_counts().unstack(fill_value=0)
            if not kec_summary.empty:
                st.dataframe(kec_summary, use_container_width=True)
