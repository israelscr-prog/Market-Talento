# Documento que sumariza lo que se ha hecho dia a dia 

## 27.04.26 empiece a las 10:30am y terminado a las 13:45

- Identificación de los dos archivos heredados (InventarioAlfa.py, EndPoint_Api.py)
- Análisis de diferencias entre ambos archivos
- Archivos creados de README.md, requirements.txt
 Market-Talento/
├── .qodo/
├── .vscode/
├── .gitignore
├── EndPoint_Api.py
├── Inventario.md
├── InventarioAlfa.py
├── LICENSE
├── README.md
└── requirements.txt

## 28.04.26 Empiece a 10:15 am terminado a las 13:55

- Creacion de boton en HTLM paracambiar pagina de ` InventarionAlfa.py` a `EndPoint.py`
- Creacion de estructura modular objetivo con carpetas

- Creación de todas las carpetas con sus `__init__.py`
- Creacion de documentos:   
──> `Final.md` --> Para documentar, corregir y seguir todas las 7 fases de problemas detectadas de Memoria de Refactorización     
──> `DiaaDia.md` --> Para documentar todos los pasos a pasos hechos dia a dia.
- Añadido el `ci.yml` para trabajar con GitHub Actions
- Añadido en Database        
──> `product_db.py` y los 11 productos    
──> `dn_filter.py`Funciones de Filtro    
──> `db_reader.py`Funcione Lectura
- Movimiento de codigo heredado a carpeta `legacy/`
- Creacion de **nuevo** `main.py`.

## 29.04.26 Empiece a 00:15am, terminado a 
- Añadido en Database   
──> 14 Productos para un total de 25
- Añadido Docstrings Google en `db_reader` y  `dn_filter.py`
- Creacion de archivos y funciones con Docstring Google:   
──> `detector.py` --> Con funciones de  ` def detect_products() `   
──> `scenario_loader.py` --> Con funcion de `def _load_scenarios()`

- Creacion de archivos y funciones con Docstring Google:   
──> `metric.py` con funcion de `def count_by_status`    
──> `valuation.py` con funcion de `def calculate_inventory_value`

- Creacion de `recomender.py` y funcion de `def geneerate_recommendations`
- 