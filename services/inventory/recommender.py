def generate_recommendations(products_needing_attention: list[dict]) -> list[dict]:
    """Genera recomendaciones de reposición para productos con stock insuficiente.

    Procesa únicamente productos en estado crítico o bajo. No clasifica
    ni calcula valores económicos — solo genera el mensaje y la prioridad
    de reposición para cada producto recibido.

    Args:
        products_needing_attention: Lista de dicts con las claves:
            - producto (str): Nombre del producto.
            - stock_actual (int): Stock actual detectado.
            - stock_minimo (int): Stock mínimo requerido.

    Returns:
        Lista de dicts, uno por producto, con las claves:
            - producto (str): Nombre del producto.
            - recomendacion (str): Mensaje de acción a tomar.
            - prioridad (str): "ALTA" si stock == 0, "MEDIA" si stock < minimo.
              Lista vacía si no hay productos que atender.

    Example:
        >>> productos = [
        ...     {"producto": "Leche", "stock_actual": 0, "stock_minimo": 5},
        ...     {"producto": "Pan", "stock_actual": 3, "stock_minimo": 10},
        ... ]
        >>> generate_recommendations(productos)
        [
            {
                "producto": "Leche",
                "recomendacion": "Reponer urgentemente Leche. Stock agotado.",
                "prioridad": "ALTA",
            },
            {
                "producto": "Pan",
                "recomendacion": "Reponer 17 unidades de Pan. Stock bajo.",
                "prioridad": "MEDIA",
            },
        ]
        >>> generate_recommendations([])
        []
    """
    recs = []

    for p in products_needing_attention:
        nombre = p["producto"]
        stock = p["stock_actual"]
        minimo = p.get("stock_minimo", 5)

        if stock == 0:
            mensaje = f"Reponer urgentemente {nombre}. Stock agotado."
            prioridad = "ALTA"
        else:
            unidades = minimo * 2 - stock
            mensaje = f"Reponer {unidades} unidades de {nombre}. Stock bajo."
            prioridad = "MEDIA"

        recs.append(
            {
                "producto": nombre,
                "recomendacion": mensaje,
                "prioridad": prioridad,
            }
        )

    return recs
