import sqlite3 as sql
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Tomando como base la idea aportada por Yonelvis para la automatización de fuentes
origen = ['2019-10.sqlite', '2019-11.sqlite', '2019-12.sqlite']
tablas_origen = ['tripdata', 'tripdata', 'tripdata']

# Ésta es la base de datos donde está nuestro esquema normalizado 
db_normalizada = 'taxis_nuevayork2019_trimestre.db'

# FUNCIÓN ETL CREADA EN BASE A LAS IDEAS DE LIMPIEZA DE SAMUEL 
# E IMPLEMENTACIÓN DE INSERCIÓN POR CHUNKS POR VICO

def procesar_y_cargar_por_lotes():
    print("🚀 Iniciando extracción y limpieza por lotes (chunks)...")
    
    conn_destino = sql.connect(db_normalizada)
    cursor = conn_destino.cursor()
    
    # Lógica inteligente para el Trip ID (Soporta carga inicial e incremental)
    try:
        cursor.execute("SELECT MAX(trip_id) FROM registro_viajes")
        ultimo_id = cursor.fetchone()[0]
        trip_id_global = (ultimo_id + 1) if ultimo_id is not None else 1
    except sql.OperationalError:
        trip_id_global = 1 
        
    print(f"🔄 Conteo de viajes configurado para iniciar en el ID: {trip_id_global}")
    
    for archivo, tabla in zip(origen, tablas_origen):
        print(f"\n📂 Procesando archivo: {archivo} (Tabla: {tabla})")
        conn_origen = sql.connect(archivo)
        
        query = f"""
            SELECT 
                vendorid, tpep_pickup_datetime, tpep_dropoff_datetime, passenger_count, 
                trip_distance, ratecodeid, store_and_fwd_flag, pulocationid, dolocationid, 
                payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount, 
                improvement_surcharge, total_amount
            FROM {tabla}
        """
        
        lote_num = 1
        # Vico: Implementación de chunksize para no saturar la RAM en la lectura/inserción
        for chunk in pd.read_sql_query(query, conn_origen, chunksize=100000):
            print(f"   Procesando lote {lote_num}...")
            
            # --- TRANSFORMACIÓN (Samuel) ---
            chunk = chunk[chunk['vendorid'].isin([1, 2])].copy()
            chunk['pickup_dt'] = pd.to_datetime(chunk['tpep_pickup_datetime'])
            chunk['dropoff_dt'] = pd.to_datetime(chunk['tpep_dropoff_datetime'])
            chunk['pickup_date'] = chunk['pickup_dt'].dt.date
            chunk['pickup_time'] = chunk['pickup_dt'].dt.time.astype(str)
            chunk['dropoff_date'] = chunk['dropoff_dt'].dt.date
            chunk['dropoff_time'] = chunk['dropoff_dt'].dt.time.astype(str)
            
            chunk.loc[chunk['passenger_count'] == 0, 'passenger_count'] = 2
            chunk = chunk[chunk['trip_distance'] > 0.0]
            
            longitud_chunk = len(chunk)
            chunk['trip_id'] = range(trip_id_global, trip_id_global + longitud_chunk)
            trip_id_global += longitud_chunk 
            
            # --- PARTICIONAMIENTO ---
            df_registro = chunk[['trip_id', 'vendorid', 'ratecodeid', 'payment_type', 
                                'pickup_date', 'pickup_time', 'dropoff_date', 'dropoff_time', 
                                'pulocationid', 'dolocationid', 'passenger_count', 'trip_distance'
                                ]].rename(columns={'vendorid': 'vendor_id', 'ratecodeid': 'rate_code_id',
                                                  'payment_type': 'payment_type_id', 'pulocationid': 'pu_location_id',
                                                  'dolocationid': 'do_location_id'})

            df_finanzas = chunk[['trip_id', 'vendorid', 'payment_type', 'store_and_fwd_flag', 
                                'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 
                                'improvement_surcharge', 'total_amount'
                                ]].rename(columns={'vendorid': 'vendor_id', 'payment_type': 'payment_type_id'})
            
            # --- CARGA (Vico) ---
            df_registro.to_sql('registro_viajes', conn_destino, if_exists='append', index=False)
            df_finanzas.to_sql('finanzas_viaje', conn_destino, if_exists='append', index=False)
            lote_num += 1
            
        conn_origen.close()
    conn_destino.close()
    print("\n✅ Carga completada con éxito.")

def exportar_toda_la_bd_a_parquet():
    print("\n📦 Generando Parquets (Modo Ahorro de Memoria - Sugerencia Vico)...")
    conn = sql.connect(db_normalizada)
    
    query_tablas = "SELECT name FROM sqlite_master WHERE type='table';"
    tablas_db = pd.read_sql_query(query_tablas, conn)
    
    for nombre_tabla in tablas_db['name']:
        if nombre_tabla != 'sqlite_sequence': 
            print(f"   -> Exportando tabla '{nombre_tabla}' a Parquet...")
            
            # Vico: Escritura por chunks para evitar NameError y MemoryError
            if nombre_tabla in ['registro_viajes', 'finanzas_viaje']:
                generador = pd.read_sql_query(f"SELECT * FROM {nombre_tabla}", conn, chunksize=200000)
                primer_chunk = True
                writer = None
                
                for chunk in generador:
                    tabla_pa = pa.Table.from_pandas(chunk)
                    if primer_chunk:
                        writer = pq.ParquetWriter(f"{nombre_tabla}.parquet", tabla_pa.schema)
                        primer_chunk = False
                    writer.write_table(tabla_pa)
                    
                if writer:
                    writer.close()
            else:
                df_tabla = pd.read_sql_query(f"SELECT * FROM {nombre_tabla}", conn)
                df_tabla.to_parquet(f"{nombre_tabla}.parquet", engine='pyarrow', index=False)
            
    conn.close()
    print("\n✅ Ecosistema Parquet generado exitosamente.")

#BLOQUE DE EJECUCIÓN 
if __name__ == "__main__":
    procesar_y_cargar_por_lotes()
    exportar_toda_la_bd_a_parquet()
    
