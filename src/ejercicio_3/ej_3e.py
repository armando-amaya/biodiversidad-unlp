import csv
from pathlib import Path


def validar_registro(fila, columna, codigos_validos):
    """Valida si el registro está en mayúsculas, sin espacios 
    y si es parte de los códigos válidos."""

    valor = fila.get(columna)

    if valor:
        # Validación de Formato 
        if valor != valor.strip().upper():
            return valor # Reportar error de formato

        # Validación de Contenido
        if valor not in codigos_validos:
            return valor # Reportar código inexistente

    return None

def detectar_codigos_invalidos(ruta_csv, lista_validos, columna):
    """
    Esta función detecta codigos invalidos en los codigos de país del dataset.
    Informa los códigos con error de formato o inexistentes.
    ruta_csv: ruta a dataset original.
    lista_validos: archivo con una lista que tiene todos los códigos de país válidos.
    columna: columna identificadora que vamos a revisar en el dataset.
    """

    try:
        # Cargar códigos válidos
        codigos_validos = set(lista_validos)

        invalidos = set()

        # Leer CSV
        with ruta_csv.open(encoding="utf-8") as f:
            lector = csv.DictReader(f)

            if not lector.fieldnames or columna not in lector.fieldnames:
                return []

            for fila in lector:
                resultado = validar_registro(fila, columna, codigos_validos)

                if resultado:
                    invalidos.add(resultado)

        return sorted(invalidos)

    except Exception as e:
        print(f"Error en validación countryCode: {e}")
        return []