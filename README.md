![banner taxis](https://github.com/user-attachments/assets/f385580e-5717-4a27-ad55-b72d8674f8ae)
# Análisis descriptivo y optimización de arquitectura de datos para la comprensión del comportamiento de los pasajeros en horas pico en el sistema de transporte "Yellow Cars" de Nueva York (Octubre-Diciembre 2019).
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
**Objetivo General:**
Analizar el comportamiento de los pasajeros de los Yellow Taxis de Nueva York durante el trimestre octubre-diciembre de 2019, específicamente en los intervalos de mayor afluencia de usuarios, para comprender la influencia de la variable "hora" en el resto de los indicadores con la finalidad de construir perfiles comparativos entre pasajeros de "Hora Pico" y "Hora No Pico".

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

### ⚙️ Procesamiento de la Información

- **Normalización:** Reestructuración de las bases de datos originales para eliminar redundancias y establecer un esquema relacional sólido.
- **ETL & Data Lake:** Limpieza de registros inconsistentes y migración a formato Parquet, permitiendo un manejo fluido de la dimensión temporal y geográfica.
  
**Despliegue Analítico:**

- **En Power BI:** Visualización del comportamiento general del universo (Métricas macro).
- **A través de Streamlit:** Presentación de la investigación detallada y comparativa de perfiles (Investigación de nicho).

## BASE DE DATOS: NYC TAXI TRIPS 2019 💽
La Base de Datos está disponible en Kaggle que contiene información de millones de viajes en taxi durante el año 2019.
URL: https://www.kaggle.com/datasets/dhruvildave/new-york-city-taxi-trips-2019

##  Como usar? 🤔
### 1. Clona el Repositorio:

```bash
https://github.com/SamuB25/Analisis-Registros-de-Viajes-de-Taxis-Amarillos-en-Nueva-York-2019-Grupo-5.git
cd Analisis-Registros-de-Viajes-de-Taxis-Amarillos-en-Nueva-York-2019-Grupo-5
```
### 2. Instalar dependencias:
```bash
pip install -r requirements.txt
```
### 3. Correr la App:
```bash
streamlit run app.py
```
##  👑Visita nuestra App en Streamlit
[https://nyc2019eeca.streamlit.app/](https://nyc2019eeca.streamlit.app/)

## 📊 Dashboard Interactivo (Versión Web Power Bi)
Pueden visualizar el análisis preliminar aquí:
[👉 Ver Dashboard en Vivo](https://app.powerbi.com/view?r=eyJrIjoiNDRiYjIwYzktMjJkZC00NzNkLWI0OTItYTgyNzg3NGVkM2I2IiwidCI6IjRjODE4Zjc5LWFiODQtNDU1Mi05YjdjLTJmZTcxNWIwZDBkNSIsImMiOjR9)

## 👥 Créditos
**Equipo Grupo 5 - EECA UCV**
- Victoria Díaz (@vicoandrediaz): Lógica de inserción/exportación por chunks y arquitectura del Data Lake. Desarrollo del de la app de Streamlit. 
- Samuel (@SamuB25): Definición de reglas de negocio, limpieza de datos y filtros financieros. Desarrollo de la app de Streamlit.
- Yonelvis (@yonelvisgonzalez): Automatización de fuentes de datos y constantes del trimestre. Desarollo de la app de Streamlit.
- Andrés Morales: Diseño y desarrollo del Power Bi. 

**🎓 Agradecimientos**
- **Profesor Jesús Ochoa:** Por guiarnos hacia el uso de DuckDB y Parquet, elevando este proyecto a un estándar profesional de ingeniería de datos.
- **Profesor Oliver Triveño:** Por su constante apoyo y guía a lo largo del desarrollo de todo este proyecto. Su colaboración y asesoría han sido fundamentales para el diseño y despliegue del proyecto. 





