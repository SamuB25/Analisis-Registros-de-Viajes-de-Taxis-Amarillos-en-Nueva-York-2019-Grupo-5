import pandas as pd 
import numpy as np
import sqlite3 as sql

#1.Creación de la base de datos normalizada

#Creamos la entidad TPEP, para registrar el catálogo de proveedores del dato.
def crear_tabla_tpep():
    conn = sql.connect('taxis_nuevayork2019_trimestre.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plataformas_tpep(
            vendor_id INTEGER PRIMARY KEY,
            plataforma TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("Tabla 'plataformas_tpep' creada con restricciones.")

#Creamos la entidad Localizacion_viaje, en la que se registran todas las localizaciones recorridas por los taxis. 
def crear_tabla_localizacion_viaje():
    conn = sql.connect('taxis_nuevayork2019_trimestre.db')
    cursor = conn.cursor() 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS localizacion_viaje(
            location_id INTEGER PRIMARY KEY,
            borough TEXT,
            zone TEXT,
            service_zone TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Tabla 'localizacion_viaje' creada exitosamente.")

#Creamos la entidad de tarifa, en la que se registra el tipo de tarifa aplicado en cada viaje
def crear_tabla_tarifas():
    conn = sql.connect('taxis_nuevayork2019_trimestre.db')
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tarifas (
            rate_code_id INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL
        )
    """)
    conn.close()
    print("Tabla 'tarifas' creada con éxito.")

#Creamos la entidad de métodos de pago, en la que se registra el tipo de método de pago utilizado en cada viaje
def crear_tabla_metodo_pago():
    conn = sql.connect('taxis_nuevayork2019_trimestre.db')
    conn.execute("""
        CREATE TABLE IF NOT EXISTS metodo_pago (
            payment_type_id INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL
        )
    """)
    conn.close()
    print("Tabla 'metodo_pago' creada correctamente.")

#Creamos la entidad REGISTRO_TRIP, la entidad central del modelo. 
def crear_tabla_registro_trip():
    conn = sql.connect('taxis_nuevayork2019_trimestre.db')
    cursor = conn.cursor() 
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registro_viajes (
            trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_id INTEGER,
            rate_code_id INTEGER,      -- FK al catálogo de tarifas
            payment_type_id INTEGER,   -- FK al catálogo de pagos
            pickup_date DATE,
            pickup_time TIME,
            dropoff_date DATE,
            dropoff_time TIME,
            pu_location_id INTEGER,
            do_location_id INTEGER,
            passenger_count INTEGER,
            trip_distance DECIMAL(10,2),
            FOREIGN KEY (vendor_id) REFERENCES plataformas_tpep(vendor_id),
            FOREIGN KEY (rate_code_id) REFERENCES tarifas(rate_code_id),
            FOREIGN KEY (payment_type_id) REFERENCES metodo_pago(payment_type_id),
            FOREIGN KEY (pu_location_id) REFERENCES localizacion_viaje(location_id),
            FOREIGN KEY (do_location_id) REFERENCES localizacion_viaje(location_id)
        )
    """)
    conn.commit()
    conn.close()
    print("Tabla 'tabla_registro_trip' creada exitosamente.")

#Unificamos los hechos financieros en una sola entidad. 
def crear_tabla_finanzas_viaje():
    conn = sql.connect('taxis_nuevayork2019_trimestre.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finanzas_viaje (
            trip_id INTEGER PRIMARY KEY,   -- Relación 1:1 con el viaje
            vendor_id INTEGER,
            payment_type_id INTEGER,
            store_and_fwd_flag TEXT,
            fare_amount REAL,
            extra REAL,
            mta_tax REAL,
            tip_amount REAL,
            tolls_amount REAL,
            improvement_surcharge REAL,
            total_amount REAL,
            FOREIGN KEY (trip_id) REFERENCES registro_viajes(trip_id),
            FOREIGN KEY (vendor_id) REFERENCES plataformas_tpep(vendor_id),
            FOREIGN KEY (payment_type_id) REFERENCES metodo_pago(payment_type_id)
        )
    """)
    conn.commit()
    conn.close()
    print("Tabla 'finanzas_viaje' unificada y lista.")

#BLOQUE DE EJECUCIÓN

# 1. Primero los catálogos (imprescindible para las FK)
crear_tabla_tpep()
crear_tabla_localizacion_viaje()
crear_tabla_tarifas()
crear_tabla_metodo_pago()

# 2. Luego las tablas centrales de registro
crear_tabla_registro_trip()
crear_tabla_finanzas_viaje()


