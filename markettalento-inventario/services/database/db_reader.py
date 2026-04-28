"""db_reader.py — Responsabilidad: lectura basica de product_database."""
from .product_db import product_database

def get_product_info(product_name: str) -> dict | None:
    """Devuelve el dict de un producto por nombre, o None si no existe."""
    return product_database.get(product_name)

def get_all_products() -> list[dict]:
    """Devuelve la lista completa de productos."""
    return list(product_database.values())
