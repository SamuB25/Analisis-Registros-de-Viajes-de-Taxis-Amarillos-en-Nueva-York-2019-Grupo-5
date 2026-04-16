import streamlit as st 
from PIL import Image # fundamental para la optimización del caché

# --- FUNCIÓN DE CARGA OPTIMIZADA ---
@st.cache_data
def cache_imagenes(path):
    """
    Lee la imagen del disco una sola vez y la guarda en cache.
    """
    return Image.open(path)

st.markdown("""
    <style>
    .justificado {
        text-align: justify;
    }
    .destaque {
        color: #F2BC1B; /* Tu amarillo taxi */
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Planteamiento del Problema y Marco Metodológico")
st.markdown("---")

st.header("1.1. Planteamiento del Problema")
with st.container():
    st.markdown("""<div class="justificado">
    La dinámica urbana de grandes metrópolis como Nueva York se fundamenta en sistemas de transporte masivos y selectivos que generan volúmenes masivos de datos cada segundo. Dentro de este ecosistema, los Yellow Taxis representan un pilar histórico y logístico cuya operatividad no solo refleja la movilidad de la ciudad, sino también el comportamiento socioeconómico de sus usuarios en contextos temporales específicos.<br><br>
    En la actualidad, el análisis de grandes bases de datos (Big Data) se ha convertido en una necesidad intelectual y vital para comprender fenómenos complejos. Sin embargo, a pesar de la disponibilidad de registros detallados proporcionados por la Taxi & Limousine Commission (TLC), los datos crudos a menudo presentan inconsistencias o redundancias que dificultan su interpretación directa. Para que el conocimiento sea considerado científico, este debe ser <span class="destaque">metódicamente obtenido y sistemáticamente organizado</span> según Fidias G. Arias (2012), lo que exige procesos rigurosos de normalización y transformación digital (ETL) antes de proceder a cualquier análisis estadístico. <br><br>
    Específicamente durante el trimestre octubre-diciembre de 2019, se observa una fluctuación considerable en la demanda del servicio. Surge entonces una interrogante sobre cómo factores temporales, particularmente la variable "hora", condicionan el comportamiento del pasajero en términos de consumo y movilidad. El desconocimiento de los patrones diferenciados entre los periodos de alta demanda (Hora Pico) y periodos regulares (Hora No Pico) representa un vacío de información que impide la construcción de perfiles de usuario precisos.<br><br>
    Sin un análisis descriptivo profundo que segmente estos registros, la información permanece como un conjunto de datos aislados sin utilidad práctica para la toma de decisiones estratégicas o la optimización del servicio. Por tanto, se requiere una investigación que, mediante el uso de herramientas tecnológicas avanzadas como <b>Power BI y Streamlit<b>, permita caracterizar la estructura de comportamiento de este universo de estudio.</div>
    """, unsafe_allow_html=True)
    st.markdown("---")

st.header("1.2. La Pregunta de Investigación")
with st.container():
    st.markdown("""¿Cómo varía el comportamiento de los pasajeros de los Yellow Taxis de Nueva York según el factor horario (Hora Pico vs. Hora No Pico) durante el trimestre octubre-diciembre del año 2019?""")
# Sección de presentación del equipo
st.header("Conoce a nuestro equipo de investigación y desarrollo (grupo 5)")
st.write("Los encargados de transformar el caos de NYC en DATOS")

# FILA 1
col1, col2 = st.columns(2, gap="large")

with col1:
    img_vic = cache_imagenes("assets/teamcard_1.png") 
    st.image(img_vic, use_container_width=True)
    st.markdown("### **Vico**")
    st.caption("Arquitecta de datos y líder de infraestructura.")

with col2:
    img_and = cache_imagenes("assets/teamcard_2.png")
    st.image(img_and, use_container_width=True)
    st.markdown("### **Andrés**")
    st.caption("Estratega de BI y visualización ejecutiva.")

st.markdown("<br>", unsafe_allow_html=True) # Espacio entre filas

# FILA 2
col3, col4 = st.columns(2, gap="large")

with col3:
    img_sam = cache_imagenes("assets/teamcard_3.png")
    st.image(img_sam, use_container_width=True)
    st.markdown("### **Samuel**")
    st.caption("Gestor de integridad de datos y soporte SQL.")

with col4:
    img_yon = cache_imagenes("assets/teamcard_4.png")
    st.image(img_yon, use_container_width=True)
    st.markdown("### **Yonelvis**")
    st.caption("Motor lógico de métricas estadísticas y cuestionario.")

# Sección del Pie de Página
st.markdown("---")
st.markdown("<center>Escuela de Estadística y Ciencias Actuariales - UCV 2026</center>", unsafe_allow_html=True)