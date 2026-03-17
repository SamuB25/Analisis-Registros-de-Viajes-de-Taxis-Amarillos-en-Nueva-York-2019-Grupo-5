import pandas as pd
import sqlite3 as sql

def insertar_datos_catalogos():
    # 1. Conexión a la base de datos
    database = 'taxis_nuevayork2019_trimestre.db'
    conn = sql.connect(database)
    cursor = conn.cursor()
    
    print(f"Conectado a {database}. Iniciando inserción de catálogos...")

    try:
        # --- A. RELLENO DE CATÁLOGOS DESDE DICCIONARIO (PDF) ---
        
        # 1.1 Catálogo de Plataformas (VendorID)
        proveedores = [
            (1, 'Creative Mobile Technologies'),
            (2, 'VeriFone Inc.')
        ]
        cursor.executemany("INSERT OR IGNORE INTO plataformas_tpep VALUES (?,?)", proveedores)
        print("- Catálogo de plataformas insertado.")

        # 1.2 Catálogo de Tarifas (RateCodeID)
        tarifas = [
            (1, 'Standard rate'),
            (2, 'JFK'),
            (3, 'Newark'),
            (4, 'Nassau or Westchester'),
            (5, 'Negotiated fare'),
            (6, 'Group ride')
        ]
        cursor.executemany("INSERT OR IGNORE INTO tarifas VALUES (?,?)", tarifas)
        print("- Catálogo de tarifas insertado.")

        # 1.3 Catálogo de Métodos de Pago (Payment_type)
        pagos = [
            (1, 'Credit card'),
            (2, 'Cash'),
            (3, 'No charge'),
            (4, 'Dispute'),
            (5, 'Unknown'),
            (6, 'Voided trip')
        ]
        cursor.executemany("INSERT OR IGNORE INTO metodo_pago VALUES (?,?)", pagos)
        print("- Catálogo de métodos de pago insertado.")

        # --- B. INSERCIÓN DESDE ARCHIVO CSV (Zonas) ---
        
        zonas_taxis = 'Base de datos/taxi_zone_lookup.csv'
        try:
            df_zonas = pd.read_csv(zonas_taxis)
            
            # Aseguramos que las columnas coincidan con la estructura de la tabla 1.3
            # Estructura: location_id, borough, zone, service_zone
            df_zonas.columns = ['location_id', 'borough', 'zone', 'service_zone']
            
            # Insertamos los datos en la tabla existente
            df_zonas.to_sql('localizacion_viaje', conn, if_exists='append', index=False)
            print(f"- Archivo '{zonas_taxis}' cargado exitosamente en 'localizacion_viaje'.")
            
        except FileNotFoundError:
            print(f"⚠️ Error: No se encontró el archivo '{zonas_taxis}' en la carpeta actual.")
        except Exception as e:
            print(f"⚠️ Error al procesar el CSV: {e}")

        # Guardar cambios
        conn.commit()
        print("\n✅ Todos los catálogos han sido actualizados y guardados correctamente.")

    except sql.Error as e:
        print(f"❌ Error de base de datos: {e}")
        conn.rollback()
    
    finally:
        # Cerrar conexión
        conn.close()

if __name__ == "__main__":
    insertar_datos_catalogos()
