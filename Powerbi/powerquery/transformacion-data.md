# 🛠️ Registro de Transformaciones en Power Query

A continuación se detallan los pasos aplicados para la limpieza y optimización de las tablas **REGISTRO_VIAJES** y **FINANZAS_VIAJE**.


### 1. Limpieza y Filtrado de Datos
| Paso M | Acción | Descripción |
| :--- | :--- | :--- |
| **#"Filas filtradas"** | `Table.SelectRows` | Se eliminan registros fuera del rango de **Octubre, Noviembre y Diciembre 2019**. |
| **#"Valor absoluto"** | `Table.TransformColumns` | Cambio de **valores negativos a positivos** en columnas de totales, propinas y demás cargos para corregir errores de registro. |
