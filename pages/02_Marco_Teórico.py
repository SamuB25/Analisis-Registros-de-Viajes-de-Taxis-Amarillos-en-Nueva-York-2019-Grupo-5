import streamlit as st
import pandas as pd


st.title("Análisis del comportamiento de los pasajeros en horas pico en el sistema de transporte Yellow Cars de Nueva York (Octubre-Diciembre 2019)")

st.header("Marco teórico📖")

st.subheader("Antecedentes📜")

st.write("En la ciudad de Nueva York, el ecosistema del transporte por contrato es una de las redes de movilidad urbana más densas, con mayor regulación y mayor desarrollo tecnológico a nivel global. Los emblemáticos taxis amarillos, cuya identidad ha ido más allá de la simple función de transporte hasta transformarse en un símbolo cultural y un soporte de la economía metropolitana, son el núcleo central de esta red. El año 2019 se destaca como un tiempo de cambio significativo, caracterizado por la convergencia de una crisis financiera en el valor de las licencias, la puesta en marcha de acciones fiscales para reducir el embotellamiento urbano y el fortalecimiento de infraestructuras tecnológicas creadas para competir con las plataformas de transporte a través de aplicaciones.")

st.write("Para entender cómo funcionan los taxis amarillos en 2019, es esencial precisar su naturaleza operativa y jurídica dentro de la Comisión de Taxis y Limusinas de Nueva York (TLC). En la ciudad de Nueva York, solo un taxi amarillo, también denominado ¨medallion taxi¨, está legalmente habilitado para recibir viajes que se soliciten por el método de señal de mano en la calle, sin importar en qué parte de los cinco condados se encuentre. Esta exclusividad es el centro del sistema de medallones, un modelo de licencias que sirve como un instrumento para controlar la oferta del gobierno, concebido en sus inicios con el objetivo de evitar el desorden en el tráfico y garantizar que el sector sea rentable.")

st.write("A fines del siglo XIX, se inició el desarrollo del sistema de taxis en Nueva York con la incorporación de los taxis amarillos a gasolina por parte de Harry Allen en 1907. La ausencia de reglamentación provocó que el mercado se saturara. En la década de 1930, el concejal Lew Haas planteó la Ley Haas, que restringía a 13,595 el número de licencias; este número se mantuvo por un periodo de 60 años, lo que hizo que los medallones adquiriesen un alto valor. El costo de los medallones pasó de $2,500 a más de un millón de dólares entre 1947 y 2013. Uber y Lyft, al tener regulaciones más flexibles, trajeron consigo más de 80 000 autos. Esto hizo que el precio de los medallones disminuyera en un 50% para el año 2018.")

#Creacion de una tabla con la evolución histórica de los taxis en Nueva York
def mostrar_tabla_historica():
    st.subheader("Evolución Histórica de los Taxis en Nueva York⏳")
    
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


st.write("El Taxicab Passenger Enhancement Program (TPEP) sustentaba el funcionamiento de los taxis amarillos en 2019. Este sistema es más que una terminal de pago; es una infraestructura compleja que permite la comunicación en ambas direcciones entre el vehículo y la TLC, además de recopilar datos. El TPEP fue creado con el propósito de actualizar la experiencia del pasajero, incorporando pantallas de información (PIM), procesamiento de tarjetas de crédito y sistemas para que el conductor mande mensajes. En el año 2019, las compañías que dominaban la provisión de estos sistemas eran Creative Mobile Technologies (CMT) y Verifone Inc. Estas empresas no solo suministran el hardware, sino que además funcionan como proveedores de servicios tecnológicos (TSPs); se ocupan de registrar y enviar los registros del viaje para enriquecer el Big Data de la ciudad.")

st.subheader("Plataforma Arro (Creative Mobile Technologies, LLC)🚕📲")

st.write("CMT (Creative Mobile Technologies, LLC), establecida en 2005 por personalidades prominentes de la industria del taxi, tenía como objetivo optimizar la eficiencia operativa sin sobrecargar a los dueños de licencias con elevados gastos. ¨La FREEdom Solution¨, su producto insignia, fusiona los medios de comunicación, la banca y el procesamiento de datos. CMT lanzó Arro en 2015, una aplicación de petición de viajes cuyo propósito es asistir a los taxis amarillos para que puedan competir con Lyft y Uber. Arro se conecta directamente con el hardware TPEP del taxi con el fin de acelerar las solicitudes de viaje. Es importante señalar que Arro se comprometió a no implementar precios dinámicos, conservando las tarifas oficiales del taxímetro en los horarios de mayor afluencia.")

st.subheader("Plataforma Curb (Verifone Inc)🚕📲")

st.write("La historia de Curb está relacionada con el progreso de los pagos electrónicos en el transporte, iniciando con TaxiTronic, empresa creada por Amos Tamam en 1992, la cual creó el Metrometer 21R, el primer taxi que podía manejar tarjetas de crédito. TaxiTronic se fusionó con Verifone en el año 2007, dando lugar a la compañía Verifone Transportation Systems (VTS). Con el objetivo de competir en el mercado de aplicaciones de rideshare, VTS compró Curb en 2015, una aplicación que anteriormente se llamaba Taxi Magic. Curb se separó de Verifone en febrero de 2018 y se constituyó como Curb Mobility, una compañía enfocada en el desarrollo de herramientas innovadoras para el tránsito. Para el año 2019, Curb se había establecido como la plataforma de e-hail más utilizada en Nueva York. Esta ofrece funcionalidades como ¨Pair & Pay¨, que facilita a los usuarios enlazar sus aplicaciones para realizar pagos digitales al parar un taxi, así como la posibilidad de reservar viajes con 24 horas de anticipación.")

st.subheader("Contexto socioeconómico de 2019💰")

st.write("El año 2019 fue un periodo crítico para la industria de los taxis amarillos, marcado por la crisis de deuda de medallones. La mayoría de los dueños, que eran en su mayor parte inmigrantes, tenían deudas medias entre 500,000 y 600,000 dolares por la disminución del valor de mercado de sus bienes. El sector observó una caída constante en el recuento de pasajeros, con menos de 9,000 taxis operativos en contraste con los 13,500 que había hace diez años, a pesar de los esfuerzos regulatorios. La situación se volvió más complicada por la competencia de plataformas como Lyft y Uber, que tenían más de 80,000 conductores y brindaban tiempos de espera más cortos en áreas fuera de Manhattan.")

st.write("Con el fin de contrarrestar esto, los taxis amarillos pusieron en marcha aplicaciones como Arro y Curb, con el objetivo de proporcionar comodidad tecnológica sin renunciar a la profesionalidad y seguridad que ofrecen los conductores autorizados. Como parte de estos esfuerzos, Curb empezó a incorporar opciones de viaje compartido, aunque su impacto fue limitado. En el sector, la estructura de ingresos se regía por un modelo de alquiler en el que los choferes, sin medallón propio, pagaban tarifas por el uso del vehículo y las licencias. Esto suponía una carga considerable al asumir todos los riesgos operativos y tener que trabajar largas jornadas para obtener beneficios.")


st.write("El análisis de los viajes realizados en taxis amarillos de Nueva York durante el año 2019 muestra que la industria se encuentra en una situación crítica. El impacto de la economía digital, combinada con el trasfondo histórico del sistema de medallones, ha forzado una evolución acelerada, que redefine la sostenibilidad financiera a largo plazo.")

st.write("Las variables del diccionario de la base de datos de 2019 ofrecen un retrato exacto de esta lucha, en la que cada información relata la historia de una ciudad que busca equilibrar la sostenibilidad fiscal, la protección de los medios económicos de miles de trabajadores y la innovación. Finalmente, el taxi amarillo de 2019 es un ejemplo de resiliencia operativa, ya que se mantiene como el único servicio que puede reaccionar al ritmo de la calle en tiempo real. Esto es posible gracias a una infraestructura de datos que da la posibilidad a los analistas y reguladores de planificar con exactitud el futuro de la movilidad urbana.")

st.subheader("Uso del diseño OLAP en el análisis de datos📂")

st.write("El procesamiento analítico en línea (OLAP) es una tecnología de computación que permite analizar datos de múltiples bases de datos de forma simultánea. En el contexto del análisis de los viajes en taxis amarillos, OLAP facilita la exploración de grandes volúmenes de datos para identificar patrones y tendencias. Usar este método es esencial en proyectos de ciencia de datos porque permite realizar consultas complejas de manera eficiente, facilitar la visualización de datos multidimensionales y mejorar la toma de decisiones basada en datos. En este análisis, usamos OLAP para analizar variables como el número de pasajeros, la duración del viaje, las zonas más frecuentes de los viajes, etc; lo que ayuda a comprender el comportamiento de los pasajeros durante las horas pico.")
