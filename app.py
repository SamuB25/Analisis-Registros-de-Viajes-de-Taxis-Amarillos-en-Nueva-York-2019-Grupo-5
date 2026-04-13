from App_taxis_ny.src.query_manager import query_manager
import streamlit as st
# from src.drive_conn import asegurar_datos_locales # Descomentar cuando integres Drive
from App_taxis_ny.src.stats_logic import (get_average_metrics, get_passenger_distribution, 
                             get_usage_frequencies, get_location_ranking,
                             plot_passenger_distribution, plot_payment_donut, plot_location_ranking)
from App_taxis_ny.src.utils import format_kpi

st.set_page_config(page_title="NYC Taxi Night Shift", layout="wide")

# 1. Carga Lazy (Asegurar Parquets)
# asegurar_datos_locales() 

# 2. Sidebar (Filtro Maestro)
st.sidebar.title("🚕 Control de Travis")
tipo_horario = st.sidebar.radio("Selector de Universo:", 
                                ["Vista General", "Hora Pico", "Hora No Pico"])
mes_filtro = st.sidebar.selectbox("Filtro de Mes:", 
                                  ["Todos", "Octubre", "Noviembre", "Diciembre"])

# 3. Llamada de Cálculos (Cálculo Bajo Demanda)
kpis = get_average_metrics(tipo_horario, mes_filtro)
df_pasajeros = get_passenger_distribution(tipo_horario, mes_filtro)
df_pagos = get_usage_frequencies("payment_type", tipo_horario, mes_filtro)
df_destinos = get_location_ranking(top=True, tipo_horario=tipo_horario, mes=mes_filtro)

# 4. Renderizado Limpio (La Zona de Despacho)
# Si es Hora Pico, Streamlit cambiará el estilo automáticamente por las variables de stats_logic
st.title(f"Dashboard: {tipo_horario}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Viajes Totales", format_kpi(kpis["total_viajes"]))
col2.metric("Distancia Promedio", format_kpi(kpis["avg_distance"])+ " mi")
col3.metric("Tarifa Promedio", format_kpi(kpis["avg_fare"], True))
col4.metric("Propina Promedio", format_kpi(kpis["avg_tip"], True))

# Cuerpo Central
st.markdown("---")
c_izq, c_der = st.columns(2)

with c_izq:
    st.plotly_chart(plot_passenger_distribution(df_pasajeros, tipo_horario), use_container_width=True)
    st.caption("Nota: Se omitieron valores de 0 pasajeros por inconsistencia operativa.")

with c_der:
    st.plotly_chart(plot_payment_donut(df_pagos, tipo_horario), use_container_width=True)

# Pie de Página
st.plotly_chart(plot_location_ranking(df_destinos, tipo_horario, top=True), use_container_width=True)