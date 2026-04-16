import os #Para agilizar el manejo de permisos y gestión de archivos/carpetas.
import gdown #Esto nos permitira descargar los archivos (parquet) de google drive.
import streamlit as st #preparamos el cache de la app. 

#Guardamos la llave primaria de la carpeta de DRIVE en el que se aloja el DATA LAKE
FOLDER_ID = "1HxA98TMS4uUT_CCZQk1J_uKOZQT1ygHl"

#Iniciamos con la preparación del cache de la app
@st.cache_resource
def preparar_data_lake():
    """
    Descarga la carpeta de Drive de forma silenciosa y asegura la estructura.
    """
    # 1. Localizamos la raíz del proyecto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")

    # 2. Creación silenciosa de la carpeta si no existe
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # 3. Verificamos si la carpeta está vacía
    if not os.listdir(data_dir):
        url = f"https://drive.google.com/drive/folders/{FOLDER_ID}?usp=sharing"
        
        try:
            #quiet=True para que no haya rastro de la descarga
            gdown.download_folder(url, output=data_dir, quiet=True, use_cookies=False)
            return True
        except Exception:
            
            return False
    else:
        
        return True