import streamlit as st 
from PIL import Image # fundamental para la optimización del caché

# --- FUNCIÓN DE CARGA OPTIMIZADA ---
@st.cache_data
def cache_imagenes(path):
    """
    Lee la imagen del disco una sola vez y la guarda en cache.
    """
    return Image.open(path)

# Sección de presentación del equipo
st.header("Conoce al grupo 5. Los encargados de transformar el caos de NYC en DATOS")
st.write("El equipo detrás de la arquitectura, análisis y estrategia del proyecto.")

# Creamos las 4 columnas para presentar las cards
col_vic, col_and, col_sam, col_yon = st.columns(4)

# Ahora usamos la función cacheada en lugar de la ruta directa
with col_vic:
    img_vic = cache_imagenes("assets\teamcard_1.png")
    st.image(img_vic, use_container_width=True)
    st.caption("**Vico** - La cabeza detrás de la visualización")

with col_and:
    img_and = cache_imagenes("assets\teamcard_2.png")
    st.image(img_and, use_container_width=True)
    st.caption("**Andrés** - El encargado del Power BI")

with col_sam:
    img_sam = cache_imagenes("assets\teamcard_3.png")
    st.image(img_sam, use_container_width=True)
    st.caption("**Samuel** - El gestor de la integridad de los datos y los querys")

with col_yon:
    img_yon = cache_imagenes("assets\teamcard_4.png")
    st.image(img_yon, use_container_width=True)
    st.caption("**Yonelvis** - El Motor lógico de las métricas estadísticas y los querys")
st.markdown("---")

# Sección del Pie de Página
st.markdown("---")
st.markdown("<center>Escuela de Estadística y Ciencias Actuarias - UCV 2026</center>", unsafe_allow_html=True)