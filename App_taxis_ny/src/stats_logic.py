import pandas as pd

# 1. Paleta de colores oficial
BICKLE_PALETTE = {
    "taxi_yellow": "#F2BC1B",
    "asphalt_night": "#121212",
    "secondary_bg": "#1F1F1F",
    "steel_gray": "#8C8C8C",
    "vapor_white": "#F2F2F2",
    "neon_red": "#D90404",
    "m65_green": "#4B5320"
}

def get_accent_color(tipo_horario):
    """Retorna Rojo si es Hora Pico, sino Amarillo."""
    return BICKLE_PALETTE["neon_red"] if tipo_horario == "Hora Pico" else BICKLE_PALETTE["taxi_yellow"]

def format_kpi(value, is_money=False):
    """Formatea números para los KPIs de la app."""
    if value is None: return "0"
    if is_money: return f"$ {value:,.2f}"
    return f"{int(value):,}" if value > 100 else f"{value:.1f}"

def build_sql_filter(tipo_horario="Vista General", mes="Todos"):
    """Genera la cláusula WHERE para las consultas SQL."""
    condiciones = ["1=1"]
    if tipo_horario == "Hora Pico":
        condiciones.append("CAST(EXTRACT(ISODOW FROM TRY_CAST(pickup_date AS DATE)) AS INT) BETWEEN 1 AND 5")
        condiciones.append("pickup_time >= '16:00:00'")
        condiciones.append("pickup_time <= '20:00:00'")
    elif tipo_horario == "Hora No Pico":
        condiciones.append("(CAST(EXTRACT(ISODOW FROM TRY_CAST(pickup_date AS DATE)) AS INT) IN (6, 7) OR pickup_time < '16:00:00' OR pickup_time > '20:00:00')")

    meses_map = {"Octubre": 10, "Noviembre": 11, "Diciembre": 12}
    if mes in meses_map:
        condiciones.append(f"EXTRACT(MONTH FROM TRY_CAST(pickup_date AS DATE)) = {meses_map[mes]}")
    
    return " AND ".join(condiciones)