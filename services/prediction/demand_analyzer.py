"""demand_analyzer.py — Analiza el historial de ventas y calcula la demanda diaria."""


def calculate_daily_demand(sales_history: list) -> dict:
    """Calcula la demanda diaria promedio, ajustada y tendencia a partir
    del historial de ventas.

    Usa una media ponderada lineal (más peso a valores recientes) para
    calcular adjusted_daily, lo que da más relevancia a los picos recientes
    que a la media pura.

    Args:
        sales_history: Lista de enteros con las ventas diarias históricas.
            No puede ser vacía ni None.

    Returns:
        Dict con las claves:
            - avg_daily (float): Media aritmética del historial.
            - adjusted_daily (float): Media ponderada lineal (énfasis reciente).
            - trend (str): "CRECIENTE", "DECRECIENTE" o "ESTABLE".

    Raises:
        ValueError: Si sales_history está vacío.
        TypeError: Si sales_history es None.

    Example:
        >>> calculate_daily_demand([3, 4, 5, 3, 4, 6, 5])
        {"avg_daily": 4.29, "adjusted_daily": 4.61, "trend": "ESTABLE"}
        >>> calculate_daily_demand([])
        ValueError
    """
    if sales_history is None:
        raise TypeError("sales_history no puede ser None.")

    if len(sales_history) == 0:
        raise ValueError("sales_history no puede estar vacío.")

    n = len(sales_history)

    # Media aritmética
    avg = sum(sales_history) / n

    # Media ponderada lineal: peso 1 al más antiguo, n al más reciente
    weights     = range(1, n + 1)
    weighted    = sum(v * w for v, w in zip(sales_history, weights))
    adjusted    = weighted / sum(weights)

    # Tendencia: compara demanda ajustada contra media pura
    if adjusted > avg * 1.1:
        trend = "CRECIENTE"
    elif adjusted < avg * 0.9:
        trend = "DECRECIENTE"
    else:
        trend = "ESTABLE"

    return {
        "avg_daily":      round(avg,      2),
        "adjusted_daily": round(adjusted, 2),
        "trend":          trend,
    }