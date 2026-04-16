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

# Guía del Esquema de Estrella para el usuario actualizada con los nombres que las entidades tomaron en los parquets de la DB
with st.expander("📖 Guía de Entidades y Arquitectura OLAP"):
    st.markdown("""
    ### Arquitectura de Estrella (Star Schema)
    Consulta el sistema usando los nombres físicos detectados en el Data Lake:
    
    1. **Entidades de Hechos**: 
        - **`viaje`**: Datos de movilidad (distancia, pasajeros).
        - **`finanzas`**: Datos monetarios (total_amount, tip_amount).
    
    2. **Entidades de Dimensión**:
        - **`localizacion`**: Zonas y distritos de NYC.
        - **`pagos`**: Métodos de pago (Crédito, Efectivo).
        - **`tarifas`**: Tipos de tarifa aplicadas.
    """)

#Guía para el usario
st.markdown("### Protocolo de Operación del Yellow Query")

col_guia, col_adv = st.columns(2)

with col_guia:
    st.markdown("""
    **Instrucciones de Consulta**
    
    Para interactuar con el motor de base de datos, siga estas normas de sintaxis:
    
    1. **Finalización de Sentencia**: Toda consulta debe terminar obligatoriamente con un punto y coma (;). Esto indica al motor DuckDB el cierre de la instrucción.
    2. **Referencia de Entidades**: Utilice los nombres físicos definidos en el Data Lake. Los nombres de tablas y columnas son sensibles al contexto del esquema.
    3. **Selección de Campos**: Se recomienda especificar las columnas requeridas en lugar de utilizar el comodín (*), esto optimiza la velocidad de transferencia de datos.
    """)

with col_adv:
    st.markdown("""
    **Restricciones y Límites del Sistema**
    
    El entorno cuenta con protecciones automáticas para garantizar la estabilidad:
    
    1. **Umbral de Visualización**: Existe un límite máximo de 5,000 registros por consulta. Resultados que excedan esta cifra serán truncados automáticamente.
    2. **Gestión de Memoria**: La terminal no almacena estados de consultas previas. Cada ejecución limpia el búfer de datos para prevenir el desbordamiento de RAM en el navegador.
    3. **Integridad de Relaciones**: Para operaciones de unión (JOIN), es indispensable utilizar la llave primaria 'trip_id' para conectar las entidades de Hechos.
    """)

st.markdown("---")

# --- 3. GESTIÓN DE CONSULTAS (Session State) ---
if 'query_input' not in st.session_state:
    st.session_state.query_input = "SELECT * FROM registro_viajes LIMIT 10"

def set_query(nueva_query):
    st.session_state.query_input = nueva_query
    st.rerun()

st.subheader("💡 Sugerencias Personalizadas")
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("Cuartiles por Distancia y Comportamiento de Propinas"):
        set_query("""WITH datos_unidos AS (
            SELECT 
                v.trip_distance, 
                f.fare_amount, 
                f.tip_amount, 
                f.total_amount,
                NTILE(4) OVER (ORDER BY v.trip_distance) AS num_cuartil
            FROM viaje v
            JOIN finanzas f ON v.trip_id = f.trip_id
            JOIN pagos p ON v.payment_type_id = p.payment_type_id
            WHERE p.descripcion ILIKE 'Credit card'
              AND f.total_amount > 0
        )
        SELECT 
            num_cuartil AS "Cuartil",
            ROUND(AVG(trip_distance), 2) AS "Distancia Promedio",
            ROUND(AVG(fare_amount), 2) AS "Tarifa Promedio (USD)",
            ROUND(AVG((tip_amount * 100.0) / total_amount), 2) AS "Propina %"
        FROM datos_unidos
        GROUP BY num_cuartil
        ORDER BY num_cuartil;""")

with c2:
    if st.button("Análisis de Embotellamientos Críticos por Hora"):
        set_query("""WITH Embotellamientos AS (
        SELECT 
            CAST(EXTRACT(HOUR FROM TRY_CAST(pickup_time AS TIME)) AS INT) AS hora,
            trip_distance,
            (DATEDIFF('second', TRY_CAST(pickup_time AS TIME), TRY_CAST(dropoff_time AS TIME)) / 3600.0) AS duracion_horas
        FROM viaje
        WHERE pickup_time IS NOT NULL 
          AND dropoff_time IS NOT NULL 
          AND trip_distance > 1.0
    ),
    Metricas AS (
        SELECT
            hora,
            COUNT(*) AS total_viajes,
            SUM(CASE WHEN (trip_distance / NULLIF(duracion_horas, 0)) < 5.0 THEN 1 ELSE 0 END) AS viajes_embotellados
            FROM Embotellamientos
            GROUP BY hora
    ) 
    SELECT
        hora AS "Hora",
        total_viajes AS "Total Viajes",
        viajes_embotellados AS "Viajes en embotellamiento",
        ROUND((viajes_embotellados * 100.0) / total_viajes, 2) AS "porcentaje %"
    FROM Metricas
    ORDER BY "Porcentaje %" DESC;""")

with c3:
    if st.button("Crecimiento Intermensual (MoM) de la Demanda"):
        set_query("""WITH Mensual AS (
    SELECT
        EXTRACT(MONTH FROM TRY_CAST(pickup_date AS DATE)) AS mes,
        COUNT(*) AS total_viajes
    FROM viaje
    WHERE pickup_date IS NOT NULL
    GROUP BY mes
    ),
    Crecimiento AS (
        SELECT
            mes,
            total_viajes,
            LAG(total_viajes) OVER (ORDER BY mes) AS viajes_mes_anterior
        FROM Mensual
    )
    SELECT
        CAST(mes AS INT) AS "Mes",
        total_viajes AS "Total Viajes",
        viajes_mes_anterior AS "Viajes Mes Anterior",
        COALESCE(
            ROUND(((total_viajes - viajes_mes_anterior) * 100.0) / NULLIF(viajes_mes_anterior, 0), 2), 0.0) AS "Variacion %"
    FROM Crecimiento
    WHERE mes BETWEEN 10 AND 12
    ORDER BY mes DESC;""")
        
with c4:
    if st.button("Comportamiento de Propinas: Fines de Semana vs. Días Laborables"):
        set_query("""WITH ViajesTarjeta AS (
        SELECT 
            v.trip_id,
            v.pickup_date,
            f.fare_amount,
            f.tip_amount,
            f.total_amount,
            CAST(EXTRACT(ISODOW FROM TRY_CAST(v.pickup_date AS DATE)) AS INT) as dia_semana
        FROM 
            viaje v
        JOIN 
            finanzas f ON v.trip_id = f.trip_id
        WHERE 
            v.payment_type_id = 1 
            AND f.total_amount > 0
    )
    SELECT 
        CASE 
            WHEN dia_semana IN (6, 7) THEN 'Fin de Semana'
            ELSE 'Día Laborable'
        END AS tipo_dia,
        COUNT(trip_id) AS numero_viajes,
        ROUND(AVG(fare_amount), 2) AS promedio_tarifa_base,
        ROUND((SUM(tip_amount) / SUM(total_amount)) * 100, 2) AS porcentaje_propina_total
    FROM 
        ViajesTarjeta
    GROUP BY 
        tipo_dia
    ORDER BY 
        tipo_dia DESC;""") 


# --- 4. LA CONSOLA INTERACTIVA ---
query_usuario = st.text_area("SQL Terminal:", value=st.session_state.query_input, height=150)

if st.button("🚀 Ejecutar Yellow Query"):
    # Borramos cualquier rastro del resultado anterior para no saturar la app con las consultas de varios usuarios
    if 'df_resultado' in st.session_state:
        del st.session_state.df_resultado
    
    with st.spinner("Consultando el Data Lake..."):
        df_res, error_sql = execute_custom_query(qm, query_usuario)
        
        if error_sql:
            st.error(f"❌ Error: {error_sql}")
        elif isinstance(df_res, pd.DataFrame) and not df_res.empty:
            # 2. CONTROL DE TAMAÑO: No dejamos que entren más de 5000 filas a la memoria del navegador porque se rompe la app
            if len(df_res) > 5000:
                st.warning(f"⚠️ Consulta truncada a 5,000 filas por seguridad.")
                df_res = df_res.head(5000)
            
            st.session_state.df_resultado = df_res # Guardamos solo el actual
            st.success(f"Éxito: {len(df_res)} registros.")
            st.dataframe(st.session_state.df_resultado, use_container_width=True)
            
            # 3. LIBERACIÓN MANUAL: Ayudamos al recolector de basura de Python
            del df_res

st.subheader("DICCIONARIO DEL YELLOW QUERY")

st.markdown("#### Entidad: viaje")
st.image("assets\diccionario_viaje.png", use_container_width=True)
    
st.markdown("#### Entidad: finanzas")
st.image("assets\diccionario_finanzas.png", use_container_width=True)
    
st.markdown("#### Entidades: localizacion y pagos")
st.image("assets\diccionario_cat1.png", use_container_width=True)
    
st.markdown("#### Entidades: tarifas y plataformas")
st.image("assets\diccionario_cat2.png", use_container_width=True)