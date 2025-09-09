"""
Enhanced visualization functions with simplified ranking system
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_enhanced_quantitative_visualization(df, column, title):
    """Create enhanced visualizations with si        with perf_cols[0    with col2:   most_common = value_counts.index[0]
            st.metric("👑 Kategori Dominan", f"{most_common}")
        
        with perf_cols[1]:
            most_common_count = value_counts.iloc[0]
            most_common_pct = (most_common_count / total_valid * 100).round(1)
            st.metric("📈 Persentase Dominan", f"{most_common_pct}%")
        
        with perf_cols[2]:
            st.metric("🎯 Total Kategori", len(value_counts))
            
        with perf_cols[3]:
            st.metric("🏘️ Total Desa", total_desa)
        
        with perf_cols[4]:
            st.metric("📊 Desa dengan Data", total_valid) ranking system"""
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
        
        # Single row with 5 columns for compact display
        stat_cols = st.columns(5)
        
        with stat_cols[0]:
            st.metric("🎯 Tertinggi", f"{int(stats['max'])}")
        
        with stat_cols[1]:
            st.metric("📉 Terendah", f"{int(stats['min'])}")
        
        with stat_cols[2]:
            total_value = clean_df[column].sum()
            st.metric("🔢 Total", f"{int(total_value)}")
            
        with stat_cols[3]:
            st.metric("🏘️ Total Desa", total_desa)
        
        with stat_cols[4]:
            st.metric("📊 Desa dengan Data", len(clean_df))
    
    with col2:
        st.markdown("#### 📈 **Analisis Distribusi**")
        
        # Always use value counts for better representation of discrete data
        value_dist = clean_df[column].value_counts().sort_index()
        
        if unique_values <= 10:
            # Create user-friendly labels for X-axis
            x_labels = []
            x_values = value_dist.index.tolist()
            
            # Check if data is binary (0,1) or small counts
            is_binary = set(x_values) <= {0, 1}
            is_small_counts = all(isinstance(x, (int, float)) and x >= 0 and x <= 20 for x in x_values)
            
            if is_binary:
                # For binary data (0,1), use meaningful labels
                x_labels = ['Tidak Ada' if x == 0 else 'Ada' for x in x_values]
            elif is_small_counts and all(isinstance(x, (int, float)) and x == int(x) for x in x_values):
                # For small integer counts, add specific unit description based on column name
                if 'puskesmas' in column.lower():
                    x_labels = [f"{int(x)} puskesmas" if x != 1 else f"{int(x)} puskesmas" for x in x_values]
                elif 'rumah_sakit' in column.lower() or 'rs_' in column.lower():
                    x_labels = [f"{int(x)} rumah sakit" if x != 1 else f"{int(x)} rumah sakit" for x in x_values]
                elif 'dokter' in column.lower():
                    x_labels = [f"{int(x)} dokter" if x != 1 else f"{int(x)} dokter" for x in x_values]
                elif 'bidan' in column.lower():
                    x_labels = [f"{int(x)} bidan" if x != 1 else f"{int(x)} bidan" for x in x_values]
                elif 'apotek' in column.lower():
                    x_labels = [f"{int(x)} apotek" if x != 1 else f"{int(x)} apotek" for x in x_values]
                elif 'posyandu' in column.lower():
                    x_labels = [f"{int(x)} posyandu" if x != 1 else f"{int(x)} posyandu" for x in x_values]
                elif 'tk' in column.lower():
                    x_labels = [f"{int(x)} TK" if x != 1 else f"{int(x)} TK" for x in x_values]
                elif 'sd' in column.lower():
                    x_labels = [f"{int(x)} SD" if x != 1 else f"{int(x)} SD" for x in x_values]
                elif 'smp' in column.lower():
                    x_labels = [f"{int(x)} SMP" if x != 1 else f"{int(x)} SMP" for x in x_values]
                elif 'sma' in column.lower():
                    x_labels = [f"{int(x)} SMA" if x != 1 else f"{int(x)} SMA" for x in x_values]
                elif 'smk' in column.lower():
                    x_labels = [f"{int(x)} SMK" if x != 1 else f"{int(x)} SMK" for x in x_values]
                elif 'pasar' in column.lower():
                    x_labels = [f"{int(x)} pasar" if x != 1 else f"{int(x)} pasar" for x in x_values]
                elif 'bank' in column.lower():
                    x_labels = [f"{int(x)} bank" if x != 1 else f"{int(x)} bank" for x in x_values]
                elif 'koperasi' in column.lower():
                    x_labels = [f"{int(x)} koperasi" if x != 1 else f"{int(x)} koperasi" for x in x_values]
                elif 'jumlah' in column.lower():
                    # Generic fallback for other "jumlah" columns
                    x_labels = [f"{int(x)} unit" if x != 1 else f"{int(x)} unit" for x in x_values]
                else:
                    x_labels = [str(int(x)) for x in x_values]
            else:
                x_labels = [str(x) for x in x_values]
            
            # For discrete data (like counts), use bar chart
            fig_dist = px.bar(
                x=x_labels,
                y=value_dist.values,
                title=f"Distribusi {title}",
                color_discrete_sequence=['#A23B72'],
                text=value_dist.values
            )
            
            fig_dist.update_traces(texttemplate='%{text} desa', textposition='outside')
            fig_dist.update_layout(
                xaxis_title=title,
                yaxis_title="Jumlah Desa"
            )
            
            st.plotly_chart(fig_dist, use_container_width=True)
        else:
            # For continuous data with many values, use histogram
            fig_hist = px.histogram(
                clean_df,
                x=column,
                nbins=min(15, unique_values),
                title=f"Distribusi {title}",
                color_discrete_sequence=['#A23B72']
            )
            
            fig_hist.update_layout(
                xaxis_title=title,
                yaxis_title="Jumlah Desa",
                bargap=0.1
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
    
    # Enhanced data table with ranking
    with st.expander("📋 **Tabel Lengkap dengan Ranking**"):
        # Prepare simplified display with ranking
        table_df = sorted_df[['rank', 'nama_desa', 'nama_kecamatan', column]].copy()
        table_df.columns = ['Rank', 'Desa', 'Kecamatan', title]
        
        # Configure column widths for better display
        column_config = {
            'Rank': st.column_config.NumberColumn(
                'Rank',
                width='small',  # Make rank column narrow
                format='%d'
            ),
            'Desa': st.column_config.TextColumn(
                'Desa',
                width='medium'
            ),
            'Kecamatan': st.column_config.TextColumn(
                'Kecamatan', 
                width='medium'
            ),
            title: st.column_config.NumberColumn(
                title,
                width='small'
            )
        }
        
        st.dataframe(
            table_df, 
            use_container_width=True, 
            height=400, 
            hide_index=True,
            column_config=column_config
        )
        
        # Add insights
        st.markdown("**💡 Insights:**")
        top_performer = table_df.iloc[0]
        
        # Format insights based on data type
        if 'jumlah' in column.lower():
            # Check if binary data (0,1 only)
            all_values = table_df[title].unique()
            is_binary = set(all_values) <= {0, 1}
            
            if is_binary:
                if int(top_performer[title]) == 1:
                    st.write(f"🏆 **Memiliki Fasilitas:** {top_performer['Desa']} ({top_performer['Kecamatan']})")
                else:
                    st.write(f"📊 **Semua desa tidak memiliki fasilitas ini**")
            else:
                # Get specific unit based on column name
                if 'puskesmas' in column.lower():
                    unit = 'puskesmas'
                elif 'rumah_sakit' in column.lower() or 'rs_' in column.lower():
                    unit = 'rumah sakit'
                elif 'dokter' in column.lower():
                    unit = 'dokter'
                elif 'bidan' in column.lower():
                    unit = 'bidan'
                elif 'apotek' in column.lower():
                    unit = 'apotek'
                elif 'posyandu' in column.lower():
                    unit = 'posyandu'
                elif 'tk' in column.lower():
                    unit = 'TK'
                elif 'sd' in column.lower():
                    unit = 'SD'
                elif 'smp' in column.lower():
                    unit = 'SMP'
                elif 'sma' in column.lower():
                    unit = 'SMA'
                elif 'smk' in column.lower():
                    unit = 'SMK'
                elif 'pasar' in column.lower():
                    unit = 'pasar'
                elif 'bank' in column.lower():
                    unit = 'bank'
                elif 'koperasi' in column.lower():
                    unit = 'koperasi'
                else:
                    unit = 'unit'
                
                st.write(f"🏆 **Terbanyak:** {top_performer['Desa']} ({top_performer['Kecamatan']}) dengan {int(top_performer[title])} {unit}")
                
                if len(table_df) > 1:
                    bottom_performer = table_df.iloc[-1]
                    if int(bottom_performer[title]) == 0:
                        st.write(f"📊 **Belum Memiliki:** {bottom_performer['Desa']} ({bottom_performer['Kecamatan']})")
                    else:
                        st.write(f"📊 **Tersedikit:** {bottom_performer['Desa']} ({bottom_performer['Kecamatan']}) dengan {int(bottom_performer[title])} {unit}")
        else:
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
        
        # Enhanced statistics section with balanced layout
        st.markdown("#### 📊 **Statistik Kunci & Ringkasan Data**")
        
        # Get total desa from original dataframe
        total_desa = len(df)
        
        # First row - performance metrics (2 columns)
        perf_cols = st.columns(5)
        with perf_cols[0]:
            most_common = value_counts.index[0]
            most_common_count = value_counts.iloc[0]
            st.metric("� Kategori Dominan", f"{most_common}")
        
        with perf_cols[1]:
            most_common_pct = (most_common_count / total_valid * 100).round(1)
            st.metric("📈 Persentase Dominan", f"{most_common_pct}%")
        
        # Second row - summary metrics (3 columns for better balance)
        summary_cols = st.columns(3)
        with summary_cols[0]:
            st.metric("🎯 Total Kategori", len(value_counts))
            
        with summary_cols[1]:
            st.metric("🏘️ Total Desa", total_desa)
        
        with summary_cols[2]:
            st.metric("� Desa dengan Data", total_valid)

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
                
                # Configure column widths for qualitative data
                qual_column_config = {
                    'Desa': st.column_config.TextColumn(
                        'Desa',
                        width='medium'
                    ),
                    'Kecamatan': st.column_config.TextColumn(
                        'Kecamatan', 
                        width='medium'
                    ),
                    title: st.column_config.TextColumn(
                        title,
                        width='medium'
                    )
                }
                
                st.dataframe(
                    category_df, 
                    use_container_width=True, 
                    height=150,
                    hide_index=True,
                    column_config=qual_column_config
                )
                st.write("")  # Space between categories
        
        # Summary by kecamatan
        if 'nama_kecamatan' in df.columns:
            st.markdown("**📊 Ringkasan per Kecamatan:**")
            kec_summary = df.groupby('nama_kecamatan')[column].value_counts().unstack(fill_value=0)
            if not kec_summary.empty:
                st.dataframe(kec_summary, use_container_width=True)
