from services.database.product_db import product_database


def count_by_status(detected_products: list[dict]) -> dict:
    """Clasifica productos detectados por estado de stock.

    Compara el stock actual de cada producto con su stock_minimo
    registrado en la base de datos. Solo clasifica, no genera
    recomendaciones ni calcula valores económicos.

    Args:
        detected_products: Lista de dicts con las claves:
            - nombre (str): Nombre del producto.
            - cantidad (int): Stock actual detectado.

    Returns:
        Dict con las claves:
            - criticos (list[dict]): Productos con stock == 0.
            - bajos (list[dict]): Productos con stock < stock_minimo.
            - adecuados (list[dict]): Productos con stock >= stock_minimo.
            - resumen (dict): Contadores totales con claves
              total_productos, total_unidades, productos_criticos,
              productos_bajos y productos_adecuados.

    Example:
        >>> productos = [{"nombre": "Leche", "cantidad": 8},
        ... {"nombre": "Pan", "cantidad": 1}]
        >>> result = count_by_status(productos)
        >>> result["resumen"]["productos_bajos"]
        1
    """
    critical, low, adequate = [], [], []

    for item in detected_products:
        info = product_database.get(item["nombre"])
        if not info:
            continue

        stock = item["cantidad"]
        minimo = info.get("stock_minimo", 5)
        entry = {
            "producto": item["nombre"],
            "stock_actual": stock,
            "stock_minimo": minimo,
        }

        if stock == 0:
            critical.append({**entry, "estado": "AGOTADO"})
        elif stock < minimo:
            low.append({**entry, "estado": "BAJO"})
        else:
            adequate.append({**entry, "estado": "ADECUADO"})

    return {
        "criticos": critical,
        "bajos": low,
        "adecuados": adequate,
        "resumen": {
            "total_productos": len(detected_products),
            "total_unidades": sum(p["cantidad"] for p in detected_products),
            "productos_criticos": len(critical),
            "productos_bajos": len(low),
            "productos_adecuados": len(adequate),
        },
    }
