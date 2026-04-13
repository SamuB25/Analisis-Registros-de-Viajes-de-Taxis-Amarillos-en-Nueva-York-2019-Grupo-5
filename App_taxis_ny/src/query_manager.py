import duckdb
import os


# Configuramos el lugar donde vamos a guardar y organizar nuestras tablas que se encuentran en "data".
class query_manager:
    def __init__(self,db_path="taxis_ny.db"):
        # Creamos la conexión que se va a utilizar con los archivos.A parte de que se creara el archivo de "taxis.ny.db"
        self.con = duckdb.connect(db_path)
        self._register_tables()

    def _register_tables(self):
        # Creamos una función que busque los archivo dentro de "data".
        # Comenzando con la ruta de los archivos.
        dir_data = os.path.dirname(os.path.abspath(__file__)) # Mediante la ubicación de este archivo coordinamos la ruta
        # de forma en que dir_data sepa que debe trabajar en la carpeta "src", con el join le indicamos que avance en esa carpeta y entre a "data".
        ruta_data = os.path.join(dir_data, "..", "data")

        # Creamos un diccionario que identifique el nombre de la tabla y su archivo correspondiente.

        tables = {
            "finanzas":"finanzas_viaje.parquet",
            "locaización":"localizacion_viaje.parquet",
            "pagos":"metodo_pago.parquet",
            "plataformas":"plataformas_tpep.parquet",
            "viaje":"registro_viaje.parquet",
            "tarifas":"tarifas.parquet"
            }

        print("Iniciando registro de Tablas.")

        for name_table, archive in tables.items():
            ruta_archive = os.path.join(ruta_data, archive)
        # Creamos un leve filtro que verifique la existencia del archivo en el dispositivo.

            if os.path.exists(ruta_archive):
                self.con.execute(f"CREATE OR REPLACE VIEW {name_table} AS SELECT * FROM read_parquet('{ruta_archive}')")
                print(f"Tabla {name_table} esta lista")
            else:
                print(f" ADVERTENCIA: No se encontró ´{archive}´ en la carpeta data.")
        print("Configuraciones de registro finalizadas.")
    
    def execute_query(self, sql):
        # Para que los querys se ejecuten desde sql y devuelva un dataframe
        return self.con.execute(sql).df()
    test = print("query_manager listo para ejecutar consultas SQL.")

