import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from services.vision.scenario_loader import _load_scenarios


# ── estructura general ───────────────────────────────────────

def test_returns_list():
    assert isinstance(_load_scenarios(), list)


def test_not_empty():
    assert len(_load_scenarios()) > 0


def test_has_three_scenarios():
    assert len(_load_scenarios()) == 3


# ── estructura de cada escenario ────────────────────────────

def test_each_scenario_has_descripcion():
    for s in _load_scenarios():
        assert "descripcion" in s, f"Falta 'descripcion' en escenario: {s}"


def test_each_scenario_has_productos():
    for s in _load_scenarios():
        assert "productos" in s, f"Falta 'productos' en escenario: {s}"


def test_each_scenario_productos_is_list():
    for s in _load_scenarios():
        assert isinstance(s["productos"], list)


def test_each_scenario_productos_not_empty():
    for s in _load_scenarios():
        assert len(s["productos"]) > 0


# ── estructura de cada producto dentro del escenario ────────

def test_each_product_has_nombre():
    for s in _load_scenarios():
        for p in s["productos"]:
            assert "nombre" in p


def test_each_product_has_cantidad():
    for s in _load_scenarios():
        for p in s["productos"]:
            assert "cantidad" in p


def test_each_product_has_confianza():
    for s in _load_scenarios():
        for p in s["productos"]:
            assert "confianza" in p


def test_cantidad_is_positive_int():
    for s in _load_scenarios():
        for p in s["productos"]:
            assert isinstance(p["cantidad"], int)
            assert p["cantidad"] >= 0


def test_confianza_between_0_and_1():
    for s in _load_scenarios():
        for p in s["productos"]:
            assert 0.0 <= p["confianza"] <= 1.0


def test_descripcion_is_string():
    for s in _load_scenarios():
        assert isinstance(s["descripcion"], str)
        assert len(s["descripcion"]) > 0