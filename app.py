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
    get_location_analysis,    # La tabla del Top 5 destinos
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


st.subheader("📍 Geografía de la Demanda: Análisis de Destinos")

col_controles, _ = st.columns([1, 2])
with col_controles:
    ver_top = st.toggle(
        "Ver destinos más frecuentados", 
        value=True, 
        help="Activa para ver el TOP, desactiva para ver las zonas con menor demanda."
    )

# Llamamos a la función 
tipo_ranking = "Más Frecuentados" if ver_top else "Menos Frecuentados"
df_destinos = get_location_analysis(qm, tipo_horario, mes_filtro, top=ver_top)

if not df_destinos.empty:
    tab1, tab2 = st.tabs(["📊 Distribución de Frecuencias", "📑 Tabla de Datos"])
    
    with tab1:
        # Forzamos que el rango de la escala siempre empiece en 0
        max_rel = df_destinos["f_relativa"].max()
        
        fig = px.bar(
            df_destinos,
            x="f_absoluta",
            y="Zona",
            orientation='h',
            title=f"Distribución de Destinos: {tipo_ranking}",
            labels={
                "f_absoluta": "Frecuencia Absoluta (fi)", 
                "Zona": "Zona de Destino",
                "f_relativa": "Frecuencia Relativa (%)"
            },
            color="f_relativa",
            color_continuous_scale="Viridis" if ver_top else "Reds",
            # SOLUCIÓN AL % NEGATIVO: Definimos el rango manualmente
            range_color=[0, max_rel if max_rel > 0 else 1], 
            text="f_relativa"
        )
        
        # SOLUCIÓN AL "0%": Aumentamos la precisión a 4 decimales para que se vean los valores reales en destinos poco frecuentes
        fig.update_traces(texttemplate='%{text:.4f}%', textposition='outside')
        
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending' if ver_top else 'total descending'},
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.write(f"### Cuadro de Distribución ($f_i$ y $h_i$): {tipo_ranking}")
        df_vista = df_destinos.rename(columns={
            "f_absoluta": "Frecuencia Absoluta (fi)",
            "f_relativa": "Frecuencia Relativa (%)"
        })
        st.dataframe(
            df_vista.style.format({"Frecuencia Relativa (%)": "{:.4f}%"}), # Más precisión aquí también
            use_container_width=True,
            hide_index=True
        )