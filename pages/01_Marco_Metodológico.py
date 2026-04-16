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

st.image("assets/taxis_banner.png", use_column_width=True)

st.header("1.1. Planteamiento del Problema")
with st.container():
    st.markdown("""<div class="justificado">
    La dinámica urbana de grandes metrópolis como Nueva York se fundamenta en sistemas de transporte masivos y selectivos que generan volúmenes masivos de datos cada segundo. Dentro de este ecosistema, los Yellow Taxis representan un pilar histórico y logístico cuya operatividad no solo refleja la movilidad de la ciudad, sino también el comportamiento socioeconómico de sus usuarios en contextos temporales específicos.<br><br>
    En la actualidad, el análisis de grandes bases de datos (Big Data) se ha convertido en una necesidad intelectual y vital para comprender fenómenos complejos. Sin embargo, a pesar de la disponibilidad de registros detallados proporcionados por la Taxi & Limousine Commission (TLC), los datos crudos a menudo presentan inconsistencias o redundancias que dificultan su interpretación directa. Para que el conocimiento sea considerado científico, este debe ser <span class="destaque">metódicamente obtenido y sistemáticamente organizado</span> según Fidias G. Arias (2012), lo que exige procesos rigurosos de normalización y transformación digital (ETL) antes de proceder a cualquier análisis estadístico. <br><br>
    Específicamente durante el trimestre octubre-diciembre de 2019, se observa una fluctuación considerable en la demanda del servicio. Surge entonces una interrogante sobre cómo factores temporales, particularmente la variable "hora", condicionan el comportamiento del pasajero en términos de consumo y movilidad. El desconocimiento de los patrones diferenciados entre los periodos de alta demanda (Hora Pico) y periodos regulares (Hora No Pico) representa un vacío de información que impide la construcción de perfiles de usuario precisos.<br><br>
    Sin un análisis descriptivo profundo que segmente estos registros, la información permanece como un conjunto de datos aislados sin utilidad práctica para la toma de decisiones estratégicas o la optimización del servicio. Por tanto, se requiere una investigación que, mediante el uso de herramientas tecnológicas avanzadas como <b>Power BI y Streamlit<b>, permita caracterizar la estructura de comportamiento de este universo de estudio.</div>
    """, unsafe_allow_html=True)
    st.markdown("---")

# PREGUNTA DE INVESTIGACIÓN
st.markdown("""
    <style>
    .pregunta-container {
        background-color: #121212; /* Asphalt Night */
        border-left: 10px solid #F2BC1B; /* Borde Taxi Yellow */
        padding: 30px;
        border-radius: 10px;
        margin: 40px 0px;
        box-shadow: 0px 4px 15px rgba(242, 188, 27, 0.2);
    }
    .pregunta-texto {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: bold;
        font-style: italic;
        line-height: 1.5;
        text-align: center;
    }
    .pregunta-label {
        color: #F2BC1B;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

# VISTA DE LA PREGUNTA EN LA APP
st.markdown("""
    <div class="pregunta-container">
        <span class="pregunta-label">Interrogante de Investigación</span>
        <p class="pregunta-texto">
            "¿Cómo varía el comportamiento de los pasajeros de los Yellow Taxis de Nueva York según el factor horario (Hora Pico vs. Hora No Pico) durante el trimestre octubre-diciembre del año 2019?"
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .justificado { text-align: justify; }
    .destaque { color: #F2BC1B; font-weight: bold; }
    .depto-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #F2BC1B;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SECCIÓN 2: MARCO METODOLÓGICO ---
st.header("2. Marco Metodológico")

# --- 2.1 NIVEL DE INVESTIGACIÓN ---
with st.expander("🔍 2.1. Nivel de Investigación", expanded=True):
    st.markdown("""
    <div class="justificado">
    De acuerdo con los objetivos planteados, la presente investigación se define como de <span class="destaque">nivel descriptivo</span>. 
    Según <b>Arias (2012)</b>, la investigación descriptiva consiste en la caracterización de un hecho o fenómeno con el fin 
    de establecer su estructura o comportamiento.
    <br><br>
    En este sentido, el estudio se limita a describir el comportamiento de los pasajeros de los Yellow Taxis en Nueva York 
    durante el cuarto trimestre de 2019. Al regirse por los estándares de la <b>Escuela de Estadística y Ciencias Actuariales</b>, 
    los resultados poseen un carácter estrictamente descriptivo, absteniéndose de realizar inferencias más allá del 
    universo de datos procesado.
    </div>
    """, unsafe_allow_html=True)

# JUSTIFICACIÓN TEORICA
st.header("2.2. Justificación de la Investigación")

st.markdown("""
<div class="justificado">
La relevancia de esta investigación reside en la necesidad crítica de transformar datos masivos en 
<b>conocimiento estratégico</b>. La normalización en <b>SQLite</b> y la implementación de un sistema 
<span class="destaque">OLAP (On-Line Analytical Processing)</span> resultan fundamentales para este modelo de negocio.
<br><br>
Mientras que las consultas analíticas tradicionales demandan un tiempo computacional excesivo, los sistemas OLAP 
permiten integrar y pre-calcular los datos (Data Lake en Parquet), garantizando la velocidad y precisión que el entorno actual exige.
</div>
""", unsafe_allow_html=True)

st.write("") # Espacio

# JUSTIFICACION POR DEPARTAMENTO
st.subheader("Impacto Institucional y Organizativo")

# Usamos columnas para los departamentos para que no sea una lista infinita
col_mkt, col_cont = st.columns(2)

with col_mkt:
    st.markdown("""
    <div class="depto-card">
    <b>🎯 Marketing</b><br>
    Segmentación y perfiles de clientes en Streamlit para identificar nichos según el factor horario y optimizar campañas.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="depto-card">
    <b>📈 Logística</b><br>
    Visualización en Power BI para detectar picos de demanda y asignar eficientemente los recursos en la ciudad.
    </div>
    """, unsafe_allow_html=True)

with col_cont:
    st.markdown("""
    <div class="depto-card">
    <b>💰 Contabilidad</b><br>
    Visión clara de flujos de ingresos y métricas de consumo para proyecciones financieras ajustadas a la realidad.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="depto-card">
    <b>🚀 Tecnología</b><br>
    Reducción de carga computacional mediante el uso de Parquet, mejorando la agilidad en la toma de decisiones.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

#PRESENTACIÓN DEL EQUIPO DE DESARROLLO
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