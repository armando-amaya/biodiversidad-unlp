from pathlib import Path
import csv

def columnas_con_registro_nulo(path_ruta, separador, encoding):
    """
    Esta función  retorne las columnas que posean al menos un dato con registro nulo.
    path_ruta: ruta a dataset pasado.
    separador: delimitador correspondiente al dataset pasado.
    encoding: codificación correspondiente al dataset pasado.  
    """
#Abro el archivo
    with open (path_ruta, "r", encoding=encoding) as archivo:
#Creo el lecto
        lector = csv.reader(archivo, delimiter=separador)
        encabezado = next(lector)
#Cro una lista para guardar las columnas vacias
        columnas_nulas = []
#Recorro las filas 
        for fila in lector:
#Recorro las columnas
            for indice, celda in enumerate(fila):
#Veo si esta vacio
                if celda == "" :
#Si todava no esta en la lista lo agrego, evito reptidos
                    if encabezado[indice] not in columnas_nulas:
                        columnas_nulas.append(encabezado[indice])
#Devuelvo la lista con los nombres de las columnas nulas
    return columnas_nulas
