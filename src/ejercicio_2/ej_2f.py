from pathlib import Path
import csv

def porcentaje_registro_nulo_columna(path_ruta, separador, encoding):
    """
    Esta función retorne para cada columna el porcentaje de registros nulos.
    path_ruta: ruta a dataset pasado.
    separador: delimitador correspondiente al dataset pasado.
    encoding: codificación correspondiente al dataset pasado.  
    """
#Abro el archivo
    with open (path_ruta, "r", encoding=encoding) as archivo:
#Creo el lecto
        lector = csv.reader(archivo, delimiter=separador)
        encabezado = next(lector)
#Creo una dicc para guardar el prcentaje por columna
        porcentaje = {columna: 0 for columna in encabezado}
#Creo un contador que cuente las fils
        tot_filas = 0 
#Recorro las filas 
        for fila in lector:
#Cuento las filas
            tot_filas += 1 
#Recorro las columnas
            for indice, celda in enumerate(fila):
#Veo si esta vacio para sumar a el dicc
                if celda == "" :
                    nombre_col = encabezado[indice]
                    porcentaje[nombre_col] += 1
#Divido los nulos para sacar el pocentaje por columna
    for elem in porcentaje:
        porcentaje[elem] = (porcentaje[elem] / tot_filas) * 100
#Devuelvo la lista con los nombres de las columnas nulas
    return porcentaje