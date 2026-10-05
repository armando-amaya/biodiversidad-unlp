import csv
from pathlib import Path

def obtener_columnas(path_route, separador, encoding):
    """
    Esta función extrae los nombres de las columnas de la primera fila del dataset.
    Utiliza un iterador para optimizar el uso de memoria.
    path_route: ruta al dataset (original o procesado).
    separador: delimitador correspondiente al dataset pasado.
    encoding: codificación correspondiente al dataset pasado.
    Retorna: una lista con los nombres de las columnas o una lista vacía si hay error.
    """
    try:
        # Abro el archivo en modo r con el encoding 
        # Uso 'with' para asegurarme que el archivo se cierre solo cuando termina la indentacion 
        with open(path_route, "r", encoding=encoding) as file:
            csv_reader = csv.reader(file, delimiter=separador)
            
            # Uso next() para leer solo la primera fila, como es un iterador nos ahorra memoria 
            columnas = next(csv_reader)
            
            # Retorno la lista encontrada
            return columnas
            
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en: {path_route}")
        return []
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return []        