"""test_full_pipeline.py — Integración end-to-end del pipeline completo.

Cadena: detect_products → predict_stock_outage → generate_recommendations
Verifica que la cadena no lanza excepciones y que los datos fluyen
correctamente entre cada módulo.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

import pytest
from unittest.mock import patch

from services.vision.detector          import detect_products
from services.prediction.stock_predictor import predict_stock_outage
from services.inventory.recommender    import generate_recommendations

# ── módulo a parchear ────────────────────────────────────────

DEMAND_MODULE = "services.prediction.stock_predictor.calculate_daily_demand"

# ── escenarios simulados de detección ────────────────────────

ESCENARIO_NORMAL = {
    "descripcion": "Estante con productos variados",
    "productos": [
        {"nombre": "Leche",  "cantidad": 20},
        {"nombre": "Huevos", "cantidad": 8},
        {"nombre": "Pan",    "cantidad": 3},
    ],
}

ESCENARIO_CRITICO = {
    "descripcion": "Estante casi vacío",
    "productos": [
        {"nombre": "Leche",  "cantidad": 0},
        {"nombre": "Pan",    "cantidad": 1},
    ],
}

ESCENARIO_UN_PRODUCTO = {
    "descripcion": "Estante con un producto",
    "productos": [
        {"nombre": "Agua", "cantidad": 50},
    ],
}

ESCENARIO_VACIO = {
    "descripcion": "Estante vacío",
    "productos": [],
}

DEMAND_OK = {"avg_daily": 4.0, "adjusted_daily": 4.0, "trend": "ESTABLE"}

HISTORIAL = [3, 4, 5, 3, 4]

# ── helpers ───────────────────────────────────────────────────

def run_pipeline(escenario: dict, historial: list = HISTORIAL) -> list:
    """Ejecuta la cadena completa y devuelve las recomendaciones."""
    productos = escenario["productos"]

    predictions = [
        predict_stock_outage(historial, p["cantidad"])
        for p in productos
    ]

    stock_items = [
        {
            "producto":      productos[i]["nombre"],
            "stock_actual":  productos[i]["cantidad"],
            "stock_minimo":  5,
            "prediccion":    predictions[i],
        }
        for i in range(len(productos))
    ]

    recomendaciones = generate_recommendations([
        {
            "producto":      item["producto"],
            "stock_actual":  item["stock_actual"],
            "stock_minimo":  item["stock_minimo"],
        }
        for item in stock_items
    ])

    return recomendaciones

# ── pipeline no lanza excepciones ────────────────────────────

def test_pipeline_normal_no_lanza():
    with patch(DEMAND_MODULE, return_value=DEMAND_OK):
        try:
            run_pipeline(ESCENARIO_NORMAL)
        except Exception as exc:
            pytest.fail(f"Pipeline lanzó excepción inesperada: {exc}")

def test_pipeline_critico_no_lanza():
    with patch(DEMAND_MODULE, return_value=DEMAND_OK):
        try:
            run_pipeline(ESCENARIO_CRITICO)
        except Exception as exc:
            pytest.fail(f"Pipeline lanzó excepción inesperada: {exc}")

def test_pipeline_un_producto_no_lanza():
    with patch(DEMAND_MODULE, return_value=DEMAND_OK):
        try:
            run_pipeline(ESCENARIO_UN_PRODUCTO)
        except Exception as exc:
            pytest.fail(f"Pipeline lanzó excepción inesperada: {exc}")

def test_pipeline_escenario_vacio_no_lanza():
    try:
        run_pipeline(ESCENARIO_VACIO)
    except Exception as exc:
        pytest.fail(f"Pipeline con lista vacía lanzó excepción: {exc}")

def test_pipeline_historial_vacio_no_lanza():
    with patch(DEMAND_MODULE, side_effect=ValueError):
        try:
            run_pipeline(ESCENARIO_NORMAL, historial=[])
        except Exception as exc:
            pytest.fail(f"Pipeline con historial vacío lanzó excepción: {exc}")

# ── retornos correctos a lo largo de la cadena ───────────────

def test_pipeline_retorna_lista():
    with patch(DEMAND_MODULE, return_value=DEMAND_OK):
        result = run_pipeline(ESCENARIO_NORMAL)
    assert isinstance(result, list)

def test_pipeline_escenario_vacio_retorna_lista_vacia():
    result = run_pipeline(ESCENARIO_VACIO)
    assert result == []

def test_pipeline_normal_n_recomendaciones():
    with patch(DEMAND_MODULE, return_value=DEMAND_OK):
        result = run_pipeline(ESCENARIO_NORMAL)
    assert len(result) == len(ESCENARIO_NORMAL["productos"])

def test_pipeline_cada_rec_tiene_claves():
    with patch(DEMAND_MODULE, return_value=DEMAND_OK):
        result = run_pipeline(ESCENARIO_NORMAL)
    for r in result:
        assert "producto"      in r
        assert "recomendacion" in r
        assert "prioridad"     in r

# ── flujo de datos entre módulos ─────────────────────────────

def test_pipeline_critico_genera_prioridad_alta():
    # Leche cantidad=0 → AGOTADO → prioridad ALTA
    with patch(DEMAND_MODULE, return_value=DEMAND_OK):
        result = run_pipeline(ESCENARIO_CRITICO)
    prioridades = [r["prioridad"] for r in result]
    assert "ALTA" in prioridades

def test_pipeline_nombres_preservados():
    with patch(DEMAND_MODULE, return_value=DEMAND_OK):
        result = run_pipeline(ESCENARIO_NORMAL)
    nombres_entrada = {p["nombre"] for p in ESCENARIO_NORMAL["productos"]}
    nombres_salida  = {r["producto"] for r in result}
    assert nombres_entrada == nombres_salida

def test_pipeline_detect_products_integra_sin_excepcion():
    # detect_products real (simulado) → pipeline completo
    with patch(DEMAND_MODULE, return_value=DEMAND_OK):
        try:
            escenario = detect_products()
            run_pipeline(escenario)
        except Exception as exc:
            pytest.fail(f"Pipeline con detect_products real lanzó: {exc}")

def test_pipeline_detect_products_retorna_lista():
    with patch(DEMAND_MODULE, return_value=DEMAND_OK):
        escenario = detect_products()
        result    = run_pipeline(escenario)
    assert isinstance(result, list)