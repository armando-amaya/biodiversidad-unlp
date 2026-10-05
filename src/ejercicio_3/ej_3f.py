import csv
from pathlib import Path


def incertidumbre_invalida_fila(fila, columna):
    """
    Analiza si el valor de la incertidumbre es válido.
    Retorna (registro_id, valor) si es inválida, o None si es válida.
    fila: fila que analiza
    columna: columna a verificar
    """
    valor = fila.get(columna)

    registro_id = (
        fila.get("occurrenceID")
        or fila.get("id")
        or fila.get("gbifID")
        or "N/A"
    )

    if valor is not None and valor != "":
        try:
            if float(valor) < 0:
                return (registro_id, valor)
        except ValueError:
            return (registro_id, valor)

    return None


def incertidumbre_invalida(ruta_csv, columna, delimiter=","):
    """
    Detecta incertidumbres inválidas en una columna de un archivo CSV.
    Retorna un diccionario que tiene:
    - "cantidad": número de valores inválidos encontrados.
    - "registros": lista de tuplas (registro_id, valor) con los valores inválidos.
    ruta_csv: ruta al archivo CSV a analizar.
    columna: es la columna del CSV que contiene los datos a validar.
    delimiter: delimitador correspondiente al dataset pasado.
    
    """

    ruta_csv = Path(ruta_csv)
    invalidos = []

    with ruta_csv.open(encoding="utf-8-sig") as f:
        lector = csv.DictReader(f, delimiter=delimiter)

        if columna not in lector.fieldnames:
            raise ValueError(f"La columna '{columna}' no existe en el dataset")

        for fila in lector:
            resultado = incertidumbre_invalida_fila(fila, columna)
            if resultado is not None:
                invalidos.append(resultado)

    return {
        "cantidad": len(invalidos),
        "registros": invalidos
    }

