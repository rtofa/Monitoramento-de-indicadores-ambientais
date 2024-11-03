def emitir_alerta(aqi, cidade):

    """Emitir alerta se o AQI ultrapassar certos limites."""

    if aqi > 100: 
        print(f"ALERTA: Qualidade do ar na cidade {cidade} está crítica! AQI: {aqi}")