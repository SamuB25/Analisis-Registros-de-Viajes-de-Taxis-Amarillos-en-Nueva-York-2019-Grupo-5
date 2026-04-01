![banner taxis](https://github.com/user-attachments/assets/f385580e-5717-4a27-ad55-b72d8674f8ae)
# Análisis descriptivo y optimización de arquitectura de datos para la comprensión del comportamiento de los pasajeros en horas pico en el sistema de transporte de Nueva York (Octubre-Diciembre 2019).
Este proyecto es una solución integral de análisis de datos que incorpora un proceso ETL creado para optimizar el procesamiento (desde la carga hasta la visualización de las métricas) de millones de registros de viajes de los Yellow Taxis en NYC (Octubre-Diciembre 2019). Nuestra aplicación transforma data cruda y fragmentada en diferentes bases de datos, seccionadas inicialmente por meses, en un Data Lake optimizado, permitiendo realizar un análisis descriptivo de alta velocidad. 

## **🛠️ ¿Por qué este Stack Tecnológico?**
Como estudiantes de la Escuela de Estadística y Ciencias Actuariales (EECA), entendemos que el volumen de datos actual requiere herramientas que superen el análisis tradicional:
- **Python (Pandas/SQLite):** Para la manipulación y el diseño de base de datos. 
- **SQLite:** Como motor de almacenamiento relacional inicial.
- **Parquet:** Nuestro Data Lake. Elegimos este formato columnar porque reduce drásticamente el espacio en disco y vuela al ser leído por herramientas de BI.
- **DuckDB:** Sugerido por el Prof. Jesús Ochoa, lo integramos para realizar consultas SQL ultra rápidas directamente sobre los archivos Parquet en nuestra App de Streamlit.

## Metodología Estadística
En cumplimiento con los estándares académicos de la Escuela de Estadística y Ciencias Actuariales (EECA), el presente proyecto se rige por un diseño de investigación descriptivo. Los resultados obtenidos, por ende, son de carácter descriptivo y no inferencial. 

### 🎯 Definición de Objetivos
**Objetivo General: **Analizar el comportamiento de los pasajeros de los Yellow Taxis de Nueva York durante el trimestre octubre-diciembre de 2019, específicamente en los intervalos de mayor afluencia de usuarios, para comprender la influencia de la variable "hora" en el resto de los indicadores con la finalidad de construir perfiles comparativos entre pasajeros de "Hora Pico" y "Hora No Pico".

**Objetivos Específicos:**
- Normalizar la base de datos relacional (SQLite) para garantizar la integridad referencial y la consistencia de la información.
- Transformar los registros crudos en un Data Lake limpio (Parquet) para optimizar la carga computacional durante el análisis descriptivo.
- Analizar la dimensión "Comportamiento del Pasajero" mediante el cálculo de estadísticos descriptivos y los indicadores señalados en la operacionalización de variables.
- Identificar patrones generales de movilidad y consumo en el universo de estudio mediante visualizaciones en Power BI.
- Segmentar y construir perfiles de clientes diferenciados en Streamlit, desglosando los hallazgos de la investigación estadística según el factor horario.

**Definición del Universo y Técnicas**
- **Universo:** Registros de viajes realizados por los Yellow Taxis en la ciudad de Nueva York (NYC) durante el cuarto trimestre (octubre, noviembre y diciembre) del año 2019.
- **Unidad de Análisis:** Cada registro individual de viaje (trip_id) registrado en la ciudad de Nueva York (NYC) durante el cuarto trimestre (octubre, noviembre y diciembre) del año 2019.
- **Técnicas Empleadas:** Cálculo de estadísticos descriptivos (Medidas de Tendencia Central, Frecuencias Absolutas/Relativas y Medidas de Dispersión).






