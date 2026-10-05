from pathlib import Path
import csv

def buscar_registros(path_ruta, separador, encoding, filtros):
    """
    Esta función permite buscar registros por múltiples columnas, retorna los registros que cumplen la condición. 
    path_ruta: ruta a dataset pasado.
    separador: delimitador correspondiente al dataset pasado.
    encoding: codificación correspondiente al dataset pasado. 
    filtros: conjunto de columnas a filtrar con los valores deseados.
    """  
    with open(path_ruta,'r',encoding=encoding) as archivo:
#DictReader usa la primera fila como nombres de columnas (llaves)
        lector = csv.DictReader(archivo)
#Creo una lista para guerdar loa que cumplen con los valores a buscar
        resultados = []
        for fila in lector:
            coincide = True
#Verificamos cada condición del filtro
            for columna, valor_buscado in filtros.items():
#Si una sola columna no coincide, descartamos la fila
                if fila.get(columna) != str(valor_buscado):
                    coincide = False
                    break 
#Si cumple lo guardo           
            if coincide:
                resultados.append(fila)
                
    return resultados