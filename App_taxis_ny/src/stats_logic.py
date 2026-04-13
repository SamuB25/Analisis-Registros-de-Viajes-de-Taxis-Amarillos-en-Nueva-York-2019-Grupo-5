# src/stats_logic.py
import streamlit as st
import pandas as pd
import plotly.express as px
from App_taxis_ny.src.query_manager import query_manager
from App_taxis_ny.src.utils import build_sql_filter, BICKLE_PALETTE, get_accent_color

# Instanciamos la conexión a DuckDB de forma global para este módulo
@st.cache_resource
def get_qm():
    return query_manager()

# ==========================================
# A. BLOQUE DE MEDIDAS DE TENDENCIA CENTRAL
# ==========================================

@st.cache_data
def get_average_metrics(tipo_horario="Vista General", mes="Todos"):
    """Calcula promedios generales para las tarjetas KPI."""
    qm = get_qm()
    filtro = build_sql_filter(tipo_horario, mes)
    
    query = f"""
        SELECT 
            COUNT(r.trip_id) AS total_viajes,
            AVG(r.trip_distance) AS avg_distance,
            AVG(f.fare_amount) AS avg_fare,
            AVG(f.tip_amount) AS avg_tip
        FROM registro_viajes r
        JOIN finanzas_viaje f ON r.trip_id = f.trip_id
        WHERE {filtro} AND f.total_amount > 0
    """
    df = qm.execute_query(query)
    # Si no hay datos, devolvemos un diccionario en 0
    if df.empty or pd.isna(df['total_viajes'][0]):
        return {"total_viajes": 0, "avg_distance": 0.0, "avg_fare": 0.0, "avg_tip": 0.0}
    return df.iloc[0].to_dict()

# ==========================================
# B. BLOQUE DE FRECUENCIAS Y DISTRIBUCIONES
# ==========================================

@st.cache_data
def get_usage_frequencies(variable="payment_type", tipo_horario="Vista General", mes="Todos"):
    """Calcula frecuencia de tipo de pago o tarifas (RateCode)."""
    qm = get_qm()
    filtro = build_sql_filter(tipo_horario, mes)
    
    if variable == "payment_type":
        query = f"""
            SELECT m.descripcion AS Categoria, COUNT(*) AS Frecuencia
            FROM registro_viajes r
            JOIN metodo_pago m ON r.payment_type_id = m.payment_type_id
            WHERE {filtro}
            GROUP BY m.descripcion
            ORDER BY Frecuencia DESC
        """
    else:  # RateCodeID
        query = f"""
            SELECT t.descripcion AS Categoria, COUNT(*) AS Frecuencia
            FROM registro_viajes r
            JOIN tarifas t ON r.rate_code_id = t.rate_code_id
            WHERE {filtro}
            GROUP BY t.descripcion
            ORDER BY Frecuencia DESC
        """
    return qm.execute_query(query)

@st.cache_data
def get_passenger_distribution(tipo_horario="Vista General", mes="Todos"):
    """Calcula frecuencias de pasajeros, omitiendo registros en cero."""
    qm = get_qm()
    filtro = build_sql_filter(tipo_horario, mes)
    
    query = f"""
        SELECT passenger_count AS Pasajeros, COUNT(*) AS Frecuencia
        FROM registro_viajes 
        WHERE passenger_count > 0 AND {filtro}
        GROUP BY passenger_count
        ORDER BY passenger_count
    """
    return qm.execute_query(query)

@st.cache_data
def get_location_ranking(top=True, tipo_horario="Vista General", mes="Todos"):
    """Retorna el Top 5 de zonas (Más o Menos frecuentadas)."""
    qm = get_qm()
    filtro = build_sql_filter(tipo_horario, mes)
    orden = "DESC" if top else "ASC"
    
    query = f"""
        SELECT l.zone AS Zona, COUNT(*) AS Total
        FROM registro_viajes r
        JOIN localizacion_viaje l ON r.do_location_id = l.location_id
        WHERE l.zone IS NOT NULL AND l.zone != 'Unknown' AND {filtro}
        GROUP BY l.zone
        ORDER BY Total {orden}
        LIMIT 5
    """
    return qm.execute_query(query)

# ==========================================
# C. GENERADORES DE GRÁFICOS VISUALES
# ==========================================

def plot_passenger_distribution(df, tipo_horario):
    """Renderiza el Histograma con Vapor White / Neon Red"""
    accent = get_accent_color(tipo_horario)
    
    fig = px.bar(df, x="Pasajeros", y="Frecuencia", title="Distribución de Pasajeros", 
                 color_discrete_sequence=[accent])
    fig.update_layout(
        plot_bgcolor=BICKLE_PALETTE["asphalt_night"], 
        paper_bgcolor=BICKLE_PALETTE["asphalt_night"],
        font_color=BICKLE_PALETTE["vapor_white"],
        xaxis=dict(tickmode='linear')
    )
    return fig

def plot_payment_donut(df, tipo_horario):
    """Renderiza el gráfico tipo Donut de pagos"""
    # Si es hora pico, resaltamos con Neón, sino grises y amarillos
    colores = [get_accent_color(tipo_horario), BICKLE_PALETTE["steel_gray"], BICKLE_PALETTE["vapor_white"]]
    
    fig = px.pie(df, names='Categoria', values='Frecuencia', hole=0.6, 
                 title="Frecuencia de Pagos", color_discrete_sequence=colores)
    fig.update_layout(
        plot_bgcolor=BICKLE_PALETTE["asphalt_night"], 
        paper_bgcolor=BICKLE_PALETTE["asphalt_night"],
        font_color=BICKLE_PALETTE["vapor_white"]
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def plot_location_ranking(df, tipo_horario, top=True):
    """Gráfico de barras horizontales para Destinos"""
    accent = get_accent_color(tipo_horario)
    titulo = "Top 5 Destinos Frecuentes" if top else "Top 5 Zonas Menos Frecuentadas"
    
    fig = px.bar(df, x="Total", y="Zona", orientation='h', title=titulo,
                 color_discrete_sequence=[accent])
    # Invertir eje Y para que el mayor quede arriba
    fig.update_layout(yaxis={'categoryorder':'total ascending'},
                      plot_bgcolor=BICKLE_PALETTE["asphalt_night"], 
                      paper_bgcolor=BICKLE_PALETTE["asphalt_night"],
                      font_color=BICKLE_PALETTE["vapor_white"])
    return fig