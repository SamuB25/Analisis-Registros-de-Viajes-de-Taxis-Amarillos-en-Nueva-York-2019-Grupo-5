import streamlit as st
import pandas as pd

# 1. PALETA DE COLORES OFICIAL (Bickle Palette) inspirada en Taxi Driver 
BICKLE_PALETTE = {
    "taxi_yellow": "#F2BC1B",
    "asphalt_night": "#121212",
    "vapor_white": "#F2F2F2",
    "neon_red": "#D90404",
    "steel_gray": "#757575"
}

def get_accent_color(tipo_horario):
    """El acento cambia a Neon Red si es Hora Pico."""
    return BICKLE_PALETTE["neon_red"] if tipo_horario == "Hora Pico" else BICKLE_PALETTE["taxi_yellow"]

def format_kpi(value, is_money=False):
    """Formatea números para la 'Zona de Despacho'."""
    if value is None: return "0"
    if is_money: return f"$ {value:,.2f}"
    if value >= 1_000_000: return f"{value/1_000_000:.1f}M"
    return f"{int(value):,}" if value > 100 else f"{value:.2f}"

def build_sql_filter(tipo_horario="Vista General", mes="Todos"):
    """
    Genera el Filtro Maestro basado en las columnas pickup_date y pickup_time.
    Lógica de Hora Pico: Lun-Vie, 16:00 a 20:00.
    """
    condiciones = ["1=1"]
    
    if tipo_horario == "Hora Pico":
        # Filtro: Lunes a Viernes (DOW 1-5) y horario de mayor afluencia 
        condiciones.append("CAST(EXTRACT(DOW FROM CAST(pickup_date AS DATE)) AS INT) BETWEEN 1 AND 5")
        condiciones.append("pickup_time BETWEEN '16:00:00' AND '20:00:00'")
    elif tipo_horario == "Hora No Pico":
        condiciones.append("(CAST(EXTRACT(DOW FROM CAST(pickup_date AS DATE)) AS INT) IN (0, 6) OR pickup_time NOT BETWEEN '16:00:00' AND '20:00:00')")

    meses_map = {"Octubre": 10, "Noviembre": 11, "Diciembre": 12}
    if mes in meses_map:
        condiciones.append(f"EXTRACT(MONTH FROM CAST(pickup_date AS DATE)) = {meses_map[mes]}")
    
    return " AND ".join(condiciones)

# --- BLOQUE DE AGREGACIONES (Consultas DuckDB) ---

@st.cache_data
def get_average_metrics(_qm, tipo_horario, mes):
    """Calcula promedios para las Cards superiores[cite: 10, 38]."""
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
    return _qm.execute_query(query).iloc[0]

@st.cache_data
def get_passenger_distribution(_qm, tipo_horario, mes):
    """Genera distribución omitiendo 0 pasajeros por consistencia operativa[cite: 5, 6, 44]."""
    filtro = build_sql_filter(tipo_horario, mes)
    query = f"""
        SELECT passenger_count as Pasajeros, COUNT(*) as Frecuencia 
        FROM viaje 
        WHERE {filtro} AND passenger_count > 0 
        GROUP BY 1 ORDER BY 1
    """
    return _qm.execute_query(query)

@st.cache_data
def get_usage_frequencies(_qm, tipo_horario, mes):
    """Calcula frecuencia de pagos uniendo con la tabla de descripciones[cite: 4, 45]."""
    filtro = build_sql_filter(tipo_horario, mes)
    query = f"""
        SELECT p.descripcion as Categoria, COUNT(*) as Frecuencia
        FROM finanzas f
        JOIN pagos p ON f.payment_type_id = p.payment_type_id
        JOIN viaje v ON f.trip_id = v.trip_id
        WHERE {filtro}
        GROUP BY 1
    """
    return _qm.execute_query(query)

@st.cache_data
def get_location_analysis(_qm, tipo_horario, mes, top=True, n=5):
    filtro = build_sql_filter(tipo_horario, mes)
    orden = "DESC" if top else "ASC"
    
    # Query para el total (necesario para la frecuencia relativa)
    res_total = _qm.execute_query(f"SELECT COUNT(*) FROM viaje v WHERE {filtro}")
    total_viajes = res_total.iloc[0, 0] if not res_total.empty else 0

    if total_viajes == 0: return pd.DataFrame()

    query = f"""
        SELECT l.zone as Zona, COUNT(*) as Frecuencia
        FROM viaje v
        JOIN localizacion l ON v.do_location_id = l.location_id
        WHERE {filtro}
        GROUP BY 1 ORDER BY 2 {orden} LIMIT {n}
    """
    df = _qm.execute_query(query)
    
    if not df.empty:
        # Usamos nombres de columna simples para evitar errores de encoding
        df.columns = ["Zona", "f_absoluta"] 
        df["f_relativa"] = (df["f_absoluta"] / total_viajes * 100).round(2)
    
    return df

@st.cache_data
def get_dynamic_insight(kpis, tipo_horario):
    """Genera la reseña automática para el chat_message de app.py."""
    if kpis['total_viajes'] == 0: return "No hay datos disponibles para este periodo."
    
    if tipo_horario == "Hora Pico":
        return f"🚨 **Perfil de Alta Demanda:** En este horario, la propina promedio es de {format_kpi(kpis['avg_tip'], True)}. El volumen de viajes se concentra en distancias cortas e intensas."
    else:
        return f"🌙 **Perfil Valle:** Se observa una distancia promedio de {format_kpi(kpis['avg_distance'])} mi. Los viajes son más largos, posiblemente hacia zonas residenciales."
    
@st.cache_data
def get_global_destination_stats(_qm, tipo_horario, mes_filtro):
    """
    Obtiene la totalidad de destinos con su frecuencia y tarifa promedio.
    Utiliza los nombres exactos de las tablas: registro_viajes, localizacion_viaje y finanzas_viaje.
    """
    filtro = build_sql_filter(tipo_horario, mes_filtro)
    
    # Query corregida con los nombres reales de las tablas de tu BD
    query = f"""
        SELECT 
            l.borough AS Distrito,
            l.zone AS Zona,
            COUNT(v.trip_id) AS Frecuencia,
            AVG(f.total_amount) AS Tarifa_Promedio
        FROM registro_viajes v
        JOIN localizacion_viaje l ON v.do_location_id = l.location_id
        JOIN finanzas_viaje f ON v.trip_id = f.trip_id
        WHERE {filtro}
        GROUP BY 1, 2
        ORDER BY 3 DESC
    """
    
    df = _qm.execute_query(query)
    
    # Verificación de seguridad para evitar el error 'NoneType' o 'empty'
    if df is not None and not df.empty:
        total_viajes = df["Frecuencia"].sum()
        df["Porcentaje (%)"] = (df["Frecuencia"] / total_viajes * 100).round(4)
        df["Tarifa_Promedio"] = df["Tarifa_Promedio"].round(2)
        return df
    
    return pd.DataFrame() # Retorna un dataframe vacío si no hay datos
