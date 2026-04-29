import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from services.database.product_db import product_database


def test_database_not_empty():
    assert len(product_database) > 0


def test_database_has_25_products():
    assert len(product_database) == 25


def test_all_products_have_required_fields():
    required = {"id", "nombre", "categoria", "precio",
                "unidad", "stock_minimo", "stock_maximo",
                "tiempo_reposicion", "historial_ventas"}
    for nombre, p in product_database.items():
        assert required.issubset(p.keys()), f"Faltan campos en {nombre}"


def test_all_prices_are_positive():
    for nombre, p in product_database.items():
        assert p["precio"] > 0, f"Precio inválido en {nombre}"


def test_all_stock_minimo_positive():
    for nombre, p in product_database.items():
        assert p["stock_minimo"] > 0, f"stock_minimo inválido en {nombre}"


def test_stock_minimo_menor_que_maximo():
    for nombre, p in product_database.items():
        assert p["stock_minimo"] < p["stock_maximo"], f"stock_minimo >= stock_maximo en {nombre}"


def test_historial_ventas_is_list():
    for nombre, p in product_database.items():
        assert isinstance(p["historial_ventas"], list), f"historial_ventas no es lista en {nombre}"


def test_historial_ventas_not_empty():
    for nombre, p in product_database.items():
        assert len(p["historial_ventas"]) > 0, f"historial_ventas vacío en {nombre}"


def test_all_ids_are_unique():
    ids = [p["id"] for p in product_database.values()]
    assert len(ids) == len(set(ids)), "Hay IDs duplicados"