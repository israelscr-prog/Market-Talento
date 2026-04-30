import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from services.inventory.metrics import count_by_status

# ── fixtures ────────────────────────────────────────────────

STOCK_AGOTADO  = [{"nombre": "Leche",  "cantidad": 0}]
STOCK_BAJO     = [{"nombre": "Pan",    "cantidad": 1}]
STOCK_ADECUADO = [{"nombre": "Leche",  "cantidad": 20}]
STOCK_MIXTO    = [
    {"nombre": "Leche",  "cantidad": 0},
    {"nombre": "Pan",    "cantidad": 1},
    {"nombre": "Agua",   "cantidad": 20},
]
PRODUCTO_BD    = [{"nombre": "ProductoXYZ", "cantidad": 5}]

# ── estructura del retorno ───────────────────────────────────

def test_returns_dict():
    assert isinstance(count_by_status([]), dict)

def test_has_all_keys():
    result = count_by_status([])
    assert "criticos" in result
    assert "bajos" in result
    assert "adecuados" in result
    assert "resumen" in result

def test_resumen_has_all_keys():
    result = count_by_status([])["resumen"]
    assert "total_productos" in result
    assert "total_unidades" in result
    assert "productos_criticos" in result
    assert "productos_bajos" in result
    assert "productos_adecuados" in result

# ── lista vacía ──────────────────────────────────────────────

def test_empty_list_returns_empty_lists():
    result = count_by_status([])
    assert result["criticos"] == []
    assert result["bajos"] == []
    assert result["adecuados"] == []

def test_empty_list_resumen_zeros():
    result = count_by_status([])["resumen"]
    assert result["total_productos"] == 0
    assert result["total_unidades"] == 0

# ── estado crítico (stock == 0) ──────────────────────────────

def test_stock_cero_es_critico():
    result = count_by_status(STOCK_AGOTADO)
    assert len(result["criticos"]) == 1

def test_stock_cero_estado_agotado():
    result = count_by_status(STOCK_AGOTADO)
    assert result["criticos"][0]["estado"] == "AGOTADO"

def test_stock_cero_no_en_bajos_ni_adecuados():
    result = count_by_status(STOCK_AGOTADO)
    assert len(result["bajos"]) == 0
    assert len(result["adecuados"]) == 0

# ── estado bajo (0 < stock < stock_minimo) ───────────────────

def test_stock_bajo_clasificado_correctamente():
    result = count_by_status(STOCK_BAJO)
    assert len(result["bajos"]) == 1

def test_stock_bajo_estado_correcto():
    result = count_by_status(STOCK_BAJO)
    assert result["bajos"][0]["estado"] == "BAJO"

# ── estado adecuado (stock >= stock_minimo) ──────────────────

def test_stock_adecuado_clasificado_correctamente():
    result = count_by_status(STOCK_ADECUADO)
    assert len(result["adecuados"]) == 1

def test_stock_adecuado_estado_correcto():
    result = count_by_status(STOCK_ADECUADO)
    assert result["adecuados"][0]["estado"] == "ADECUADO"

# ── mezcla de estados ────────────────────────────────────────

def test_mixto_clasifica_los_tres():
    result = count_by_status(STOCK_MIXTO)
    assert len(result["criticos"]) == 1
    assert len(result["bajos"]) == 1
    assert len(result["adecuados"]) == 1

def test_mixto_total_correcto():
    result = count_by_status(STOCK_MIXTO)
    assert result["resumen"]["total_productos"] == 3

# ── producto no encontrado en BD ─────────────────────────────

def test_producto_no_en_bd_ignorado():
    result = count_by_status(PRODUCTO_BD)
    total = (len(result["criticos"]) +
             len(result["bajos"]) +
             len(result["adecuados"]))
    assert total == 0

def test_producto_no_en_bd_total_productos_cuenta():
    result = count_by_status(PRODUCTO_BD)
    assert result["resumen"]["total_productos"] == 1