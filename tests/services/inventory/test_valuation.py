import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from services.inventory.valuation import calculate_inventory_value

# ── lista vacía ──────────────────────────────────────────────

def test_empty_list_returns_zero():
    assert calculate_inventory_value([]) == 0.0

def test_empty_list_returns_float():
    assert isinstance(calculate_inventory_value([]), float)

# ── producto existente ───────────────────────────────────────

def test_single_product_returns_positive():
    result = calculate_inventory_value([{"nombre": "Leche", "cantidad": 5}])
    assert result > 0

def test_single_product_correct_value():
    # Leche: 1.20€ x 5 = 6.00€
    result = calculate_inventory_value([{"nombre": "Leche", "cantidad": 5}])
    assert result == 6.0

def test_returns_float():
    result = calculate_inventory_value([{"nombre": "Leche", "cantidad": 5}])
    assert isinstance(result, float)

def test_rounded_to_2_decimals():
    result = calculate_inventory_value([{"nombre": "Leche", "cantidad": 3}])
    assert result == round(result, 2)

# ── múltiples productos ──────────────────────────────────────

def test_multiple_products_sums_correctly():
    products = [
        {"nombre": "Leche",  "cantidad": 5},
        {"nombre": "Huevos", "cantidad": 2},
    ]
    # Leche: 1.20x5=6.00, Huevos: 2.50x2=5.00 → 11.00
    assert calculate_inventory_value(products) == 11.0

def test_cantidad_cero_no_suma():
    result = calculate_inventory_value([{"nombre": "Leche", "cantidad": 0}])
    assert result == 0.0

# ── producto no encontrado en BD ─────────────────────────────

def test_unknown_product_returns_zero():
    assert calculate_inventory_value([{"nombre": "ProductoXYZ", "cantidad": 10}]) == 0.0

def test_unknown_product_ignored_in_total():
    products = [
        {"nombre": "Leche",       "cantidad": 5},
        {"nombre": "ProductoXYZ", "cantidad": 10},
    ]
    solo_leche = calculate_inventory_value([{"nombre": "Leche", "cantidad": 5}])
    assert calculate_inventory_value(products) == solo_leche