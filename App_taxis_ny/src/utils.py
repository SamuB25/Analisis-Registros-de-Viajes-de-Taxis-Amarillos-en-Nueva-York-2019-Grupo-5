
import pandas as pd

# 1. Diccionario de la paleta de colores "Bickle Palette"
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
    """
    Retorna Rojo Neón si es Hora Pico, de lo contrario Taxi Yellow.
    """
    return BICKLE_PALETTE["neon_red"] if tipo_horario == "Hora Pico" else BICKLE_PALETTE["taxi_yellow"]

def build_sql_filter(tipo_horario="Vista General", mes="Todos"):
    """
    Traduce los filtros del Sidebar en cláusulas WHERE para DuckDB.
    Hora Pico NY: Lunes a Viernes (1 a 5), de 16:00 a 20:00.
    """
    condiciones = ["1=1"] # Base para anidar filtros

    # Filtro de Universo (Hora Pico vs No Pico)
    if tipo_horario == "Hora Pico":
        # ISODOW 1 = Lunes, 7 = Domingo. 
        condiciones.append("CAST(EXTRACT(ISODOW FROM TRY_CAST(pickup_date AS DATE)) AS INT) BETWEEN 1 AND 5")
        condiciones.append("pickup_time >= '16:00:00'")
        condiciones.append("pickup_time <= '20:00:00'")
    elif tipo_horario == "Hora No Pico":
        condiciones.append("""
            (CAST(EXTRACT(ISODOW FROM TRY_CAST(pickup_date AS DATE)) AS INT) IN (6, 7)
            OR pickup_time < '16:00:00'
            OR pickup_time > '20:00:00')
        """)

    # Filtro de Mes
    meses_map = {"Octubre": 10, "Noviembre": 11, "Diciembre": 12}
    if mes in meses_map:
        condiciones.append(f"EXTRACT(MONTH FROM TRY_CAST(pickup_date AS DATE)) = {meses_map[mes]}")

    return " AND ".join(condiciones)

def format_kpi(value, is_currency=False):
    """Formatea métricas para las Cards superiores."""
    if pd.isna(value): return "0"
    if is_currency:
        return f"${value:,.2f}"
    return f"{value:,.1f}" if isinstance(value, float) else f"{value:,}"