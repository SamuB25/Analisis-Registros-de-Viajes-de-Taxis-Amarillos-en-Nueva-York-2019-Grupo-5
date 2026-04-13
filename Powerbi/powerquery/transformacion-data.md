# 🛠️ Registro de Transformaciones en Power Query

A continuación se detallan los pasos aplicados para la limpieza y optimización de las tablas **REGISTRO_VIAJES** y **FINANZAS_VIAJE**.


### 1. Limpieza y Filtrado de Datos
| Paso M | Acción | Descripción |
| :--- | :--- | :--- |
| **#"Filas filtradas"** | `Table.SelectRows` | Se eliminan registros fuera del rango de **Octubre, Noviembre y Diciembre 2019**. |
| **#"Valor absoluto"** | `Table.TransformColumns` | Cambio de **valores negativos a positivos** en columnas de totales, propinas y demás cargos para corregir errores de registro. |

### 2. Reestructuración de Tabla: REGISTRO_VIAJES
Se corrigieron los tipos de datos para permitir análisis de series de tiempo y jerarquías temporales exactas.

| Campo | Tipo Original | Tipo Nuevo | Motivo |
| :--- | :--- | :--- | :--- |
| **PICKUP_DATE** | Texto | **Fecha** | Permitir segmentación por Mes y Día del viaje. |
| **PICKUP_TIME** | Texto | **Hora** | Análisis de demanda en horas pico. |
| **DROPOFF_DATE** | Texto | **Fecha** | Consistencia en la duración de los trayectos. |
| **DROPOFF_TIME** | Texto | **Hora** | Precisión en el registro de tiempo de llegada. |
