import random
from .scenario_loader import _load_scenarios


def detect_products(image_path: str | None = None) -> dict:
    """Orquesta la detección de productos en una imagen.

    Selecciona un escenario de detección simulada delegando
    la carga de datos en scenario_loader. Esta función solo
    orquesta, no contiene datos ni lógica de clasificación.

    Args:
        image_path: Ruta de la imagen a analizar.
            None activa el modo simulación (por defecto).

    Returns:
        Dict con las claves:
            - descripcion (str): Descripción del escenario detectado.
            - productos (list[dict]): Productos detectados con
              claves nombre, cantidad y confianza.

    Example:
        >>> resultado = detect_products()
        >>> "productos" in resultado
        True
        >>> detect_products("ruta/imagen.jpg")
        {"descripcion": "...", "productos": [...]}
    """
    return random.choice(_load_scenarios())