# Cuestionario SQL 

# 1. Cuartiles de Distancia y Comportamiento de Propinas
# Enunciado: Divide todos los viajes pagados con tarjeta de crédito en 4 cuartiles basados 
# en la distancia del viaje. Para cada cuartil, calcula la distancia promedio, el monto de tarifa
#  promedio y el porcentaje promedio que representa la propina respecto al monto total.
# Muestra el número de cuartil y las métricas calculadas.
import sys
import os

# 1. Obtenemos la ruta de 'pages'
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# 2. Subimos UN nivel para llegar a la Raíz (donde están ambas carpetas)
ruta_raiz = os.path.dirname(directorio_actual)

# 3. Añadimos la Raíz al radar de Python
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

# 4. AHORA EL IMPORT (Desde la raíz, entramos a App_taxis_ny -> src)
try:
    from App_taxis_ny.src.query_manager import query_manager
    print("✅ Conexión establecida: Ahora pages y App_taxis ya se hablan.")
except Exception as e:
    print(f"❌ Error de ruta: {e}")
def ejecutar_pregunta_1():
    manager = query_manager()
    """
    Divide los viajes pagados con tarjeta de crédito en 4 cuartiles por distancia.
    Calcula distancia promedio, tarifa promedio y % de propina.
    """
    
    # El JOIN es vital: 'viaje' tiene la distancia, 'finanzas' tiene los montos.
    sql = """
    WITH datos_unidos AS (
        SELECT 
            v.trip_distance, 
            f.fare_amount, 
            f.tip_amount, 
            f.total_amount,
            NTILE(4) OVER (ORDER BY v.trip_distance) AS num_cuartil
        FROM viaje v
        JOIN finanzas f ON v.vendor_id = f.vendor_id 
                       AND v.tpep_pickup_datetime = f.tpep_pickup_datetime
        JOIN pagos p ON v.payment_type = p.payment_type
        WHERE p.description ILIKE 'Credit card'
          AND f.total_amount > 0
    )
    SELECT 
        num_cuartil AS "Cuartil",
        ROUND(AVG(trip_distance), 2) AS "Distancia Promedio",
        ROUND(AVG(fare_amount), 2) AS "Tarifa Promedio",
        ROUND(AVG((tip_amount * 100.0) / total_amount), 2) AS "Propina %"
    FROM datos_unidos
    GROUP BY num_cuartil
    ORDER BY num_cuartil;
    """
    
    return manager.execute_query(sql)

# Bloque de ejecución principal
if __name__ == "__main__":
    print("\n--- EJECUTANDO CONSULTA 1: CUARTILES Y PROPINAS ---")
    try:
        df_resultado = ejecutar_pregunta_1()
        if df_resultado.empty:
            print("⚠️ La consulta no devolvió resultados. Revisa los filtros o los JOINs.")
        else:
            print(df_resultado)
    except Exception as e:
        print(f"❌ Error crítico al procesar los datos: {e}")

        

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




# 5. Impacto del Recargo por Congestión según la Longitud del Viaje
# Enunciado: Analiza cómo afecta el recargo por congestión a la estructura de costos del
# pasajero. Clasifica los viajes en Cortos”(menos de 2 millas), ”Medios”(entre 2 y 8 millas) y
# ”Largos”(más de 8 millas). Para cada categoría, calcula el porcentaje promedio del monto
# total que es consumido exclusivamente por el recargo de congestión. Excluye viajes donde el
# recargo sea cero o nulo.


