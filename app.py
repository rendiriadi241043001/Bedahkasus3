import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Analisis Cuaca",
    page_icon="⛅",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('dataset_cuaca_1000.csv')

df = load_data()

st.title("⛅ Dashboard Analisis Pengamatan Cuaca (Bedah Kasus 3)")
st.markdown("Dashboard interaktif ini menyajikan analisis data pengamatan cuaca sintetik sebanyak **1.000 baris** berdasarkan sampel data awal (Jakarta & Bandung), yang mencakup variabel **Kategorik Nominal** (Kondisi & Kota), **Numerik Interval** (Suhu), dan **Numerik Rasio** (Kelembaban).")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
selected_cities = st.sidebar.multiselect("Pilih Kota:", options=df['Kota'].unique(), default=df['Kota'].unique())
selected_conditions = st.sidebar.multiselect("Pilih Kondisi Cuaca:", options=df['Kondisi'].unique(), default=df['Kondisi'].unique())

filtered_df = df[(df['Kota'].isin(selected_cities)) & (df['Kondisi'].isin(selected_conditions))]

# Top Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Pengamatan", f"{len(filtered_df):,} data")
with col2:
    avg_temp = filtered_df['Suhu_C'].mean() if len(filtered_df) > 0 else 0
    st.metric("Rata-rata Suhu", f"{avg_temp:.1f} °C")
with col3:
    avg_hum = filtered_df['Kelembaban_persen'].mean() if len(filtered_df) > 0 else 0
    st.metric("Rata-rata Kelembaban", f"{avg_hum:.1f} %")
with col4:
    max_temp = filtered_df['Suhu_C'].max() if len(filtered_df) > 0 else 0
    st.metric("Suhu Maksimum", f"{max_temp:.1f} °C")

st.divider()

# Row 1: Charts
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🌡️ Perbandingan Suhu Berdasarkan Kota")
    fig_temp = px.box(filtered_df, x='Kota', y='Suhu_C', color='Kota',
                      color_discrete_sequence=['#ff7f0e', '#1f77b4'],
                      labels={'Suhu_C': 'Suhu (°C)', 'Kota': 'Kota'})
    st.plotly_chart(fig_temp, use_container_width=True)

with col_b:
    st.subheader("💧 Perbandingan Kelembaban Berdasarkan Kota")
    fig_hum = px.box(filtered_df, x='Kota', y='Kelembaban_persen', color='Kota',
                     color_discrete_sequence=['#2ca02c', '#d62728'],
                     labels={'Kelembaban_persen': 'Kelembaban (%)', 'Kota': 'Kota'})
    st.plotly_chart(fig_hum, use_container_width=True)

# Row 2: Charts
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("🌤️ Distribusi Kondisi Cuaca")
    cond_counts = filtered_df['Kondisi'].value_counts().reset_index()
    cond_counts.columns = ['Kondisi', 'Jumlah']
    fig_cond = px.pie(cond_counts, names='Kondisi', values='Jumlah', hole=0.4,
                      color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_cond, use_container_width=True)

with col_d:
    st.subheader("📈 Hubungan Suhu vs Kelembaban")
    fig_scatter = px.scatter(filtered_df, x='Suhu_C', y='Kelembaban_persen', color='Kota',
                             symbol='Kondisi', opacity=0.7,
                             labels={'Suhu_C': 'Suhu (°C)', 'Kelembaban_persen': 'Kelembaban (%)'})
    st.plotly_chart(fig_scatter, use_container_width=True)

# Data Table preview
st.subheader("📋 Tabel Data Pengamatan Cuaca")
st.dataframe(filtered_df, use_container_width=True)
