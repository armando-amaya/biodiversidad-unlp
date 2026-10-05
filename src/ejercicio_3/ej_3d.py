from pathlib import Path
import csv


def deteccion_duplicados(path_ruta, delimiter=",", encoding="utf-8"):    
    """
    Esta función utilizando los “ID” detecta posibles registros duplicados, devuelviendo la cantidad de duplicados y cuales son.
    path_ruta: ruta a dataset pasado.
    separador: delimitador correspondiente al dataset pasado.
    encoding: codificación correspondiente al dataset pasado. 
    """    
    with open(path_ruta, mode="r", encoding=encoding) as archivo:
        lector = csv.reader(archivo, delimiter=delimiter)
        encabezado = next(lector)
        id_contador = {}
        lista_repetidos = []
        i = encabezado.index("id")
        for fila in lector:
            id_actual = fila[i]
            if id_actual not in id_contador:
                id_contador[id_actual] = 1
            else:
                id_contador[id_actual] += 1
    for elem, cantidad in id_contador.items():
        if cantidad > 1:
            lista_repetidos.append(elem)
    tot_repetidos = len(lista_repetidos)
    return tot_repetidos, lista_repetidos

