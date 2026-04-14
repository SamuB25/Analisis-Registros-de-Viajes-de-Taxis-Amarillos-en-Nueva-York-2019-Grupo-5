import streamlit as st
from App_taxis_ny.src.query_manager import query_manager
from App_taxis_ny.src.stats_logic import (
    BICKLE_PALETTE, get_accent_color, format_kpi,
    get_average_metrics, get_passenger_distribution, 
    get_usage_frequencies, get_location_ranking
)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NYC Taxi Night Shift", layout="wide")

# Fondo Asphalt Night (#121212) 
st.markdown(
    f"<style>.stApp {{background-color: {BICKLE_PALETTE['asphalt_night']}; color: {BICKLE_PALETTE['vapor_white']};}}</style>", 
    unsafe_allow_html=True
)

# --- INICIALIZACIÓN DE DATOS ("Carga Lazy" guiandose por el archivo enviado por victoria) ---
@st.cache_resource
def init_connection():
    return query_manager()

qm = init_connection()

# --- SIDEBAR (El Control de Travis) ---
with st.sidebar:
    st.title("🚕 Control de Travis") # Silueta minimalista Taxi Yellow 
    tipo_horario = st.radio(
        "Selector de Universo:", 
        ["Vista General", "Hora Pico", "Hora No Pico"]
    )
    mes_filtro = st.selectbox("Filtro de Mes:", ["Todos", "Octubre", "Noviembre", "Diciembre"])
    
    accent = get_accent_color(tipo_horario) # Cambio a Neon Red automático 
    st.markdown(f"<p style='color:{accent}'>Modo Activo: {tipo_horario}</p>", unsafe_allow_html=True)

# --- CABECERA (junto a la metricas de tendencia central---
st.title(f"Dashboard: {tipo_horario}")
kpis = get_average_metrics(qm, tipo_horario, mes_filtro)

col1, col2, col3, col4 = st.columns(4)
# Los números resaltan en Taxi Yellow sobre el fondo oscuro 
col1.metric("Viajes Totales", format_kpi(kpis["total_viajes"]))
col2.metric("Distancia Promedio", f"{format_kpi(kpis['avg_distance'])} mi")
col3.metric("Tarifa Promedio", format_kpi(kpis["avg_fare"], True))
col4.metric("Propina Promedio", format_kpi(kpis["avg_tip"], True))

st.markdown("---")

# --- COMPORTAMIENTO DE LOS PASAJEROS ---
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Distribución de Pasajeros")
    df_pasajeros = get_passenger_distribution(qm, tipo_horario, mes_filtro)
    
    st.bar_chart(df_pasajeros.set_index("Pasajeros"), color=BICKLE_PALETTE["vapor_white"])
   
    st.caption(f"N={format_kpi(kpis['total_viajes'])} registros. Se omitieron valores de 0 pasajeros por inconsistencia operativa.")

with col_der:
    st.subheader("Comportamiento de Pago")
    df_pagos = get_usage_frequencies(qm, tipo_horario, mes_filtro)
    
    st.write("Frecuencia relativa de tipos de pago")
    st.bar_chart(df_pagos.set_index("Categoria"), color=accent)

# --- PIE DE PÁGINA---
st.markdown("---")
st.subheader("📍 Geografía de la Demanda (Top 5 Destinos)")
df_destinos = get_location_ranking(qm, tipo_horario, mes_filtro)
st.table(df_destinos) # Muestra los nombres de las zonas (JFK, Manhattan, etc.)