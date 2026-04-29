import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from unittest.mock import patch
from services.vision.detector import detect_products
from services.vision.scenario_loader import _load_scenarios


# ── sin mock ────────────────────────────────────────────────

def test_returns_dict():
    assert isinstance(detect_products(), dict)


def test_has_descripcion_key():
    assert "descripcion" in detect_products()


def test_has_productos_key():
    assert "productos" in detect_products()


def test_productos_is_list():
    assert isinstance(detect_products()["productos"], list)


def test_productos_not_empty():
    assert len(detect_products()["productos"]) > 0


def test_accepts_image_path():
    result = detect_products(image_path="ruta/imagen.jpg")
    assert isinstance(result, dict)


def test_accepts_none_image_path():
    result = detect_products(image_path=None)
    assert isinstance(result, dict)


# ── con mock de random.choice ────────────────────────────────

def test_mock_returns_first_scenario():
    escenarios = _load_scenarios()
    with patch("services.vision.detector.random.choice", return_value=escenarios[0]):
        result = detect_products()
        assert result == escenarios[0]


def test_mock_returns_specific_scenario():
    escenarios = _load_scenarios()
    with patch("services.vision.detector.random.choice", return_value=escenarios[2]):
        result = detect_products()
        assert result["descripcion"] == escenarios[2]["descripcion"]


def test_mock_called_once():
    with patch("services.vision.detector.random.choice") as mock_choice:
        mock_choice.return_value = _load_scenarios()[0]
        detect_products()
        mock_choice.assert_called_once()


# ── edge case: lista vacía ───────────────────────────────────

def test_mock_empty_list_raises():
    with patch("services.vision.scenario_loader._load_scenarios", return_value=[]):
        with patch("services.vision.detector.random.choice", side_effect=IndexError):
            try:
                detect_products()
                assert False, "Debería haber lanzado IndexError"
            except IndexError:
                pass