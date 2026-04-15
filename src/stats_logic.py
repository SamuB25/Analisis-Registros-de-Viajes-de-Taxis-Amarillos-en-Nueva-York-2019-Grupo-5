import streamlit as st
import pandas as pd
import plotly.express as px #Se incorpora plotly.express para garantizar gráficos dinámicos 

# 1. PALETA DE COLORES OFICIAL (Bickle Palette) inspirada en Taxi Driver 
BICKLE_PALETTE = {
    "taxi_yellow": "#F2BC1B",
    "asphalt_night": "#121212",
    "vapor_white": "#F2F2F2",
    "neon_red": "#D90404",
    "steel_gray": "#757575"
}

def get_accent_color(tipo_horario):
    """El acento cambia a Neon Red solo en Hora Pico[cite: 15, 56]."""
    return BICKLE_PALETTE["neon_red"] if tipo_horario == "Hora Pico" else BICKLE_PALETTE["taxi_yellow"]

def format_kpi(value, is_money=False):
    """Formatea números para la 'Zona de Despacho'[cite: 57]."""
    if value is None or pd.isna(value): return "0"
    if is_money: return f"$ {value:,.2f}"
    if value >= 1_000_000: return f"{value/1_000_000:.1f}M"
    return f"{int(value):,}" if value > 100 else f"{value:.2f}"

def build_sql_filter(tipo_horario="Vista General", mes="Todos"):
    """Genera el Filtro Maestro basado en el rigor de la UCV[cite: 25, 31, 69]."""
    condiciones = ["1=1"]
    
    if tipo_horario == "Hora Pico":
        # Lun-Vie entre 16:00 y 20:00 [cite: 31]
        condiciones.append("CAST(EXTRACT(DOW FROM CAST(pickup_date AS DATE)) AS INT) BETWEEN 1 AND 5")
        condiciones.append("pickup_time BETWEEN '16:00:00' AND '20:00:00'")
    elif tipo_horario == "Hora No Pico":
        # Fines de semana O fuera del horario pico
        condiciones.append("(CAST(EXTRACT(DOW FROM CAST(pickup_date AS DATE)) AS INT) IN (0, 6) OR pickup_time NOT BETWEEN '16:00:00' AND '20:00:00')")

    meses_map = {"Octubre": 10, "Noviembre": 11, "Diciembre": 12}
    if mes in meses_map:
        condiciones.append(f"EXTRACT(MONTH FROM CAST(pickup_date AS DATE)) = {meses_map[mes]}")
    
    return " AND ".join(condiciones)

# BLOQUE DE AGREGACIONES (Consultas DuckDB con Caching para optimizar la rapidez de la lectura de la app)

@st.cache_data
def get_average_metrics(_qm, tipo_horario, mes):
    """Calcula KPIs robustos"""
    filtro = build_sql_filter(tipo_horario, mes)
    query = f"""
        SELECT 
            COUNT(v.trip_id) as total_viajes,
            AVG(v.trip_distance) as avg_distance,
            AVG(f.fare_amount) as avg_fare,
            AVG(f.tip_amount) as avg_tip
        FROM viaje v
        JOIN finanzas f ON v.trip_id = f.trip_id
        WHERE {filtro} AND f.total_amount > 0
    """
    res = _qm.execute_query(query)
    return res.iloc[0] if not res.empty else {"total_viajes":0, "avg_distance":0, "avg_fare":0, "avg_tip":0}

@st.cache_data
def get_dynamic_insight(kpis, tipo_horario):
    """Genera reseñas interactivas basadas en los datos"""
    if kpis['total_viajes'] == 0: return "No hay datos para este filtro."
    
    if tipo_horario == "Hora Pico":
        return f"🚨 **Alerta de Tráfico:** En horas pico, la propina promedio es de {format_kpi(kpis['avg_tip'], True)}."
    else:
        return f"🌙 **Perfil Nocturno/Weekend:** Los viajes suelen ser más largos ({format_kpi(kpis['avg_distance'])} mi), lo que indica desplazamientos hacia zonas residenciales."

@st.cache_data
def get_location_ranking(_qm, tipo_horario, mes, top=True):
    """Top 5 Destinos más frecuentados"""
    filtro = build_sql_filter(tipo_horario, mes)
    orden = "DESC" if top else "ASC"
    query = f"""
        SELECT l.zone as Zona, COUNT(*) as Frecuencia
        FROM viaje v
        JOIN localizacion l ON v.do_location_id = l.location_id
        WHERE {filtro}
        GROUP BY 1 ORDER BY 2 {orden} LIMIT 5
    """
    return _qm.execute_query(query)
