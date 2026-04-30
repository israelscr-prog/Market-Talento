import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

import pytest
from unittest.mock import patch
from services.prediction.stock_predictor import predict_stock_outage

MODULE = "services.prediction.stock_predictor.calculate_daily_demand"

# ── fixtures ─────────────────────────────────────────────────

HISTORIAL  = [3, 4, 5, 3, 4]
DEMAND_OK  = {"avg_daily": 4.0, "adjusted_daily": 4.0, "trend": "ESTABLE"}
DEMAND_ALT = {"avg_daily": 2.0, "adjusted_daily": 2.0, "trend": "ESTABLE"}

# ── estructura del retorno ───────────────────────────────────

def test_returns_dict():
    with patch(MODULE, return_value=DEMAND_OK):
        assert isinstance(predict_stock_outage(HISTORIAL, 20), dict)

def test_has_required_keys():
    with patch(MODULE, return_value=DEMAND_OK):
        result = predict_stock_outage(HISTORIAL, 20)
    assert "dias_hasta_agotarse"     in result
    assert "estado"                  in result
    assert "cantidad_recomendada"    in result
    assert "consumo_promedio_diario" in result

# ── stock agotado (stock <= 0) ────────────────────────────────

def test_stock_cero_estado_agotado():
    result = predict_stock_outage(HISTORIAL, 0)
    assert result["estado"] == "AGOTADO"

def test_stock_negativo_estado_agotado():
    result = predict_stock_outage(HISTORIAL, -5)
    assert result["estado"] == "AGOTADO"

def test_stock_cero_dias_es_cero():
    result = predict_stock_outage(HISTORIAL, 0)
    assert result["dias_hasta_agotarse"] == 0

def test_stock_cero_no_llama_demand(mocker):
    mock = mocker.patch(MODULE)
    predict_stock_outage(HISTORIAL, 0)
    mock.assert_not_called()

# ── historial vacío → ValueError → SIN HISTORIAL ────────────

def test_historial_vacio_estado_sin_historial():
    result = predict_stock_outage([], 10)
    assert result["estado"] == "SIN HISTORIAL"

def test_historial_vacio_dias_es_cero():
    result = predict_stock_outage([], 10)
    assert result["dias_hasta_agotarse"] == 0

def test_historial_vacio_no_propaga_excepcion():
    try:
        predict_stock_outage([], 10)
    except Exception as exc:
        pytest.fail(f"Propagó excepción inesperada: {exc}")

def test_historial_vacio_cantidad_recomendada_positiva():
    result = predict_stock_outage([], 10)
    assert result["cantidad_recomendada"] > 0

# ── estado CRITICO (dias <= 2) ────────────────────────────────

def test_critico_con_mock():
    # 4 unidades / 4/día = 1 día → CRITICO
    with patch(MODULE, return_value=DEMAND_OK):
        result = predict_stock_outage(HISTORIAL, 4)
    assert result["estado"] == "CRITICO"

def test_critico_dias_menor_igual_2():
    with patch(MODULE, return_value=DEMAND_OK):
        result = predict_stock_outage(HISTORIAL, 4)
    assert result["dias_hasta_agotarse"] <= 2

# ── estado BAJO (dias <= 5) ───────────────────────────────────

def test_bajo_con_mock():
    # 16 / 4 = 4 días → BAJO
    with patch(MODULE, return_value=DEMAND_OK):
        result = predict_stock_outage(HISTORIAL, 16)
    assert result["estado"] == "BAJO"

# ── estado MODERADO (dias <= 10) ─────────────────────────────

def test_moderado_con_mock():
    # 28 / 4 = 7 días → MODERADO
    with patch(MODULE, return_value=DEMAND_OK):
        result = predict_stock_outage(HISTORIAL, 28)
    assert result["estado"] == "MODERADO"

# ── estado ADECUADO (dias > 10) ──────────────────────────────

def test_adecuado_con_mock():
    # 50 / 4 = 12.5 días → ADECUADO
    with patch(MODULE, return_value=DEMAND_OK):
        result = predict_stock_outage(HISTORIAL, 50)
    assert result["estado"] == "ADECUADO"

# ── mock verifica delegación correcta ────────────────────────

def test_mock_llama_calculate_daily_demand(mocker):
    mock = mocker.patch(MODULE, return_value=DEMAND_OK)
    predict_stock_outage(HISTORIAL, 20)
    mock.assert_called_once_with(HISTORIAL)

def test_mock_usa_adjusted_daily(mocker):
    mocker.patch(MODULE, return_value=DEMAND_ALT)
    result = predict_stock_outage(HISTORIAL, 20)
    # 20 / 2.0 = 10 días → MODERADO
    assert result["dias_hasta_agotarse"] == 10.0

def test_cantidad_recomendada_usa_avg_daily(mocker):
    mocker.patch(MODULE, return_value=DEMAND_OK)
    result = predict_stock_outage(HISTORIAL, 20)
    # avg_daily=4.0 → round(4.0 * 10) = 40
    assert result["cantidad_recomendada"] == 40

# ── product_info (parámetro reservado) ───────────────────────

def test_product_info_none_no_rompe():
    with patch(MODULE, return_value=DEMAND_OK):
        result = predict_stock_outage(HISTORIAL, 20, product_info=None)
    assert "estado" in result

def test_product_info_dict_no_rompe():
    with patch(MODULE, return_value=DEMAND_OK):
        result = predict_stock_outage(HISTORIAL, 20, product_info={"id": 1})
    assert "estado" in result