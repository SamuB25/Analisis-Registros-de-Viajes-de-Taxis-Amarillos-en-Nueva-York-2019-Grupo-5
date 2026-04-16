import streamlit as st
import pandas as pd
import plotly.express as px
from src.drive_conn import preparar_data_lake
from src.query_manager import get_query_manager
from src.stats_logic import execute_custom_query 

@st.cache_resource
def init_connection():
    if preparar_data_lake():
        return get_query_manager()
    return None

qm = init_connection()

if qm is None:
    st.error("❌ No se pudo conectar al Data Lake.")
    st.stop()

# 2. INTERFAZ Y BANNERS
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
query_usuario = st.text_area("SQL Terminal:", value=st.session_state.query_input, height=150)

if st.button("🚀 Ejecutar Consulta"): #Simplificamos la consola para evitar problemas en el despliegue
    with st.spinner("Consultando..."):
        # Llamamos a la lógica que ya tiene el try-except
        df_res, error_sql = execute_custom_query(qm, query_usuario)
        
        if error_sql:
            st.error(f"❌ Error SQL: {error_sql}")
        
        # EL BLOQUE CLAVE: Validamos que sea un DataFrame antes de preguntar si está vacío
        elif isinstance(df_res, pd.DataFrame):
            if not df_res.empty:
                st.success(f"Resultados: {len(df_res)} registros encontrados.")
                # Solo entregamos el DataFrame, sin gráficos
                st.dataframe(df_res, use_container_width=True)
            else:
                st.warning("La consulta se ejecutó correctamente pero no devolvió filas.")
        else:
            # Por si acaso la función devuelve algo inesperado (como un booleano)
            st.info("La consulta se procesó (posiblemente un comando que no devuelve tabla).")
