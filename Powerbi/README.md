### 📊 Dashboard Interactivo (Versión Web)
Pueden visualizar el análisis de los 20 millones de viajes de Taxis NY aquí:
[👉 Ver Dashboard en Vivo](https://app.powerbi.com/view?r=eyJrIjoiNDRiYjIwYzktMjJkZC00NzNkLWI0OTItYTgyNzg3NGVkM2I2IiwidCI6IjRjODE4Zjc5LWFiODQtNDU1Mi05YjdjLTJmZTcxNWIwZDBkNSIsImMiOjR9)

# Analisis-Registros-de-Viajes-de-Taxis-Amarillos-en-Nueva-York-2019-Grupo-5/


Análisis descriptivo de la demanda de taxis en Nueva York durante el utimo trimestre del 2019 (Octubre-Diciembre) mediante un dashboard interactivo construido en **Power BI Desktop**, usando más de **20 millones de registros** 

---

## Descripción del Proyecto
Este proyecyo lleva como objetivo Analizar el comportamiento de los pasajeros de los Yellow Taxis de Nueva York durante el ultimo trimestre de 2019, octubre-diciembre, específicamente en los intervalos de mayor afluencia de usuarios, para comprender la influencia de la variable "hora" en el resto de los indicadores con la finalidad de construir perfiles comparativos entre pasajeros de "Hora Pico" y "Hora No Pico".

---

## Estructura del Repositorio

```
Analisis-Registros-de-Viajes-de-Taxis-Amarillos-en-Nueva-York-2019-Grupo-5/

│
│
├── powerquery/
│   └── tranformacion-data.md    # tripdata_clean
│
├── dax/
│   └── dax-resumen.md         
│
├── screenshots/                          # Capturas del dashboard
│
└── README.md                             # Este archivo
```

---

## Modelo de Datos

El modelo contiene las siguientes tablas principales:

| Tabla | Descripción |
|---|---|
| `registro_viajes` | Tabla de hechos: 20M+ registros de viajes (hora, zona, duración, distancia) |
| `finanzas_viaje` | Datos financieros por viaje: tarifa, propina, monto total |
| `flujos_origen_destino` | Combinaciones de zona de origen y destino |
| `localizacion_viaje` | Coordenadas geográficas de cada viaje |
| `coordenadas` | Tabla de referencia geográfica por zona |
| `metodo_pago` | Tipos de pago disponibles |
| `plataformas_tpep` | Proveedores del sistema (VeriFone Inc., Creative Mobile) |
| `tarifas` | Tipos de tarifa aplicables |
| `_medidas` | Tabla auxiliar que centraliza todas las medidas DAX |

---

## Páginas del Dashboard

### Página 1 — TAXI DRIVER
Portada y presentación.

### Página 2 — "The City's Pulse"
Análisis de distribución temporal y geográfica de la demanda. Incluye:
- **KPIs:** 20,634,593 viajes totales | $400,209,154.97 ingresos | 32,682,855 pasajeros | $19.40 ingreso promedio
- **Matriz de calor:** Distribución de viajes por hora y día de la semana
- **Gráfico de barras:** Viajes por distrito de origen (Manhattan lidera con 18.4M)
- **Línea de tiempo:** Total de viajes por mes y semana (octubre–noviembre)
- **Treemap:** Viajes totales por plataforma TPEP (VeriFone: 13.6M | Creative Mobile: 6.9M)
- **Segmentadores:** Tipo de tarifa, método de pago, categoría de día, número de semana

### Página 3 — "Peak vs. Off-Peak"
Análisis de rendimiento económico y velocidad según franja horaria. Incluye:
- **KPIs:** Duración promedio 15.01 min | Distancia promedio 2.97 mi | Ingreso/min $10.82 | Velocidad 10.82 MPH | CV Duración 0.95
- **Mapa de calor por zonas:** Cantidad de viajes por zona (Manhattan, Queens, Brooklyn)
- **Mapa 3D:** Total de viajes por distrito con escala visual
- **Gráfico combinado:** Impacto de congestión en rendimiento económico por franja horaria (Ingreso/Minuto vs Velocidad MPH)
- **Filtros:** Segmento horario y categoría de día (Día Laboral / Fin de Semana)

---

## Medidas DAX — Resumen

Todas las medidas se centralizan en la tabla `_medidas`:

| Medida | Fórmula base |
|---|---|
| `Total Viajes` | `CALCULATE(COUNTROWS(...), monto_total > 0)` |
| `Ingresos Totales` | `CALCULATE(SUM(monto_total), monto_total > 0)` |
| `Ingreso_Promedio` | `DIVIDE([Ingresos Totales], [Total Viajes])` |
| `Ingreso_Minuto` | `SUMX(... DIVIDE(Ingreso, Duracion))` |
| `Ingreso por Milla` | `DIVIDE([Ingreso_Promedio], [Distancia Promedio (Millas)])` |
| `Velocidad_MPH` | `AVERAGEX(... distancia / (minutos / 60))` |
| `Duracion Promedio (Min)` | `AVERAGE(Duracion Exacta (min))` |
| `Desviacion Duracion` | `STDEV.S(Duracion Exacta (min))` |
| `Varianza Duracion` | `VAR.S(Duracion Exacta (min))` |
| `CV Duracion` | `[Desviacion Duracion] / [Duracion Promedio (Min)]` |
| `Total Pasajeros` | `SUM(cantidad_pasajeros)` |
| `Porcentaje_Propina` | `DIVIDE(SUM(propina), SUM(tarifa_base))` |
| `Distancia Promedio (Millas)` | `AVERAGE(distancia_viaje)` |

Ver documentación completa en [`dax/dax-resumen.md`](dax/dax-resumen.md).

---

## Columnas Calculadas Principales

| Columna | Tabla | Descripción |
|---|---|---|
| `Duracion Exacta (min)` | `registro_viajes` | Duración en minutos calculada con `DATEDIFF(..., SECOND) / 60` |
| `Dia_Nombre` | `registro_viajes` | Nombre del día en español: `FORMAT(..., "dddd", "es-ES")` |
| `N_Hora_salida` | `registro_viajes` | Hora numérica de inicio: `HOUR(hora_recogida)` |
| `Segmento_Horario` | `registro_viajes` | Franja de 4 horas usando `SWITCH(TRUE(), ...)` |
| `Categoria_Dia` | `registro_viajes` | "Día Laboral" o "Fin de Semana" |

---

## Métricas Clave del Dataset Completo

| Métrica | Valor |
|---|---|
| Total de viajes | 20,634,593 |
| Ingresos totales | $400,209,154.97 |
| Total de pasajeros | 32,682,855 |
| Ingreso promedio por viaje | $19.40 |
| Duración promedio | 15.01 min |
| Distancia promedio | 2.97 millas |
| Velocidad promedio | 10.82 MPH |
| CV de duración | 0.95 |

---

## Hallazgos Principales

- **Manhattan** concentra la mayor demanda con 18.4 millones de viajes, seguido de Queens (1.05M) y Brooklyn (0.80M).
- **VeriFone Inc.** es la plataforma dominante con ~66% de los viajes totales.
- La franja horaria **08:00–12:00** y **16:00–20:00** concentran la mayor cantidad de viajes.
- El **ingreso por minuto** es más alto en horas valle (menor tráfico), reflejando el impacto de la congestión.
- El coeficiente de variación de duración (**CV = 0.95**) indica alta variabilidad: los tiempos de viaje son muy dispersos.


---

## Recomendaciones Futuras

- Incorporar coordenadas geográficas exactas por zona para mejorar precisión en mapas.
- Agregar análisis por tipo de tarifa y método de pago cruzado con zona.
- Automatizar la carga mensual de nuevos datos desde la fuente oficial de NYC TLC.
- Explorar visualizaciones avanzadas como debed para flujos de rutas.
- Implementar análisis predictivo de demanda por hora y zona.

---

## Estado del Proyecto

✅ Finalizado  
📅 Última modificación: 16/04/2026  
👤 Autor: Andres MOrales
