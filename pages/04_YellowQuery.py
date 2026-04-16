import streamlit as st
import pandas as pd
import plotly.express as px
# Importamos la lógica y la conexión
from src.drive_conn import preparar_data_lake
from src.query_manager import get_query_manager
from src.stats_logic import execute_custom_query 

# --- 1. INICIALIZACIÓN DE CONEXIÓN (Indispensable en cada página) ---
@st.cache_resource
def init_connection():
    if preparar_data_lake():
        return get_query_manager()
    return None

# Definimos 'qm' al principio para que toda la página lo reconozca
qm = init_connection()

if qm is None:
    st.error("❌ No se pudo conectar al Data Lake.")
    st.stop()

# --- 2. INTERFAZ Y BANNERS ---
# Usamos / para que funcione bien en la nube de Streamlit
st.image("assets/yellow_q.png", use_column_width=True) 
st.markdown("""
    Bienvenido a la terminal de inteligencia. Aquí puedes ejecutar sentencias **SQL** directamente sobre el Data Lake de los Yellow Taxis.
""")

# Guía del Esquema de Estrella para el usuario
with st.expander("📖 Guía de Entidades y Arquitectura OLAP"):
    st.markdown("""
    ### Arquitectura de Estrella (Star Schema)
    El **Yellow Query** integra un sistema OLAP diseñado para el análisis estadístico eficiente.
    
    1. **Entidades Centrales (Hechos)**: 
        - `registro_viajes`: Movilidad (distancia, pasajeros).
        - `finanzas_viaje`: Dinero (total_amount, fare_amount, tip_amount).
    
    2. **Entidades Periféricas (Dimensiones)**:
        - `localizacion_viaje`: Zonas y distritos de NYC.
        - `metodo_pago`: Crédito, efectivo y otros.
    """)

# --- 3. GESTIÓN DE CONSULTAS (Session State) ---
if 'query_input' not in st.session_state:
    st.session_state.query_input = "SELECT * FROM registro_viajes LIMIT 10"

def set_query(nueva_query):
    st.session_state.query_input = nueva_query
    st.rerun()

st.subheader("💡 Sugerencias Personalizadas")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("📍 Destinos por Gasto Total"):
        set_query("""SELECT l.zone as Zona, AVG(f.total_amount) as Gasto_Promedio 
FROM registro_viajes v 
JOIN finanzas_viaje f ON v.trip_id = f.trip_id 
JOIN localizacion_viaje l ON v.do_location_id = l.location_id 
GROUP BY 1 ORDER BY 2 DESC LIMIT 10""")

with c2:
    if st.button("💰 Propinas por Pago"):
        set_query("""SELECT m.descripcion as Metodo, AVG(f.tip_amount) as Propina_Media 
FROM finanzas_viaje f 
JOIN metodo_pago m ON f.payment_type_id = m.payment_type_id 
GROUP BY 1 ORDER BY 2 DESC""")

with c3:
    if st.button("🚕 Viajes Largos por Distrito"):
        set_query("""SELECT l.borough as Distrito, MAX(v.trip_distance) as Distancia_Max 
FROM registro_viajes v 
JOIN localizacion_viaje l ON v.pu_location_id = l.location_id 
GROUP BY 1 ORDER BY 2 DESC""")

# --- 4. LA CONSOLA INTERACTIVA ---
query_usuario = st.text_area(
    "Escribe tu sentencia SQL:", 
    value=st.session_state.query_input, 
    height=150,
    help="Usa SQL estándar. Tablas: registro_viajes, finanzas_viaje, localizacion_viaje."
)

if st.button("🚀 Ejecutar Yellow Query"):
    with st.spinner("Consultando el Data Lake..."):
        # Llamamos a la función protegida
        df_res, error_sql = execute_custom_query(qm, query_usuario)
        
        if error_sql:
            st.error(f"❌ Error en la consulta SQL: {error_sql}")
        elif df_res is not None and not df_res.empty:
            st.success(f"¡Éxito! {len(df_res)} registros encontrados.")
            tab1, tab2 = st.tabs(["📑 Datos Crudos", "📊 Visualización"])
            
            with tab1:
                st.dataframe(df_res, use_container_width=True)
            
            with tab2:
                columnas = df_res.columns
                if len(columnas) >= 2:
                    # Determinamos si hay una columna de 'frecuencia' o 'gasto' para el color
                    color_col = columnas[1] if pd.api.types.is_numeric_dtype(df_res[columnas[1]]) else None
                    fig = px.bar(
                        df_res, x=columnas[0], y=columnas[1], color=color_col,
                        color_continuous_scale="Viridis", template="plotly_dark",
                        range_color=[0, df_res[columnas[1]].max()] if color_col else None # BLOQUEO DE NEGATIVOS
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Necesitas al menos 2 columnas para graficar.")
        else:
            st.warning("La consulta no devolvió resultados.")
