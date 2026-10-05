import csv

def obtener_columna(ruta, nombre_columna, separador):
    """
    Función auxiliar que recibe una un dataset con su respectivo delimitador
    y el nombre de una columna a buscar y retorna una lista con todos los
    valores de una columna específica del dataset.
    ruta: path, con la ruta al dataset.
    separador: string, delimitador del dataset.
    nombre_columna: string, identificador de una columna del dataset.
    """
    with open(ruta, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo, delimiter=separador)
        return [fila[nombre_columna] for fila in lector]