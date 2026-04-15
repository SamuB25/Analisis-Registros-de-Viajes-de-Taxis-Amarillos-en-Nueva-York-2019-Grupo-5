import streamlit as st
import pandas as pd
import plotly.express as px
from src.drive_conn import preparar_data_lake # Importaciones de tus módulos de la carpeta src
from src.query_manager import get_query_manager
from src.stats_logic import (
    BICKLE_PALETTE,          # Los colores oficiales
    get_accent_color,        # El cambio a rojo en hora pico
    format_kpi,              # Formato de moneda y miles
    get_average_metrics,     # Los 4 números principales del tope
    get_location_ranking,    # La tabla del Top 5 destinos
    get_dynamic_insight,     # La reseña del asistente
    get_passenger_distribution, # El gráfico de barras de pasajeros
    get_usage_frequencies       # El gráfico de métodos de pago
)

st.set_page_config(
    page_title="NYC Taxi Insights - Grupo 5",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def init_connection():
    # Paso 1: Asegura que los parquets existan (Sin esto, DuckDB muere)
    if preparar_data_lake():
        return get_query_manager()
    return None

qm = init_connection()

if qm is None:
    st.error("❌ Error Crítico: No se pudieron sincronizar los datos del Drive.")
    st.stop()

# --- SIDEBAR (El Control de Travis) ---
with st.sidebar:
    st.title("🚕 Control de Travis") # Inspirado en la estética Checker Cab
    tipo_horario = st.radio(
        "Selector de Universo:", 
        ["Vista General", "Hora Pico", "Hora No Pico"]
    )
    mes_filtro = st.selectbox("Filtro de Mes:", ["Todos", "Octubre", "Noviembre", "Diciembre"])
    
    accent = get_accent_color(tipo_horario) # Cambio a Neon Red en Hora Pico
    st.markdown(f"<p style='color:{accent}; font-weight:bold;'>Modo Activo: {tipo_horario}</p>", unsafe_allow_html=True)

# --- CABECERA (Métricas de Tendencia Central) ---
st.title(f"Dashboard: {tipo_horario}")
kpis = get_average_metrics(qm, tipo_horario, mes_filtro)

col1, col2, col3, col4 = st.columns(4)
# Números en Taxi Yellow sobre el fondo oscuro
col1.metric("Viajes Totales", format_kpi(kpis["total_viajes"]))
col2.metric("Distancia Promedio", f"{format_kpi(kpis['avg_distance'])} mi")
col3.metric("Tarifa Promedio", format_kpi(kpis["avg_fare"], True))
col4.metric("Propina Promedio", format_kpi(kpis["avg_tip"], True))

# Reseña Interactiva (Insight dinámico del perfil)
st.chat_message("assistant").write(get_dynamic_insight(kpis, tipo_horario))

st.markdown("---")

# --- COMPORTAMIENTO DE LOS PASAJEROS ---
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Distribución de Pasajeros")
    df_pasajeros = get_passenger_distribution(qm, tipo_horario, mes_filtro)
    st.bar_chart(df_pasajeros.set_index("Pasajeros"), color=BICKLE_PALETTE["vapor_white"])
    st.caption(f"N={format_kpi(kpis['total_viajes'])} registros. Filtro de integridad aplicado.")

with col_der:
    st.subheader("Comportamiento de Pago")
    df_pagos = get_usage_frequencies(qm, tipo_horario, mes_filtro)
    st.write("Frecuencia relativa de tipos de pago")
    st.bar_chart(df_pagos.set_index("Categoria"), color=accent)
    st.caption("*Nota: Los viajes con tarifa de $0 fueron removidos por limpieza de datos.*")

# --- GEOGRAFÍA (Pie de Página) ---
st.markdown("---")
st.subheader("📍 Geografía de la Demanda (Top 5 Destinos)")
df_destinos = get_location_ranking(qm, tipo_horario, mes_filtro)
st.table(df_destinos)