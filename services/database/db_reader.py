"""db_reader.py — Responsabilidad: lectura basica de product_database."""
from typing import Optional

from .product_db import product_database


def get_product_info(product_name: str) -> Optional[dict]:
    """Devuelve el diccionario completo de un producto dado su nombre.

    Args:
        product_name: Nombre exacto del producto (ej. "Leche").

    Returns:
        Dict con todos los datos del producto, o None si no existe.

    Example:
        >>> get_product_info("Leche")
        {"id": "PROD001", "nombre": "Leche", ...}
        >>> get_product_info("Fantasma")
        None
    """
    return product_database.get(product_name)


def get_all_products() -> list:
    """Devuelve la lista completa de todos los productos de la base de datos.

    Returns:
        Lista de dicts, uno por cada producto registrado.

    Example:
        >>> productos = get_all_products()
        >>> len(productos)
        25
    """
    return list(product_database.values())
