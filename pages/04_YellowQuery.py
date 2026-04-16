import streamlit as st
import pandas as pd
import plotly.express as px
from src.stats_logic import execute_custom_query #Importamos la función de ejecución que protege a la app

st.image("assets/yellow_q.png", use_column_width=True)
st.markdown("""
    Bienvenido a la terminal de inteligencia. Aquí puedes ejecutar sentencias **SQL** directamente sobre el Data Lake de los Yellow Taxis.
""")

# Guía de Entidades y Arquitectura OLAP para el usuario
with st.expander("📖 Guía de Entidades y Arquitectura OLAP"):
    st.markdown("""
    ### Arquitectura de Estrella (Star Schema)
    El **Yellow Query** integra un sistema OLAP diseñado para el análisis estadístico eficiente.
    
    1. **Entidades Centrales (Hechos)**: 
        - `registro_viajes`: Métricas de movilidad (distancia, pasajeros).
        - `finanzas_viaje`: Métricas monetarias (total pagado, propinas).
    
    2. **Entidades Periféricas (Dimensiones)**:
        - `localizacion_viaje`: Zonas y distritos de NYC.
        - `metodo_pago`: Crédito, efectivo y otros.
        - `tarifas`: Tipo de tarifa aplicada (Estándar, JFK, etc.).
        - `plataformas_tpep`: Proveedor del dato.
    
    *Tip: Para consultas de gasto, une `registro_viajes` con `finanzas_viaje` usando `trip_id`.*
    """)

# Inicializamos el estado de la query si no existe
if 'query_input' not in st.session_state:
    st.session_state.query_input = "SELECT * FROM registro_viajes LIMIT 10"

def set_query(nueva_query):
    st.session_state.query_input = nueva_query
    # Forzamos el rerun para que el text_area actualice su valor inmediatamente
    st.rerun()

st.subheader("Sugerencias Personalizadas de parte del equipo")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Top 10 Destinos por Gasto"):
        set_query("""SELECT l.zone as Zona, AVG(f.total_amount) as Gasto_Promedio 
FROM registro_viajes v 
JOIN finanzas_viaje f ON v.trip_id = f.trip_id 
JOIN localizacion_viaje l ON v.do_location_id = l.location_id 
GROUP BY 1 ORDER BY 2 DESC LIMIT 10""")

with c2:
    if st.button("Propinas por Pago"):
        set_query("""SELECT m.metodo as Metodo, AVG(f.tip_amount) as Propina_Media 
FROM finanzas_viaje f 
JOIN metodo_pago m ON f.payment_type_id = m.payment_type_id 
GROUP BY 1 ORDER BY 2 DESC""")

with c3:
    if st.button("Viajes Largos por Distrito"):
        set_query("""SELECT l.borough as Distrito, MAX(v.trip_distance) as Distancia_Max 
FROM registro_viajes v 
JOIN localizacion_viaje l ON v.pu_location_id = l.location_id 
GROUP BY 1 ORDER BY 2 DESC""")

query_usuario = st.text_area(
    "Escribe tu sentencia SQL:", 
    value=st.session_state.query_input, 
    height=150,
    help="Usa SQL estándar. Las tablas disponibles son registro_viajes, finanzas_viaje y localizacion_viaje."
)

if st.button("Ejecutar Yellow Query"):
    with st.spinner("Consultando el Data Lake..."):
        # AQUÍ USAMOS LA FUNCIÓN DE STATS_LOGIC
        # La función ya tiene el try-except interno
        df_resultado, error_sql = execute_custom_query(qm, query_usuario)
        
        if error_sql:
            # Si hay un error (de sintaxis, de tabla inexistente, etc.)
            st.error(f"Error en la consulta SQL: {error_sql}")
            st.info("Revisa que los nombres de las tablas y columnas sean correctos.")
        
        elif df_resultado is not None and not df_resultado.empty:
            st.success(f"¡Éxito! Se encontraron {len(df_resultado)} registros.")
            
            # Visualización dual: Tabla y Gráfico
            tab_tabla, tab_viz = st.tabs(["📑 Datos Crudos", "📊 Visualización"])
            
            with tab_tabla:
                st.dataframe(df_resultado, use_container_width=True)
            
            with tab_viz:
                columnas = df_resultado.columns
                if len(columnas) >= 2:
                    fig = px.bar(
                        df_resultado, 
                        x=columnas[0], 
                        y=columnas[1],
                        color=columnas[1],
                        color_continuous_scale="Viridis",
                        template="plotly_dark"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Agrega más columnas a tu SELECT para generar un gráfico automático.")
        else:
            st.warning("La consulta no devolvió resultados.")
