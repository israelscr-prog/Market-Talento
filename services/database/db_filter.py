"""db_filter.py — Responsabilidad: filtrado y consultas derivadas."""
from .product_db import product_database
from .db_reader import get_product_info


def get_by_category(category: str) -> list:
    """Devuelve todos los productos que pertenecen a una categoría dada.

    Args:
        category: Nombre exacto de la categoría (ej. "Bebidas").

    Returns:
        Lista de dicts con los productos de esa categoría.
        Lista vacía si la categoría no existe.

    Example:
        >>> get_by_category("Bebidas")
        [{"nombre": "Agua", ...}, {"nombre": "Cafe", ...}]
        >>> get_by_category("CategoriaXYZ")
        []
    """
    return [p for p in product_database.values() if p["categoria"] == category]


def get_sales_history(product_name: str, days: int = 20) -> list:
    """Devuelve el historial de ventas de un producto para los últimos N días.

    Args:
        product_name: Nombre exacto del producto (ej. "Leche").
        days: Número de días a recuperar. 0 devuelve todo el historial.
            Por defecto 20.

    Returns:
        Lista de enteros con las ventas diarias.
        Lista vacía si el producto no existe.

    Example:
        >>> get_sales_history("Leche", 5)
        [4, 6, 3, 5, 4]
        >>> get_sales_history("Fantasma")
        []
    """
    product = get_product_info(product_name)
    if not product:
        return []

    history = product["historial_ventas"]
    return history[-days:] if days > 0 else history
