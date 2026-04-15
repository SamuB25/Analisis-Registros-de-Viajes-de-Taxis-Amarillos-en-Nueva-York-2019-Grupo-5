import duckdb
import os
import streamlit as st #incluimos ésta dependencia FUNDAMENTAL porque es el entorno de ejecución del proyecto

# Configuramos el lugar donde vamos a guardar y organizar nuestras tablas que se encuentran en "data".
class QueryManager:
    def __init__(self):
        # Usamos :memory: para que sea un rayo y no dependa de archivos locales
        self.con = duckdb.connect(database=':memory:')
        self._register_tables()

    def _register_tables(self):
        # Localizamos 'data' subiendo un nivel desde 'src' (Raíz del proyecto)
        dir_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_data = os.path.abspath(os.path.join(dir_actual, "..", "data"))

        # Diccionario de tablas (Mapeo de archivos Parquet)
        tables = {
            "finanzas": "finanzas_viaje.parquet", #nos aseguramos cada nombre en el diccionario coincida 
            "localizacion": "localizacion_viaje.parquet",
            "pagos": "metodo_pago.parquet",
            "plataformas": "plataformas_tpep.parquet",
            "viaje": "registro_viajes.parquet",
            "tarifas": "tarifas.parquet"
        }

        for name_table, archive in tables.items():
            ruta_archive = os.path.join(ruta_data, archive)
            
            if os.path.exists(ruta_archive):
                # Creamos una VISTA. DuckDB no "copia" los datos, los lee directo del Parquet
                # Buscamos cumplir con el pilar fundamental del diseño a través de rutas relativas propias del entorno del proyecto
                self.con.execute(f"CREATE OR REPLACE VIEW {name_table} AS SELECT * FROM read_parquet('{ruta_archive}')")
            else:
                # Si llegamos aquí, es que drive_conn.py falló o la ruta está mal
                st.error(f"❌ Error Crítico: No se encontró el archivo {archive} en {ruta_data}")

    def execute_query(self, sql):
        """Ejecuta SQL y devuelve DataFrame para las visualizaciones o la terminal."""
        try:
            return self.con.execute(sql).df()
        except Exception as e:
            # Manejo de errores para que la app no explote (Pilar #5) 
            return f"⚠️ Error en la consulta: {str(e)}"

# Designamos una función para inyectar el manager en el estado de Streamlit (Caching)
@st.cache_resource #Optimizamos el funcionamiento de la app mediante el CACHE
def get_query_manager():
    return QueryManager()

