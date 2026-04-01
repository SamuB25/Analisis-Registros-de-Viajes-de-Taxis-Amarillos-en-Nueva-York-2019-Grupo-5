![banner taxis](https://github.com/user-attachments/assets/f385580e-5717-4a27-ad55-b72d8674f8ae)
#Análisis descriptivo y optimización de arquitectura de datos para la comprensión del comportamiento de los pasajeros en horas pico en el sistema de transporte de Nueva York (Octubre-Diciembre 2019).
---
Este proyecto es una solución integral de análisis de datos que incorpora un proceso ETL creado para optimizar el procesamiento (desde la carga hasta la visualización de las métricas) de millones de registros de viajes de los Yellow Taxis en NYC (Octubre-Diciembre 2019). Nuestra aplicación transforma data cruda y fragmentada en diferentes bases de datos, seccionadas inicialmente por meses, en un Data Lake optimizado, permitiendo realizar un análisis descriptivo de alta velocidad. 
---
##**🛠️ ¿Por qué este Stack Tecnológico?**
Como estudiantes de la Escuela de Estadística y Ciencias Actuariales (EECA), entendemos que el volumen de datos actual requiere herramientas que superen el análisis tradicional:
-Python (Pandas/SQLite): Para la manipulación y el diseño de base de datos. 
-SQLite: Como motor de almacenamiento relacional inicial.
-Parquet: Nuestro Data Lake. Elegimos este formato columnar porque reduce drásticamente el espacio en disco y vuela al ser leído por herramientas de BI.
-DuckDB: Sugerido por el Prof. Jesús Ochoa, lo integramos para realizar consultas SQL ultra rápidas directamente sobre los archivos Parquet en nuestra App de Streamlit.


