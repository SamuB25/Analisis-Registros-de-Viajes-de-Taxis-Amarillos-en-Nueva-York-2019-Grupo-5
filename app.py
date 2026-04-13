import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Configuración de rutas para que encuentre query_manager
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

# Imports de tus módulos internos
from App_taxis_ny.src.query_manager import query_manager
from App_taxis_ny.src.stats_logic import (BICKLE_PALETTE, get_accent_color, 
                                          format_kpi, build_sql_filter)

st.set_page_config(page_title="NYC Taxi Night Shift", layout="wide")

# --- LÓGICA DE DATOS (Antes en stats_logic.py) ---

@st.cache_resource
def get_qm():
    return query_manager()

@st.cache_data
def get_average_metrics(tipo_horario, mes):
    qm = get_qm()
    filtro = build_sql_filter(tipo_horario, mes)
    query = f"""
        SELECT COUNT(r.trip_id) as total_viajes, AVG(r.trip_distance) as avg_distance,
               AVG(f.fare_amount) as avg_fare, AVG(f.tip_amount) as avg_tip
        FROM registro_viajes r JOIN finanzas_viaje f ON r.trip_id = f.trip_id
        WHERE {filtro} AND f.total_amount > 0
    """
    return qm.execute_query(query).iloc[0]

@st.cache_data
def get_passenger_distribution(tipo_horario, mes):
    qm = get_qm()
    filtro = build_sql_filter(tipo_horario, mes)
    query = f"SELECT passenger_count as Pasajeros, COUNT(*) as Frecuencia FROM registro_viajes WHERE {filtro} AND passenger_count > 0 GROUP BY 1"
    return qm.execute_query(query)

@st.cache_data
def get_usage_frequencies(variable, tipo_horario, mes):
    qm = get_qm()
    filtro = build_sql_filter(tipo_horario, mes)
    tabla = "metodo_pago" if variable == "payment_type" else "tarifas"
    id_col = "payment_type_id" if variable == "payment_type" else "rate_code_id"
    query = f"""
        SELECT t.descripcion as Categoria, COUNT(*) as Frecuencia 
        FROM finanzas_viaje f JOIN {tabla} t ON f.{id_col} = t.{id_col}
        WHERE {filtro} GROUP BY 1
    """
    return qm.execute_query(query)

# --- FUNCIONES DE GRÁFICOS ---

def plot_passenger_distribution(df, tipo_horario):
    fig = px.bar(df, x='Pasajeros', y='Frecuencia', title="Distribución de Pasajeros",
                 color_discrete_sequence=[get_accent_color(tipo_horario)])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    return fig

def plot_payment_donut(df, tipo_horario):
    colores = [get_accent_color(tipo_horario), BICKLE_PALETTE["steel_gray"], BICKLE_PALETTE["vapor_white"]]
    fig = px.pie(df, names='Categoria', values='Frecuencia', hole=0.6, title="Métodos de Pago", color_discrete_sequence=colores)
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    return fig

# --- INTERFAZ (UI) ---

st.sidebar.title("🚕 Control de Travis")
tipo_horario = st.sidebar.radio("Selector de Universo:", ["Vista General", "Hora Pico", "Hora No Pico"])
mes_filtro = st.sidebar.selectbox("Filtro de Mes:", ["Todos", "Octubre", "Noviembre", "Diciembre"])

# Cálculos
kpis = get_average_metrics(tipo_horario, mes_filtro)
df_pasajeros = get_passenger_distribution(tipo_horario, mes_filtro)
df_pagos = get_usage_frequencies("payment_type", tipo_horario, mes_filtro)

# Renderizado
st.title(f"Dashboard: {tipo_horario}")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Viajes Totales", format_kpi(kpis["total_viajes"]))
c2.metric("Distancia Promedio", f"{format_kpi(kpis['avg_distance'])} mi")
c3.metric("Tarifa Promedio", format_kpi(kpis["avg_fare"], True))
c4.metric("Propina Promedio", format_kpi(kpis["avg_tip"], True))

st.markdown("---")
col_izq, col_der = st.columns(2)
with col_izq:
    st.plotly_chart(plot_passenger_distribution(df_pasajeros, tipo_horario), use_container_width=True)
with col_der:
    st.plotly_chart(plot_payment_donut(df_pagos, tipo_horario), use_container_width=True)