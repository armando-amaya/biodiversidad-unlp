from pathlib import Path
import csv

def aparicion_en_columna(path_ruta, separador, encoding, nombre_columna):    
    """
        Esta función retorne la frecuencia de aparición de cada valor, dada una columna pasada.
        path_ruta: ruta a dataset pasado.
        separador: delimitador correspondiente al dataset pasado.
        encoding: codificación correspondiente al dataset pasado. 
        nombre_columna: columna a ver apariciones.
    """
#Abro el archivo
    with open (path_ruta, "r", encoding=encoding) as archivo:
#Creo el lector
        lector = csv.reader(archivo, delimiter=separador)
        encabezado = next(lector)
#Creo un dicc para contar cuantas veces aparece cada palabra         
        aparicion = {}
#Busco la posicion de la clumna
        i= encabezado.index(nombre_columna)
#Recrro la filas en el erchivo         
        for fila in lector:
#Busco el dato en la columna que quiero
            dato = fila[i]
#Si el dato no esta lo agrego y sino sumo uno en el que ya esa
            if dato not in aparicion:
                aparicion[dato] = 1
            else: 
                aparicion[dato] += 1
#Devuelvo el diccionario con la canidad de apariciones de esa columna                
    return aparicion
