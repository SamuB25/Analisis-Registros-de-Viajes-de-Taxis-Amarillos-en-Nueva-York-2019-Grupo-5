import streamlit as st
import pandas as pd
from App_taxis_ny.src.query_manager import query_manager

# 1. Configuración básica de la app
st.title("🚖 Análisis de Frecuencia de Viajes")
st.subheader("Distribución por intervalos de 4 horas")

# 2. Inicializar la conexión a la base de datos
# Usamos @st.cache_resource para que no vuelva a leer los Parquet cada vez que interactúas con la app
@st.cache_resource
def iniciar_conexion():
    return query_manager()

qm = iniciar_conexion()

# 3. Consulta SQL a DuckDB
# - EXTRACT(hour...) saca solo la hora del texto.
# - Dividimos entre 4 para agrupar (Ej: 0,1,2,3 / 4 = 0 -> bloque 0)
query = """
    SELECT 
        CAST(EXTRACT(hour FROM TRY_CAST(pickup_time AS TIME)) / 4 AS INT) AS id_bloque,
        COUNT(*) AS cantidad_viajes
    FROM viaje
    WHERE pickup_time IS NOT NULL 
      AND TRY_CAST(pickup_time AS TIME) IS NOT NULL
    GROUP BY id_bloque
    ORDER BY id_bloque
"""

# Ejecutamos la consulta usando tu método creado en query_manager
df_horas = qm.execute_query(query)

# Eliminamos cualquier fila donde el id_bloque sea nulo
df_horas = df_horas.dropna(subset=['id_bloque'])

# Convertimos id_bloque a entero (esto falla si hay nulos, asegurando que el paso anterior funcionó)
df_horas['id_bloque'] = df_horas['id_bloque'].astype(int)

# 4. Crear los intervalos de texto legibles para el gráfico
etiquetas_intervalos = {
    0: "00:00 - 03:59",
    1: "04:00 - 07:59",
    2: "08:00 - 11:59",
    3: "12:00 - 15:59",
    4: "16:00 - 19:59",
    5: "20:00 - 23:59"
}

# Mapeamos la columna 'id_bloque' con nuestro diccionario
df_horas['Intervalo'] = df_horas['id_bloque'].map(etiquetas_intervalos)

# Eliminamos cualquier fila donde el mapeo haya fallado (por si acaso)
df_horas = df_horas.dropna(subset=['Intervalo'])

# Preparamos el índice para que Streamlit sepa qué poner en el eje X
df_grafico = df_horas.set_index('Intervalo')[['cantidad_viajes']]

# 5. Renderizar el gráfico de barras nativo de Streamlit
st.bar_chart(df_grafico, color="#ffd700") # Color amarillo taxi opcional 🚖