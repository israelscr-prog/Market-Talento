def _load_scenarios() -> list[dict]:
    """Devuelve la lista de escenarios de detección simulada disponibles.

    Cada escenario representa una situación real de estantería con
    productos detectados, su cantidad y nivel de confianza de detección.
    Esta función solo contiene datos, sin lógica de selección.

    Returns:
        Lista de dicts, cada uno con las claves:
            - descripcion (str): Descripción del escenario.
            - productos (list[dict]): Productos detectados con
              claves nombre, cantidad y confianza.

    Example:
        >>> escenarios = _load_scenarios()
        >>> len(escenarios)
        3
        >>> escenarios[0]["productos"][0]
        {"nombre": "Leche", "cantidad": 8, "confianza": 0.92}
    """
    return [
        {"descripcion": "Estanteria supermercado - Stock moderado", "productos": [
            {"nombre": "Leche",  "cantidad": 8,  "confianza": 0.92},
            {"nombre": "Huevos", "cantidad": 5,  "confianza": 0.88},
            {"nombre": "Pan",    "cantidad": 3,  "confianza": 0.85},
            {"nombre": "Agua",   "cantidad": 12, "confianza": 0.95},
            {"nombre": "Cafe",   "cantidad": 6,  "confianza": 0.90},
        ]},
        {"descripcion": "Almacen tienda - Stock alto", "productos": [
            {"nombre": "Arroz",  "cantidad": 25, "confianza": 0.94},
            {"nombre": "Leche",  "cantidad": 18, "confianza": 0.91},
            {"nombre": "Huevos", "cantidad": 22, "confianza": 0.89},
            {"nombre": "Agua",   "cantidad": 30, "confianza": 0.96},
            {"nombre": "Cafe",   "cantidad": 15, "confianza": 0.87},
        ]},
        {"descripcion": "Nevera comercial - Stock bajo", "productos": [
            {"nombre": "Yogur",       "cantidad": 4, "confianza": 0.83},
            {"nombre": "Queso",       "cantidad": 2, "confianza": 0.80},
            {"nombre": "Mantequilla", "cantidad": 3, "confianza": 0.82},
            {"nombre": "Zumo",        "cantidad": 5, "confianza": 0.86},
            {"nombre": "Fiambre",     "cantidad": 1, "confianza": 0.78},
        ]},
    ]