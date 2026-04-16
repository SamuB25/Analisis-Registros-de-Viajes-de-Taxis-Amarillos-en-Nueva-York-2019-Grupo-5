import os #Para agilizar el manejo de permisos y gestión de archivos/carpetas.
import gdown #Esto nos permitira descargar los archivos (parquet) de google drive.
import streamlit as st #preparamos el cache de la app. 

#Guardamos la llave primaria de la carpeta de DRIVE en el que se aloja el DATA LAKE
FOLDER_ID = "1HxA98TMS4uUT_CCZQk1J_uKOZQT1ygHl"

#Iniciamos con la preparación del cache de la app
@st.cache_resource
def preparar_data_lake():
    """
    Descarga la carpeta completa de Drive y asegura la estructura de datos.
    """
    # Localizamos la raíz del proyecto para conectar
    # Subimos un nivel desde 'src' para encontrar la raíz
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")

    # Si la carpeta data no existe, la creamos
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Verificamos si la carpeta está vacía (si hay parquets, no descargamos nada)
    if not os.listdir(data_dir):
        st.warning("Iniciando descarga del Data Lake desde Google Drive...")
        url = f"https://drive.google.com/drive/folders/{FOLDER_ID}?usp=sharing"
        
        try:
            # gdown.download_folder baja TODO lo que esté en ese link
            gdown.download_folder(url, output=data_dir, quiet=False, use_cookies=False)
            st.success("Datos descargados exitosamente.")
            return True
        except Exception as e:
            st.error(f"Error crítico de conexión: {e}")
            return False
    else:
        # Si ya hay archivos, no hacemos perder tiempo al usuario
        return True