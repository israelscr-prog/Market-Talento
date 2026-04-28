@'
"""
main.py
Punto de entrada principal del sistema de inventario.
Levanta el servidor Flask con todas las rutas usando los servicios refactorizados.
Uso: python main.py
"""

from flask import Flask, jsonify, render_template_string
from datetime import datetime

from services.vision.detector import detect_products
from services.inventory.metrics import count_by_status
from services.inventory.valuation import calculate_inventory_value
from services.inventory.recommender import generate_recommendations
from services.prediction.stock_predictor import predict_stock_outage
from services.database.db_reader import get_product_info, get_all_products
from services.database.db_filter import get_sales_history

app = Flask(__name__)

# ============================================================
# HTML TEMPLATE (temporal — se moverá a archivo .html en Fase 4)
# ============================================================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Inventario Inteligente</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .card { border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 20px; border: none; }
        .card-header { background: linear-gradient(45deg, #667eea, #764ba2); color: white; border-radius: 15px 15px 0 0 !important; }
        .btn-api { margin: 5px; border-radius: 20px; }
        .response-area { background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 10px; font-family: monospace; font-size: 12px; max-height: 450px; overflow-y: auto; }
        .stat-card { text-align: center; padding: 20px; border-radius: 10px; color: white; }
    </style>
</head>
<body>
<div class="container">
    <div class="text-center mb-4">
        <h1 class="text-white">Sistema de Inventario Inteligente</h1>
        <p class="text-white-50">Refactorizado — Fase 1</p>
    </div>
    <div class="row">
        <div class="col-md-4">
            <div class="card">
                <div class="card-header"><h5 class="mb-0">Endpoints</h5></div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <button class="btn btn-primary btn-api"   onclick="callAPI('/api/test')">GET /api/test</button>
                        <button class="btn btn-success btn-api"   onclick="callAPI('/api/analizar')">GET /api/analizar</button>
                        <button class="btn btn-info btn-api"      onclick="callAPI('/api/productos')">GET /api/productos</button>
                        <button class="btn btn-warning btn-api"   onclick="callAPI('/api/producto/Leche')">GET /api/producto/Leche</button>
                        <button class="btn btn-secondary btn-api" onclick="callAPI('/api/recomendaciones')">GET /api/recomendaciones</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-8">
            <div class="card">
                <div class="card-header"><h5 class="mb-0">Respuesta</h5></div>
                <div class="card-body">
                    <div id="response" class="response-area">Haz clic en un endpoint para ver la respuesta...</div>
                </div>
            </div>
        </div>
    </div>
</div>
<script>
    function callAPI(url) {
        document.getElementById("response").innerHTML = "Cargando...";
        fetch(url)
            .then(r => r.json())
            .then(data => {
                document.getElementById("response").innerHTML =
                    "<div style=\'color:#9cdcfe\'>Endpoint: " + url + "</div><hr>" +
                    "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
            })
            .catch(err => {
                document.getElementById("response").innerHTML = "Error: " + err;
            });
    }
</script>
</body>
</html>
'''

# ============================================================
# RUTAS
# ============================================================

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/test")
def test_api():
    return jsonify({
        "status": "success",
        "message": "API de Inventario Inteligente funcionando",
        "version": "2.0-refactorizada",
        "timestamp": datetime.now().isoformat(),
        "servicios": ["vision", "database", "prediction", "inventory"]
    })


@app.route("/api/analizar")
def analizar_inventario():
    deteccion = detect_products()
    productos_detectados = deteccion.get("productos", [])

    productos_analizados = []
    for p in productos_detectados:
        nombre, stock = p["nombre"], p["cantidad"]
        info = get_product_info(nombre)
        if info:
            pred = predict_stock_outage(get_sales_history(nombre, 30), stock, info)
            productos_analizados.append({
                "producto": nombre,
                "stock_actual": stock,
                "informacion": {"categoria": info.get("categoria"), "precio": info.get("precio")},
                "prediccion": pred
            })
        else:
            productos_analizados.append({
                "producto": nombre, "stock_actual": stock,
                "informacion": None,
                "prediccion": {"estado": "NO ENCONTRADO EN BD"}
            })

    metrics   = count_by_status(productos_detectados)
    valor     = calculate_inventory_value(productos_detectados)

    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "deteccion": deteccion,
        "productos": productos_analizados,
        "analisis": metrics,
        "valor_inventario": valor,
        "resumen": {
            "total_productos": len(productos_analizados),
            "productos_criticos": metrics["resumen"]["productos_criticos"],
            "valor_total": valor
        }
    })


@app.route("/api/productos")
def obtener_productos():
    todos = get_all_products()
    return jsonify({"status": "success", "total": len(todos), "productos": todos})


@app.route("/api/producto/<nombre>")
def obtener_producto(nombre):
    producto = get_product_info(nombre)
    if producto:
        return jsonify({"status": "success", "producto": producto})
    return jsonify({"status": "error", "message": f"Producto '{nombre}' no encontrado"}), 404


@app.route("/api/recomendaciones")
def obtener_recomendaciones():
    deteccion = detect_products()
    metrics   = count_by_status(deteccion["productos"])
    recs      = generate_recommendations(metrics["criticos"] + metrics["bajos"])
    return jsonify({"status": "success", "recomendaciones": recs, "total": len(recs)})


# ============================================================
# ARRANQUE
# ============================================================

if __name__ == "__main__":
    print("=" * 55)
    print("  SISTEMA DE INVENTARIO — VERSION REFACTORIZADA")
    print("=" * 55)
    print("  GET  /")
    print("  GET  /api/test")
    print("  GET  /api/analizar")
    print("  GET  /api/productos")
    print("  GET  /api/producto/<nombre>")
    print("  GET  /api/recomendaciones")
    print("=" * 55)
    print("  Abre: http://localhost:5000")
    print("=" * 55)
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
'@ | Set-Content "markettalento-inventario\main.py" -Encoding UTF8

Write-Host "✅ main.py creado" -ForegroundColor Green