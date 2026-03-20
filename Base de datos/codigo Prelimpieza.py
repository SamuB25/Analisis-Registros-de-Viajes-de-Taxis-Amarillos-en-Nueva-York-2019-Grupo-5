import sqlite3 as sql
import pandas as pd

# 1. Definir los archivos de origen
archivos_origen = ['2019-10.db', '2019-11.db', '2019-12.db']
nombre_tabla_origen = 'tripdata' # Cambia esto por el nombre real de tu tabla

lista_dataframes = []

# 2. Extraer y combinar los datos
for archivo in archivos_origen:
    # Conectar a cada base de datos mensual
    conn = sqlite3.connect(archivo)
    
    # Leer la tabla completa en un DataFrame de pandas
    query = f"SELECT * FROM {tripdata}"
    df = pd.read_sql_query(query, conn)
    
    # Agregar opcionalmente una columna para saber de qué mes viene (útil para el modelo)
    df['archivo_origen'] = archivo 
    
    lista_dataframes.append(df)
    conn.close()

# Unir los 3 meses en un solo DataFrame
df_unificado = pd.concat(lista_dataframes, ignore_index=True)

# 3. Limpieza de Datos

# A. Eliminar valores nulos:
df_limpio = df_unificado.dropna(subset=['vendorid', 'passenger_count', 'ratecode_id', 'store_and_fwd_flag', 'payment_type']) 

# B. Eliminar filas con ceros
columnas_a_revisar = ['passenger_count', 'trip_distance']

# .all(axis=1) asegura que la fila se conserve SOLO si TODAS las 
# columnas revisadas en esa fila son diferentes de 0.0
df_limpio = df_limpio[(df_limpio[columnas_a_revisar] != 0.0).all(axis=1)]

# C. Eliminar valores negativos
columnas_estrictas = ['total_amount', '']

# .all(axis=1) asegura que la fila se conserve SOLO si TODAS las 
# columnas evaluadas tienen valores >= 0
df_limpio = df_limpio[(df_limpio[columnas_estrictas] >= 0).all(axis=1)]

# D. Eliminar decimales:
columnas_a_entero = ['vendorid', 'passenger_count', 'ratecode', 'pulocationid', 'dolocationid', 'payment_type']

for col in columnas_a_entero:
    # Asegúrate de que no queden nulos en estas columnas antes de convertir, o cámbialos por 0
    df_limpio[col] = df_limpio[col].fillna(0).astype(int)

# 4. Cargar en el Modelo Normalizado
# Conectar a la nueva base de datos
conn_destino = sqlite3.connect('taxis_nuevayork2019_trimestre.db')

# Insertar los datos limpios. 
# if_exists='replace' sobrescribe la tabla si existe. Usa 'append' si quieres ir sumando datos sin borrar.
df_limpio.to_sql('taxis_nuevayork2019_trimestre_limpia', conn_destino, if_exists='replace', index=False)

conn_destino.close()

print("Limpieza y consolidación completadas con éxito.")