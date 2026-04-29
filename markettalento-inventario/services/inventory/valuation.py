from services.database.product_db import product_database


def calculate_inventory_value(detected_products: list[dict]) -> float:
    """Calcula el valor económico total del inventario detectado.

    Multiplica precio × cantidad para cada producto detectado
    que exista en la base de datos. Solo calcula valor económico,
    no clasifica ni genera recomendaciones.

    Args:
        detected_products: Lista de dicts con las claves:
            - nombre (str): Nombre del producto.
            - cantidad (int): Stock actual detectado.

    Returns:
        Valor total en euros redondeado a 2 decimales.
        Devuelve 0.0 si la lista está vacía o ningún
        producto existe en la base de datos.

    Example:
        >>> calculate_inventory_value([{"nombre": "Leche", "cantidad": 5}])
        6.0
        >>> calculate_inventory_value([])
        0.0
        >>> calculate_inventory_value([{"nombre": "XYZ", "cantidad": 10}])
        0.0
    """
    total = 0.0

    for item in detected_products:
        info = product_database.get(item["nombre"])
        if info and "precio" in info:
            total += item["cantidad"] * info["precio"]

    return round(total, 2)