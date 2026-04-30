import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

import pytest
from services.prediction.demand_analyzer import calculate_daily_demand

# ── fixtures ─────────────────────────────────────────────────

HISTORIAL_NORMAL  = [3, 4, 5, 3, 4, 6, 5]
HISTORIAL_PICO    = [1, 1, 1, 1, 50]       # pico que ajusta la demanda
HISTORIAL_UNO     = [5]
HISTORIAL_IGUALES = [4, 4, 4, 4, 4]

# ── ValueError con historial vacío ───────────────────────────

def test_empty_list_raises_value_error():
    with pytest.raises(ValueError):
        calculate_daily_demand([])

def test_none_raises_error():
    with pytest.raises((ValueError, TypeError)):
        calculate_daily_demand(None)

# ── estructura del retorno ───────────────────────────────────

def test_returns_dict():
    assert isinstance(calculate_daily_demand(HISTORIAL_NORMAL), dict)

def test_has_avg_daily():
    assert "avg_daily" in calculate_daily_demand(HISTORIAL_NORMAL)

def test_has_adjusted_daily():
    assert "adjusted_daily" in calculate_daily_demand(HISTORIAL_NORMAL)

def test_has_trend():
    assert "trend" in calculate_daily_demand(HISTORIAL_NORMAL)

def test_avg_and_adjusted_are_floats():
    result = calculate_daily_demand(HISTORIAL_NORMAL)
    assert isinstance(result["avg_daily"], float)
    assert isinstance(result["adjusted_daily"], float)

# ── valores correctos ────────────────────────────────────────

def test_avg_daily_correct():
    result = calculate_daily_demand(HISTORIAL_IGUALES)
    assert result["avg_daily"] == 4.0

def test_adjusted_daily_positive():
    result = calculate_daily_demand(HISTORIAL_NORMAL)
    assert result["adjusted_daily"] > 0

def test_pico_adjusted_mayor_que_avg():
    # Con un pico, adjusted debe superar avg
    result = calculate_daily_demand(HISTORIAL_PICO)
    assert result["adjusted_daily"] >= result["avg_daily"]

def test_historial_unico_no_lanza():
    result = calculate_daily_demand(HISTORIAL_UNO)
    assert result["avg_daily"] == 5.0

def test_adjusted_not_negative():
    result = calculate_daily_demand(HISTORIAL_NORMAL)
    assert result["adjusted_daily"] >= 0