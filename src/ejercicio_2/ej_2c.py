from pathlib import Path
import csv

def posicion_columna(path_ruta, separador, encoding):
    """
    Esta función imprime la posición (índice) de cada columna dentro del archivo.
    path_ruta: ruta a dataset pasado.
    separador: delimitador correspondiente al dataset pasado.
    encoding: codificación correspondiente al dataset pasado.  
    """
#Abro el archivo
    with open (path_ruta, "r", encoding=encoding) as archivo:
#Creo el lecto
        lector = csv.reader(archivo, delimiter=separador)
#Me paro en la primera fila
        encabezado = next(lector)
# Recorro el encabezado
        for posicion, elem in enumerate(encabezado): 
            print(f"la posicion del {elem} es {posicion}" )