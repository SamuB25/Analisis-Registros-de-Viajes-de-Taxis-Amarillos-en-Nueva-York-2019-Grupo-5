import sqlite3 as sql
import pandas as pd

# 1. Definir los archivos de origen
archivos_origen = ['2019-10.sqlite', '2019-11.sqlite', '2019-12.sqlite']
nombre_tablas_origen = ['Octubre', 'Noviembre', 'Diciembre']

lista_dataframes = []

# 2. Extraer y combinar los datos
for archivo, tabla in zip(archivos_origen, nombre_tablas_origen):
    # Conectar a cada base de datos mensual
    conn = sql.connect(archivo)
    
    # IMPORTANTE: Ahora usamos la variable 'tabla' que cambia en cada vuelta del ciclo
    query = f"SELECT * FROM {tabla}"
    
    print(f"Leyendo tabla {tabla} desde {archivo}...")
    df = pd.read_sql_query(query, conn)
    
    # Agregar columna de origen
    df['archivo_origen'] = archivo 
    
    lista_dataframes.append(df)
    conn.close()

# Unir los 3 meses en un solo DataFrame
df_unificado = pd.concat(lista_dataframes, ignore_index=True)

# 3. Limpieza de Datos

# A. Eliminar valores nulos:
df_limpio = df_unificado.dropna(subset=['vendorid', 'passenger_count', 'ratecodeid', 'store_and_fwd_flag', 'payment_type']) 

# B. Eliminar filas con ceros
columnas_a_revisar = ['trip_distance']

# .all(axis=1) asegura que la fila se conserve SOLO si TODAS las columnas revisadas en esa fila son diferentes de 0.0
df_limpio = df_limpio[(df_limpio[columnas_a_revisar] != 0.0).all(axis=1)]

# C. Buscamos las filas donde passenger_count sea 0 y les asignamos directamente el promedio de pasajeros por viaje, que es 2, para reducir la varianza de los datos
df_limpio.loc[df_limpio['passenger_count'] == 0, 'passenger_count'] = 2

# D. Eliminar valores negativos que pueden afectar el análisis
columnas_estrictas = ['fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount', 'congestion_surcharge']

# .all(axis=1) asegura que la fila se conserve SOLO si TODAS las 
# columnas evaluadas tienen valores >= 0
df_limpio = df_limpio[(df_limpio[columnas_estrictas] >= 0).all(axis=1)]

# E. Eliminar decimales
columnas_a_entero = ['vendorid', 'passenger_count', 'ratecodeid', 'pulocationid', 'dolocationid', 'payment_type']

for col in columnas_a_entero:
    df_limpio[col] = df_limpio[col].astype('Int64')

# 4. Cargar en el Modelo Normalizado
# Conectar a la nueva base de datos
conn_destino = sql.connect('taxis_nuevayork2019_trimestre.db')

# Insertar los datos limpios. 
# if_exists='replace' sobrescribe la tabla si existe. Usa 'append' si quieres ir sumando datos sin borrar.
df_limpio.to_sql('taxis_nuevayork2019_trimestre_limpia', conn_destino, if_exists='replace', index=False)

conn_destino.close()

print("Limpieza y consolidación completadas con éxito.")