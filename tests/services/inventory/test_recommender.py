import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from services.inventory.recommender import generate_recommendations

# ── fixtures ────────────────────────────────────────────────

CRITICO = {"producto": "Leche", "stock_actual": 0,  "stock_minimo": 5}
BAJO    = {"producto": "Pan",   "stock_actual": 3,  "stock_minimo": 10}
NORMAL  = {"producto": "Agua",  "stock_actual": 20, "stock_minimo": 15}

# ── lista vacía ──────────────────────────────────────────────

def test_empty_input_returns_empty():
    assert generate_recommendations([]) == []

def test_empty_input_returns_list():
    assert isinstance(generate_recommendations([]), list)

# ── estado crítico (stock == 0) ──────────────────────────────

def test_critico_prioridad_alta():
    recs = generate_recommendations([CRITICO])
    assert recs[0]["prioridad"] == "ALTA"

def test_critico_mensaje_contiene_urgente():
    recs = generate_recommendations([CRITICO])
    assert "urgentemente" in recs[0]["recomendacion"].lower()

def test_critico_tiene_producto():
    recs = generate_recommendations([CRITICO])
    assert recs[0]["producto"] == "Leche"

# ── estado bajo (0 < stock < minimo) ────────────────────────

def test_bajo_prioridad_media():
    recs = generate_recommendations([BAJO])
    assert recs[0]["prioridad"] == "MEDIA"

def test_bajo_mensaje_contiene_reponer():
    recs = generate_recommendations([BAJO])
    assert "reponer" in recs[0]["recomendacion"].lower()

def test_bajo_tiene_producto():
    recs = generate_recommendations([BAJO])
    assert recs[0]["producto"] == "Pan"

# ── estructura del retorno ───────────────────────────────────

def test_each_rec_has_required_keys():
    recs = generate_recommendations([CRITICO, BAJO])
    for r in recs:
        assert "producto" in r
        assert "recomendacion" in r
        assert "prioridad" in r

def test_returns_one_rec_per_product():
    recs = generate_recommendations([CRITICO, BAJO])
    assert len(recs) == 2

# ── múltiples productos ──────────────────────────────────────

def test_multiple_products_correct_priorities():
    recs = generate_recommendations([CRITICO, BAJO])
    prioridades = [r["prioridad"] for r in recs]
    assert "ALTA" in prioridades
    assert "MEDIA" in prioridades