from pathlib import Path
import csv
import re
"""Función auxiliar para obtener la columna ID y el delimitador según el archivo."""
def _detectar_configuracion(path_ruta: Path) -> tuple:
    path_str = str(path_ruta).lower()
    
    if "iadiza" in path_str:
        return "gbifID", ","
    elif "inaturalist" in path_str:
        return "id", "\t"
    else:  # xeno-canto
        return "id", ","


def _generar_nuevo_id(path_ruta: Path, col_id: str, delimiter: str) -> str:
    """Función auxiliar que lee el archivo y calcula el próximo ID único."""
    with open(path_ruta, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        encabezado = next(reader)
        filas = [row for row in reader if row]

    # Si la columna de ID no existe en el encabezado, generamos un ID simple y seguro
    if col_id not in encabezado:
        contador = len([r for r in filas if any(r)]) + 1
        return f"{contador}"

    idx = encabezado.index(col_id)
    ids = {r[idx] for r in filas if len(r) > idx}
    ultimo_id = filas[-1][idx] if filas and len(filas[-1]) > idx else "0"

    def ajustar(id_str):
        match = re.search(r"(\d+)(?!.*\d)", str(id_str))
        if not match:
            # si no hay número en el id, simplemente añadimos un sufijo
            return f"{id_str}_1"
        num = int(match.group(1))
        # Si es iadiza resta 1, si no (inaturalist / xeno-canto) suma 1
        num = num - 1 if col_id == "gbifID" else num + 1
        return id_str[:match.start()] + str(num) + id_str[match.end():]

    nuevo_id = ajustar(ultimo_id)
    # Evitamos bucle infinito: límite de intentos
    intentos = 0
    while nuevo_id in ids and intentos < 1000:
        nuevo_id = ajustar(nuevo_id)
        intentos += 1

    return nuevo_id

"""
Toma un registro vacío, uno con datos a añadir y la ruta del dataset. Construye un diccionario 
listo para ser añadido al dataset, delegando tareas en funciones más pequeñas.
"""

def construir_fila(registro_vacio: dict, datos: dict, path_ruta) -> dict:

    # 1. Copiamos la estructura base
    fila = registro_vacio.copy()

    # 2. Delegamos la detección de config y la generación del ID
    col_id, delimiter = _detectar_configuracion(Path(path_ruta))
    fila[col_id] = _generar_nuevo_id(Path(path_ruta), col_id, delimiter)

    # 3. Completamos los datos enviados por parámetro
    for clave, valor in datos.items():
        if clave != col_id:
            fila[clave] = valor

    # Reordeno el diccionario poniendo el ID primero con lambda
    llaves_ordenadas = sorted(fila.keys(), key=lambda k: 0 if k == col_id else 1)
    fila_ordenada = {k: fila[k] for k in llaves_ordenadas}

    return fila_ordenada