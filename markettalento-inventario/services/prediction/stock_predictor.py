from .demand_analyzer import calculate_daily_demand


def predict_stock_outage(
    sales_history: list[int],
    current_stock: int,
    product_info: dict | None = None,
) -> dict:
    """Predice cuántos días quedan hasta que se agote el stock de un producto.

    Delega el análisis de demanda en calculate_daily_demand y usa
    el resultado para estimar los días restantes. Maneja los casos
    de stock agotado e historial vacío sin propagar excepciones.

    Args:
        sales_history: Lista de enteros con las ventas diarias históricas.
        current_stock: Stock actual del producto. 0 o negativo
            devuelve estado AGOTADO directamente.
        product_info: Dict opcional con metadatos del producto.
            No se usa en el cálculo actual, reservado para Fase 2.

    Returns:
        Dict con las claves:
            - dias_hasta_agotarse (float): Días estimados hasta agotamiento.
              0 si el stock ya está agotado.
            - estado (str): "AGOTADO", "SIN HISTORIAL", "CRITICO",
              "BAJO", "MODERADO" o "ADECUADO".
            - cantidad_recomendada (int): Unidades sugeridas para reponer.
            - consumo_promedio_diario (float): Demanda ajustada utilizada.

    Raises:
        No propaga excepciones. Los casos límite devuelven
        un dict con estado descriptivo.

    Example:
        >>> predict_stock_outage([3, 4, 5, 3, 4], 20)
        {"dias_hasta_agotarse": 5.2, "estado": "BAJO", ...}
        >>> predict_stock_outage([], 10)
        {"dias_hasta_agotarse": 0, "estado": "SIN HISTORIAL", ...}
        >>> predict_stock_outage([3, 4, 5], 0)
        {"dias_hasta_agotarse": 0, "estado": "AGOTADO", ...}
    """
    if current_stock <= 0:
        return {
            "dias_hasta_agotarse":      0,
            "estado":                   "AGOTADO",
            "cantidad_recomendada":     10,
            "consumo_promedio_diario":  0.0,
        }

    try:
        demand   = calculate_daily_demand(sales_history)
        adjusted = demand["adjusted_daily"]
        avg      = demand["avg_daily"]
    except ValueError:
        return {
            "dias_hasta_agotarse":      0,
            "estado":                   "SIN HISTORIAL",
            "cantidad_recomendada":     10,
            "consumo_promedio_diario":  0.0,
        }

    days = max(0, min(90, round(current_stock / adjusted, 1))) if adjusted > 0 else 999

    if days <= 2:    estado = "CRITICO"
    elif days <= 5:  estado = "BAJO"
    elif days <= 10: estado = "MODERADO"
    else:            estado = "ADECUADO"

    return {
        "dias_hasta_agotarse":     days,
        "estado":                  estado,
        "cantidad_recomendada":    round(avg * 10),
        "consumo_promedio_diario": adjusted,
    }