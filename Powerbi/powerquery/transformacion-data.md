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

### 3. Traducción y Semántica de Campos
Para garantizar una mejor contextualización a un público hispanohablante, se renombraron los campos preservando el contexto técnico del diccionario oficial de la TLC de Nueva York.

#### 🚕 Tabla: REGISTRO_VIAJES
| Nombre Original | Nombre Traducido | Descripción Técnica |
| :--- | :--- | :--- |
| `trip_id` | **id_viaje** | Identificador único del registro. |
| `vendor_id` | **id_proveedor** | Código de la empresa tecnológica (Vendor). |
| `rate_code_id` | **id_tipo_tarifa** | Código de la tarifa final aplicada al viaje. |
| `payment_type_id` | **id_metodo_pago** | Código del método de pago utilizado. |
| `pickup_date` | **fecha_recogida** | Fecha en que se activó el taxímetro. |
| `pickup_time` | **hora_recogida** | Hora exacta de inicio del servicio. |
| `dropoff_date` | **fecha_finalización** | Fecha en que se desactivó el taxímetro. |
| `dropoff_time` | **hora_finalización** | Hora exacta de fin del servicio. |
| `pu_location_id` | **id_zona_origen** | Zona de la TLC donde inició el viaje. |
| `do_location_id` | **id_zona_destino** | Zona de la TLC donde terminó el viaje. |
| `passenger_count` | **cantidad_pasajeros** | Número de personas reportadas en el vehículo. |
| `trip_distance` | **distancia_viajes** | Recorrido en millas reportado por el taxímetro. |

#### 💰 Tabla: FINANZAS_VIAJES
| Nombre Original | Nombre Traducido | Descripción Técnica |
| :--- | :--- | :--- |
| `fare_amount` | **importe_tarifa** | Costo calculado por tiempo y distancia. |
| `extra` | **cargos_adicionales** | Recargos por hora pico o tarifas nocturnas. |
| `mta_tax` | **impuesto_mta** | Impuesto fijo de la Autoridad de Transporte ($0.50). |
| `tip_amount` | **monto_propina** | Propina registrada (automático en pagos con tarjeta). |
| `tolls_amount` | **monto_peajes** | Suma total de peajes pagados durante el trayecto. |
| `improvement_surcharge`| **recargo_mejora** | Cargo de $0.30 destinado a infraestructura. |
| `total_amount` | **monto_total** | Suma total cobrada (no incluye propinas en efectivo). |
| `store_and_fwd_flag` | **indicador_almacenamiento_envio** | Indica si el dato se guardó en memoria local antes de enviarse. |

#### 📍 Tabla: LOCALIZACIÓN_VIAJE
| Nombre Original | Nombre Traducido | Descripción Técnica |
| :--- | :--- | :--- |
| `location_id` | **id_ubicación** | Código único de la zona geográfica. |
| `borough` | **distrito** | Condado de NY (Manhattan, Brooklyn, Queens, etc.). |
| `zone` | **zona** | Nombre específico del área o vecindario. |
| `service_zone` | **zona_servicio** | Categorización de la zona según servicio de taxis. |

#### 📂 Otras Entidades
* **PLATAFORMAS_TPEP**: Se tradujo `plataforma` para identificar proveedores (Creative Mobile / VeriFone).
* **METODO_PAGO**: Se tradujo `descripcion` para identificar (Tarjeta, Efectivo, Sin Cargo, etc.).
* **TARIFAS**: Se tradujo `descripcion` para tipos de tarifa (Estándar, JFK, Newark, Negociada).

### 4. Optimización de Precisión: FINANZAS_VIAJE
Para asegurar la integridad en grandes sumas de dinero (procesamiento de más de 20M de registros), se cambió el tipo de dato de **Número decimal** a **Número decimal fijo ($)** en los siguientes campos:

* `importe_tarifa`, `cargos_adicionales`, `impuesto_mta`, `monto_propina`, `monto_peajes`, `recargo_mejora`, `monto_total`.

**Beneficios Técnicos:**
1. **Precisión:** Evita errores de redondeo en cálculos de sumas masivas.
2. **Rendimiento:** Carga más eficiente en el motor de Power BI.
3. **Visualización:** Formato de moneda automático y limpio en los objetos visuales.

### 📊 Resultado del Proceso
La base de datos resultante ofrece una estructura **saneada, optimizada y fácil de interpretar** para el análisis estadístico, eliminando barreras de idioma y asegurando precisión en los KPIs financieros.