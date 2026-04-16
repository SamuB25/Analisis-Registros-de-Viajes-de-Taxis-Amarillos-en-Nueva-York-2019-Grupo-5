import streamlit as st

def mostrar_conclusiones_finales():
    st.title("🏁 Conclusiones del Proyecto: 'Yellow Cars' NYC 2019")

    # 1. Infraestructura y Optimización
    with st.expander("🛠️ 1. Infraestructura y optimización de los datos", expanded=False):
        st.markdown("""
        * **Integridad referencial y consistencia:** La fase de normalización permitió poner orden al caos inicial que nos generaban los datos crudos. Al estructurar la información en tablas conectadas de forma lógica, logramos optimizar en gran medida el manejo de los datos evitando cualquier clase de duplicidad en los datos y los datos sean coherentes con la investigación.
        * **Eficiencia del Data Lake:** La transformación de los registros base a un formato parquet es sin lugar a duda el proceso que mas beneficioso resulto para la viabilidad del proyecto. Permitió reducir drasticamente la carga que sufrirían los equipos de trabajo del equipo y además de facilitar análizar rapidamente los **20.6 millones de registros** abarcados en la investigación para las consultas necesarias. 
        """)

    # 2. Perfiles Comparativos (El corazón de la página)
    st.header("👥 2. Caracterización de la Población")
    
    # Bloque de Perfil General
    st.info("### 📍 Perfil General del Trimestre (Octubre-Diciembre)")
    st.write("Métricas base calculadas sobre el universo total de viajes:")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Tarifa Promedio", "$13.30")
    c2.metric("Propina Estándar", "$2.27")
    c3.metric("Distancia Promedio", "2.98 mi")
    st.caption("Fuente: Datos del trimestre analizados en la investigación.")

    st.markdown("---")

    # Comparativa de Segmentos con Metodología
    st.subheader("📊 Perfiles Comparativos: Hora Pico vs. No Pico")
    col_pico, col_no_pico = st.columns(2)

    with col_pico:
        st.markdown("#### 🚀 Hora Pico")
        st.write("**Volumen:** 3.6M de viajes")
        st.metric("Propina Promedio", "$2.40", "+$0.13")
        st.metric("Distancia Promedio", "2.78 mi", "-0.20 mi")
        st.write("*Caracterizado por viajes concentrados en **distancias cortas**.*")

    with col_no_pico:
        st.markdown("#### 🌙 Hora No Pico")
        st.write("**Volumen:** 16.9M de viajes ")
        st.metric("Propina Promedio", "$2.25", "-$0.02")
        st.metric("Distancia Promedio", "3.02 mi", "+0.04 mi")
        st.write("*Viajes concentrados en **distancias más largas**.*")

    # 3. Sección Añadida: Análisis de Movilidad y Hallazgos
    st.header("🧠 3. Análisis de Movilidad y Hallazgos")
    
    # Usamos columnas para resaltar los hallazgos clave
    hal1, hal2 = st.columns(2)
    
    with hal1:
        st.markdown("##### 🕒 El Factor 'Hora'")
        st.write("""
        El análisis descriptivo genero indicios que la variable "hora" actua como el principal diferenciador, 
        afectando tanto la eficiencia del viaje como los costos del mismo y la generocidad del usuario.
        """)

    with hal2:
        st.markdown("##### 📍 Puntos Calientes")
        st.write("""
        Los patrones de movilidad no son aleatorios; siguen una **estructura urbana predecible** marcada por la actividad comercial de la ciudad.
        """)

    st.success("""
    **💡 Hallazgo Destacado:** A pesar de que en Hora Pico las distancias disminuyen a **2.78 millas**, la gratificación promedio sube a **$2.40**. 
    Esto sugiere que la población mantiene una alta tolerancia al costo y una mayor generosidad en condiciones de tráfico crítico.
    """)

    # 4. Recomendaciones
    st.divider()
    st.subheader("🚀 Recomendaciones para Futuros Equipos")
    st.markdown("""
    Debido a la naturaleza descriptiva de esta investigación, se recomienda a futuros equipos:
    * **Analizar la rentabilidad:** Calcular qué viajes resultan más beneficiosos para los conductores, ya que esto requiere un enfoque más allá de la estadística descriptiva.
    * **Estudio de Causalidad:** Investigar si el nivel de tráfico (tiempo de viaje) tiene una relación inversamente proporcional con el porcentaje de propina otorgado.
    """)

mostrar_conclusiones_finales()