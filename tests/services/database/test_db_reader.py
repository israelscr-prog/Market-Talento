import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from services.database.db_reader import get_product_info, get_all_products


# ── get_product_info ────────────────────────────────────────

def test_get_existing_product_returns_dict():
    result = get_product_info("Leche")
    assert isinstance(result, dict)


def test_get_existing_product_correct_name():
    result = get_product_info("Leche")
    assert result["nombre"] == "Leche"


def test_get_existing_product_has_precio():
    result = get_product_info("Leche")
    assert "precio" in result


def test_get_nonexistent_product_returns_none():
    assert get_product_info("ProductoFantasma") is None


def test_get_empty_string_returns_none():
    assert get_product_info("") is None


def test_get_case_sensitive():
    assert get_product_info("leche") is None
    assert get_product_info("Leche") is not None


# ── get_all_products ────────────────────────────────────────

def test_get_all_returns_list():
    assert isinstance(get_all_products(), list)


def test_get_all_not_empty():
    assert len(get_all_products()) > 0


def test_get_all_returns_25():
    assert len(get_all_products()) == 25


def test_get_all_each_item_is_dict():
    for p in get_all_products():
        assert isinstance(p, dict)