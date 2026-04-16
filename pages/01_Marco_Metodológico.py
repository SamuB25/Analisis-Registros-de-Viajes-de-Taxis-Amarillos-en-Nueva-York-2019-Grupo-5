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

# FILA 1
col1, col2 = st.columns(2, gap="large")

with col1:
    # Usamos '/' para que funcione en la nube (Linux)
    img_vic = cache_imagenes("assets/teamcard_1.jpg") 
    st.image(img_vic, use_container_width=True)
    st.markdown("### **Vico**")
    st.caption("Arquitecta de datos y líder de infraestructura.")

with col2:
    img_and = cache_imagenes("assets/teamcard_2.jpg")
    st.image(img_and, use_container_width=True)
    st.markdown("### **Andrés**")
    st.caption("Estratega de BI y visualización ejecutiva.")

st.markdown("<br>", unsafe_allow_html=True) # Espacio entre filas

# FILA 2
col3, col4 = st.columns(2, gap="large")

with col3:
    img_sam = cache_imagenes("assets/teamcard_3.jpg")
    st.image(img_sam, use_container_width=True)
    st.markdown("### **Samuel**")
    st.caption("Gestor de integridad de datos y soporte SQL.")

with col4:
    img_yon = cache_imagenes("assets/teamcard_4.jpg")
    st.image(img_yon, use_container_width=True)
    st.markdown("### **Yonelvis**")
    st.caption("Motor lógico de métricas estadísticas y cuestionario.")

# Sección del Pie de Página
st.markdown("---")
st.markdown("<center>Escuela de Estadística y Ciencias Actuarias - UCV 2026</center>", unsafe_allow_html=True)