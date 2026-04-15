# Cuestionario SQL 
import streamlit as st
import pandas as pd
from App_taxis_ny.src.query_manager import query_manager

def ejecutar_pregunta_1():
    manager = query_manager()
    """
    Divide los viajes pagados con tarjeta de crédito en 4 cuartiles por distancia.
    Calcula distancia promedio, tarifa promedio y % de propina.
    """

    # 1. Cuartiles de Distancia y Comportamiento de Propinas
    # Enunciado: Divide todos los viajes pagados con tarjeta de crédito en 4 cuartiles basados 
    # en la distancia del viaje. Para cada cuartil, calcula la distancia promedio, el monto de tarifa
    #  promedio y el porcentaje promedio que representa la propina respecto al monto total.
    # Muestra el número de cuartil y las métricas calculadas.


    sql = """
        WITH datos_unidos AS (
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
        ORDER BY num_cuartil;
        """
    return manager.execute_query(sql)

#como ya no estamos trabajando con direcciones eliminamos eso pues el import de App_.... debería funcionar
# Anexas una interfaz para que se vizualice el resultado consultado de manera correcta a petición del grupo
st.title("Query nro 1. Cuartiles de Distancia y Comportamiento de Propinas")
st.subheader("Resultados:")     
try:
    df_resultado = ejecutar_pregunta_1()
    if df_resultado.empty:
        st.warning("No se encontraron datos para la consulta.")
    else:
        st.dataframe(df_resultado)
        st.caption("En el primer cuartil (el cual equivale a los viajes con un distancia más corta) es el que mayor porcentaje de propinas con un 15.41% a diferencia de cuarto cuartil que contiene las distancias promedio mas altas pero el porcentaje de propinas entre los cuatro cuartiles con unn 14.82%") 
except Exception as e:
    st.error(f"Ocurrió un error al ejecutar la consulta: {e}")

# 2. Análisis de Embotellamientos Críticos por Hora
# Enunciado: Identifica a qué hora del día la ciudad sufre los peores embotellamientos. Define
# un embotellamiento como un viaje de más de 1 milla de distancia donde la velocidad promedio
# fue inferior a 5 millas por hora. Agrupa los datos por la hora del día (0 a 23) de la recogida.
# Muestra la hora, el número total de viajes realizados a esa hora, la cantidad de viajes que
# cayeron en embotellamiento y el porcentaje que estos representan. Ordena de peor a mejor porcentaje.




# 3. Crecimiento Intermensual (MoM) de la Demanda
# Enunciado: Evalúa la estacionalidad del servicio calculando la tasa de crecimiento mensual
# (Month-over-Month) en la cantidad total de viajes. Para cada mes del ultimo trimestre
# del año 2019, muestra el mes, el total de viajes de ese mes, el total de viajes del mes
# inmediatamente anterior y el porcentaje de variación.



# 4. Comportamiento de Propinas: Fines de Semana vs. Días Laborables
# Enunciado: ¿La gente da mejores propinas los fines de semana? Clasifica los viajes pagados
# con tarjeta de crédito en ”Fin de Semana”(Sábado y Domingo) y ”Día Laborable”(Lunes a Viernes)
# basándote en la fecha de recogida. Calcula para ambos grupos el número de viajes,
# el promedio de la tarifa base y el porcentaje que representa la propina sobre el monto total.

def ejecutar_query_4():
    # Instanciamos el manager 
    manager = query_manager()
    query_4 = """
    WITH ViajesTarjeta AS (
        SELECT 
            r.trip_id,
            r.pickup_date,
            f.fare_amount,
            f.tip_amount,
            f.total_amount,
            CAST(EXTRACT(ISODOW FROM TRY_CAST(r.pickup_date AS DATE)) AS INT) as dia_semana
        FROM 
            registro_viaje r
        JOIN 
            finanzas_viaje f ON r.trip_id = f.trip_id
        WHERE 
            r.payment_type_id = 1 
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
        tipo_dia DESC
    """
    return manager.execute_query(query_4)

# Puedes probar si funciona imprimiendo el resultado así:
print(ejecutar_query_4())

# 5. Impacto del Recargo por Congestión según la Longitud del Viaje
# Enunciado: Analiza cómo afecta el recargo por congestión a la estructura de costos del
# pasajero. Clasifica los viajes en Cortos”(menos de 2 millas), ”Medios”(entre 2 y 8 millas) y
# ”Largos”(más de 8 millas). Para cada categoría, calcula el porcentaje promedio del monto
# total que es consumido exclusivamente por el recargo de congestión. Excluye viajes donde el
# recargo sea cero o nulo.

def ejecutar_pregunta_5():
    # Instanciamos el manager 
    manager = query_manager()
    
    sql = """
    WITH ClasificacionViajes AS (
        SELECT 
            CASE 
                WHEN r.trip_distance < 2 THEN 'Cortos'
                WHEN r.trip_distance >= 2 AND r.trip_distance <= 8 THEN 'Medios'
                WHEN r.trip_distance > 8 THEN 'Largos'
            END AS categoria_viaje,
            f.improvement_surcharge, 
            f.total_amount
        FROM registro_viajes r
        JOIN finanzas_viaje f ON r.trip_id = f.trip_id
        -- Filtramos para excluir recargos en cero o nulos, y totales en cero
        WHERE f.improvement_surcharge IS NOT NULL 
          AND f.improvement_surcharge > 0
          AND f.total_amount > 0
    )
    SELECT 
        categoria_viaje AS "Categoría de Viaje",
        -- Calculamos el porcentaje: (Recargo / Total) * 100
        ROUND(AVG((improvement_surcharge * 100.0) / total_amount), 2) AS "Porcentaje Promedio Recargo (%)"
    FROM ClasificacionViajes
    GROUP BY categoria_viaje
    -- Ordenamos para que se vea más organizado
    ORDER BY 
        CASE categoria_viaje
            WHEN 'Cortos' THEN 1
            WHEN 'Medios' THEN 2
            WHEN 'Largos' THEN 3
        END;
    """
    
    return manager.execute_query(sql)

# Puedes probar si funciona imprimiendo el resultado así:
print(ejecutar_pregunta_5())
