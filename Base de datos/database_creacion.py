import pandas as pd 
import numpy as np
import sqlite3 as sql

conn = sql.connect('taxis_nuevayork2019_trimestre.db') #Creamos la base de datos
#1.Creamos las entidades necesarias para nuestra database

#1.1 Creamos la entidad TPEP, para registrar al proveedor del dato. 
def crear_tabla_tpep():
    # 1. Conexión a la base de datos
    conn = sql.connect('taxis_nuevayork2019_trimestre.db')
    cursor = conn.cursor()

    # 2. Definición de la tabla con PK y restricción CHECK
    cursor.execute("""
        CREATE TABLE plataformas_tpep(
            vendor_id INTEGER PRIMARY KEY,
            plataforma VARCHAR(10) NOT NULL CHECK(plataforma IN ('ARRO', 'CURB'))
    )
    """
    )
    # 3. Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()
    print("Tabla 'plataformas_tpep' creada con restricciones.")
#1.2 Creamos la entidad REGISTRO_TRIP, la entidad central del modelo. 
def crear_tabla_registro_trip():
    # 1. Conexión a la base de datos
    conn = sql.connect('taxis_nuevayork2019_trimestre.db')
    cursor = conn.cursor() 
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS registro_viajes (
            trip_id INTEGER PRIMARY KEY AUTOINCREMENT, -- BigInt en SQLite es INTEGER
            vendor_id INTEGER,                         -- FK a plataformas_tpep
            pickup_date DATE,
            pickup_time TIME,
            dropoff_date DATE,
            dropoff_time TIME,
            pu_location_id INTEGER,                    -- FK a tabla de zonas (Pickup)
            do_location_id INTEGER,                    -- FK a tabla de zonas (Dropoff)
            passenger_count INTEGER,
            trip_distance DECIMAL(10,2),

            -- DEFINICIÓN DE LLAVES FORÁNEAS (FK)
            FOREIGN KEY (vendor_id) REFERENCES plataformas_tpep(vendor_id),
            FOREIGN KEY (pu_location_id) REFERENCES zonas(location_id),
            FOREIGN KEY (do_location_id) REFERENCES zonas(location_id)
        )
    """)
    # 3. Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()
    print("Tabla 'tabla_registro_trip' creada con restricciones.")
#1.3 Creamos la entidad Localizacion_viaje, en la que se registran todas las localizaciones recorridas por los taxis. 
def crear_tabla_localizacion_viaje():
    # 1. Conexión a la base de datos
    conn = sql.connect('taxis_nuevayork2019_trimestre.db')
    cursor = conn.cursor() 
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS localizacion_viaje (
            location_id INTEGER PRIMARY KEY,    -- PK: Identificador único de la zona
            borough TEXT,                       -- Condado (Manhattan, Brooklyn, etc.)
            zone TEXT,                          -- Nombre de la zona específica
            service_zone TEXT,                  -- Tipo de zona de servicio
            trip_id INTEGER,                    -- FK: Relación con el viaje
            FOREIGN KEY (trip_id) REFERENCES registro_viajes(trip_id)
        )
    """)
    # 3. Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()
    print("Tabla 'tabla_registro_trip' creada con restricciones.")
#1.4 Creamos la entidad detalle_financiero_viaje, en la que se registran todos los datos contables de los viajes. 
def crear_tabla_detalle_financiero_viaje():
    # 1. Conexión a la base de datos
    conn = sql.connect('taxis_nuevayork2019_trimestre.db')
    cursor = conn.cursor() 
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_financiero_viaje(
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT, -- PK única para el pago
            trip_id INTEGER,                               -- FK a la tabla de viajes
            vendor_id INTEGER,                             -- FK a la plataforma
            payment_type_id INTEGER,                       -- FK a tipos de pago (efectivo, tarjeta, etc.)
            fare_amount DECIMAL(10,2),
            extra DECIMAL(10,2),
            mta_tax DECIMAL(10,2),
            improvement_surcharge DECIMAL(10,2),
            tip_amount DECIMAL(10,2),
            tolls_amount DECIMAL(10,2),
            total_amount DECIMAL(10,2),
            FOREIGN KEY (trip_id) REFERENCES registro_viajes(trip_id),
            FOREIGN KEY (vendor_id) REFERENCES plataformas_tpep(vendor_id)
            -- Nota: Si creas una tabla de 'tipos_pago', agregarías la FK aquí
        )
    """)

    conn.commit()
    conn.close()
    print("Tabla 'detalle_financiero' creada con éxito.")
#1.5 Creamos la entidad de tarifa, en la que se registra el tipo de tarifa aplicado en cada viaje
def crear_tabla_tarifa():
    conn = sql.connect('taxis_nuevayork2019_trimestre.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarifa_viaje (
            trip_id INTEGER,
            vendor_id INTEGER,
            rate_code_id INTEGER,
            description VARCHAR(20),
            
            -- Definición de la PK Compuesta
            PRIMARY KEY (trip_id, rate_code_id),
            
            -- Definición de las FK
            FOREIGN KEY (trip_id) REFERENCES registro_viajes(trip_id),
            FOREIGN KEY (vendor_id) REFERENCES plataformas_tpep(vendor_id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tabla 'tarifa_viaje' creada con éxito.")
#1.5 Creamos la entidad de métodos de pago, en la que se registra el tipo de método de pago utilizado en cada viaje
def crear_tabla_metodo_pago():
    conn = sql.connect('taxis_nuevayork2019_trimestre.db')
    cursor = conn.cursor()

    # Activamos restricciones de integridad
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metodo_pago (
            trip_id INTEGER,
            payment_type_id INTEGER,
            description VARCHAR(25), -- Ej: 'Credit card', 'Cash', 'No charge'
            
            -- Definimos la PK Compuesta (la unión de ambos campos es única)
            PRIMARY KEY (trip_id, payment_type_id),
            
            -- Definimos la relación con la tabla principal de viajes
            FOREIGN KEY (trip_id) REFERENCES registro_viajes(trip_id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tabla 'metodo_pago' creada correctamente.")
#1.6 Creamos la entidad de registro_financiero_delviaje , en la que se registra el tipo de método de pago utilizado en cada viaje
def crear_tabla_registro_financiero():
    conn = sql.connect('taxis_nuevayork2019_trimestre.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registro_financiero_viaje (
            trip_id INTEGER,
            vendor_id INTEGER,
            store_and_fwd_flag CHAR(1),
            rate_code_id INTEGER,
            payment_id INTEGER UNIQUE,

            -- Definición de Llaves Foráneas (FK)
            FOREIGN KEY (trip_id) REFERENCES registro_viajes(trip_id),
            FOREIGN KEY (vendor_id) REFERENCES plataformas_tpep(vendor_id),
            FOREIGN KEY (payment_id) REFERENCES detalle_financiero(payment_id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tabla 'registro_financiero_viaje' creada con éxito.")

crear_tabla_tarifa()
crear_tabla_registro_trip()
crear_tabla_localizacion_viaje()
crear_tabla_registro_financiero()
crear_tabla_detalle_financiero_viaje()
crear_tabla_metodo_pago()

