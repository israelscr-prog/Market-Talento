def calculate_daily_demand(sales_history: list[int]) -> dict:
    """Calcula la demanda media diaria y la ajustada por tendencia reciente.

    Analiza el historial de ventas para obtener la demanda promedio
    global y una demanda ajustada basada en los últimos 5 días.
    Solo realiza análisis estadístico, sin clasificar ni recomendar.

    Args:
        sales_history: Lista de enteros con las ventas diarias históricas.
            Debe contener al menos un elemento.

    Returns:
        Dict con las claves:
            - avg_daily (float): Media diaria global redondeada a 2 decimales.
            - adjusted_daily (float): Media ajustada por tendencia reciente,
              redondeada a 2 decimales.

    Raises:
        ValueError: Si sales_history está vacío.

    Example:
        >>> calculate_daily_demand([4, 4, 4, 4, 4])
        {"avg_daily": 4.0, "adjusted_daily": 4.0}
        >>> calculate_daily_demand([1, 2, 3, 4, 8, 8, 8, 8, 8])
        {"avg_daily": 5.0, "adjusted_daily": 8.0}
        >>> calculate_daily_demand([])
        ValueError: sales_history no puede estar vacío.
    """
    if not sales_history:
        raise ValueError("sales_history no puede estar vacío.")

    avg = sum(sales_history) / len(sales_history)

    if len(sales_history) >= 5:
        recent   = sum(sales_history[-5:]) / 5
        adjusted = avg * (recent / avg if avg > 0 else 1.0)
    else:
        adjusted = avg

    return {
        "avg_daily":      round(avg, 2),
        "adjusted_daily": round(adjusted, 2),
    }