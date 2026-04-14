import duckdb
import os

class query_manager:
    # 1. CAMBIO: Usamos ':memory:' en lugar de un archivo físico
    def __init__(self, db_path=":memory:"):
        self.con = duckdb.connect(db_path)
        self._register_tables()

    def _register_tables(self):
        dir_data = os.path.dirname(os.path.abspath(__file__))
        ruta_data = os.path.join(dir_data, "..", "..", "data")

        # 2. CAMBIO: Los nombres de las claves ahora coinciden EXACTAMENTE 
        # con las tablas de stats_logic.py y app.py
        tables = {
            "finanzas_viaje": "finanzas_viaje.parquet",
            "localizacion_viaje": "localizacion_viaje.parquet",
            "metodo_pago": "metodo_pago.parquet",
            "plataformas_tpep": "plataformas_tpep.parquet",
            "registro_viajes": "registro_viaje.parquet",
            "tarifas": "tarifas.parquet"
        }

        print("Iniciando registro de Tablas.")

        for name_table, archive in tables.items():
            ruta_archive = os.path.join(ruta_data, archive)

            if os.path.exists(ruta_archive):
                self.con.execute(f"CREATE OR REPLACE VIEW {name_table} AS SELECT * FROM read_parquet('{ruta_archive}')")
                print(f"Tabla {name_table} está lista")
            else:
                print(f"ADVERTENCIA: No se encontró '{archive}' en la carpeta data.")
        print("Configuraciones de registro finalizadas.")
    
    def execute_query(self, sql):
        return self.con.execute(sql).df()
    test = print("query_manager listo para ejecutar consultas SQL.")

