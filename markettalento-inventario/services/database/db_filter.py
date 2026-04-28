"""db_filter.py — Responsabilidad: filtrado y consultas derivadas."""
from .product_db import product_database
from .db_reader import get_product_info

def get_by_category(category: str) -> list[dict]:
    """Devuelve todos los productos de una categoria dada."""
    return [p for p in product_database.values() if p["categoria"] == category]

def get_sales_history(product_name: str, days: int = 20) -> list[int]:
    """Devuelve el historial de ventas de un producto (ultimos N dias)."""
    product = get_product_info(product_name)
    if not product:
        return []
    h = product["historial_ventas"]
    return h[-days:] if days > 0 else h
