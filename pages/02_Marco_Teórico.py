import streamlit as st
import pandas as pd


st.title("Análisis del comportamiento de los pasajeros en horas pico en el sistema de transporte Yellow Cars de Nueva York (Octubre-Diciembre 2019)")

st.header("Marco teórico")

st.subheader("Antecedentes")

st.write("En la ciudad de Nueva York, el ecosistema del transporte por contrato es una de las redes de movilidad urbana más densas, con mayor regulación y mayor desarrollo tecnológico a nivel global. Los emblemáticos taxis amarillos, cuya identidad ha ido más allá de la simple función de transporte hasta transformarse en un símbolo cultural y un soporte de la economía metropolitana, son el núcleo central de esta red. El año 2019 se destaca como un tiempo de cambio significativo, caracterizado por la convergencia de una crisis financiera en el valor de las licencias, la puesta en marcha de acciones fiscales para reducir el embotellamiento urbano y el fortalecimiento de infraestructuras tecnológicas creadas para competir con las plataformas de transporte a través de aplicaciones.")

st.write("Para entender cómo funcionan los taxis amarillos en 2019, es esencial precisar su naturaleza operativa y jurídica dentro de la Comisión de Taxis y Limusinas de Nueva York (TLC). En la ciudad de Nueva York, solo un taxi amarillo, también denominado ¨medallion taxi¨, está legalmente habilitado para recibir viajes que se soliciten por el método de señal de mano en la calle, sin importar en qué parte de los cinco condados se encuentre. Esta exclusividad es el centro del sistema de medallones, un modelo de licencias que sirve como un instrumento para controlar la oferta del gobierno, concebido en sus inicios con el objetivo de evitar el desorden en el tráfico y garantizar que el sector sea rentable.")

st.write("A fines del siglo XIX, se inició el desarrollo del sistema de taxis en Nueva York con la incorporación de los taxis amarillos a gasolina por parte de Harry Allen en 1907. La ausencia de reglamentación provocó que el mercado se saturara. En la década de 1930, el concejal Lew Haas planteó la Ley Haas, que restringía a 13,595 el número de licencias; este número se mantuvo por un periodo de 60 años, lo que hizo que los medallones adquiriesen un alto valor. El costo de los medallones pasó de $2,500 a más de un millón de dólares entre 1947 y 2013. Uber y Lyft, al tener regulaciones más flexibles, trajeron consigo más de 80 000 autos. Esto hizo que el precio de los medallones disminuyera en un 50% para el año 2018.")

#Creacion de una tabla con la evolución histórica de los taxis en Nueva York
def mostrar_tabla_historica():
    st.subheader("Evolución Histórica de los Taxis en Nueva York")
    
    # Diccionario para la tabla
    datos_historia = {
        "Período Histórico": [
            "1907", 
            "1937-1938", 
            "1960", 
            "1971", 
            "2013-2014", 
            "2019"
        ],
        "Evento Histórico": [
            "Debut de los taxis de gasolina",
            "Aprobación de la Ley Haas",
            "Obligatoriedad del color amarillo",
            "Fundación de la TLC",
            "Pico de valoración del medallón",
            "Implementación del Congestion Surcharge"
        ],
        "Impacto Económico y Social": [
            "Mejora en fiabilidad y rango operativo frente a modelos eléctricos.",
            "Creación del medallón como permiso transferible y limitado.",
            "Estandarización visual para la seguridad y reconocimiento del pasajero.",
            "Centralización de la supervisión de taxis y limusinas en una sola agencia.",
            "El valor de mercado alcanza los $1.3 millones antes de la crisis de las apps.",
            "Introducción de un recargo fiscal de $2.50 para financiar el transporte masivo."
        ]
    }

    # 2. Convertimos el diccionario a un DataFrame de Pandas
    df_historia = pd.DataFrame(datos_historia)

    df_historia.set_index("Período Histórico", inplace=True)

    # 3. Renderizamos la tabla en Streamlit
    st.table(df_historia)

mostrar_tabla_historica()

