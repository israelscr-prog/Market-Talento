import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from services.database.db_filter import get_by_category, get_sales_history


# ── get_by_category ─────────────────────────────────────────

def test_bebidas_returns_list():
    assert isinstance(get_by_category("Bebidas"), list)


def test_bebidas_not_empty():
    assert len(get_by_category("Bebidas")) >= 1


def test_bebidas_all_correct_category():
    for p in get_by_category("Bebidas"):
        assert p["categoria"] == "Bebidas"


def test_lacteos_has_multiple_products():
    assert len(get_by_category("Lacteos")) >= 2


def test_unknown_category_returns_empty():
    assert get_by_category("CategoriaInexistente") == []


def test_empty_string_category_returns_empty():
    assert get_by_category("") == []


# ── get_sales_history ────────────────────────────────────────

def test_history_existing_product_returns_list():
    assert isinstance(get_sales_history("Leche"), list)


def test_history_default_20_days():
    result = get_sales_history("Leche")
    assert len(result) <= 20


def test_history_custom_days():
    result = get_sales_history("Leche", 5)
    assert len(result) == 5


def test_history_all_days():
    result = get_sales_history("Leche", 0)
    assert len(result) == len(get_sales_history("Leche", 999))


def test_history_values_are_integers():
    for v in get_sales_history("Leche"):
        assert isinstance(v, int)


def test_history_nonexistent_product_returns_empty():
    assert get_sales_history("ProductoFantasma") == []


def test_history_empty_string_returns_empty():
    assert get_sales_history("") == []