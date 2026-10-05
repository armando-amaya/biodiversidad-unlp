from pathlib import Path
import csv


def validar_latitud(path_ruta, separador, encoding, lat):
    """
    Esta función agrupe y ejecuta todas las validaciones para el campo latitud.
    path_ruta: ruta a dataset pasado.
    separador: delimitador correspondiente al dataset pasado.
    encoding: codificación correspondiente al dataset pasado. 
    lat: numero a validar.
    """    
#Abro el archivo
    with open (path_ruta, "r", encoding=encoding) as archivo:
#Creo el lector
        lector = csv.reader(archivo, delimiter=separador)
        encabezado = next(lector)
#Veo que no sea un numero 
        if not isinstance(lat, (int, float)):
            return False, "La latitud debe ser un número"
#Veo que cumpla con el rango
        if lat < -90 or lat > 90:
            return False, "La latitud debe estar entre -90 y 90"
        return True, "Latitud válida"


def validar_longitud(path_ruta, separador, encoding, lon):
    """
    Esta función agrupe y ejecuta todas las validaciones para el campo longitud.
    path_ruta: ruta a dataset pasado.
    separador: delimitador correspondiente al dataset pasado.
    encoding: codificación correspondiente al dataset pasado. 
    lon: numero a validar.
    """    
#Abro el archivo
    with open (path_ruta, "r", encoding=encoding) as archivo:
#Creo el lector
        lector = csv.reader(archivo, delimiter=separador)
        encabezado = next(lector)
#Veo que no sea un numero 
        if not isinstance(lon, (int, float)):
            return False, "La longitud debe ser un número"
#Veo que cumpla con el rango
        if lon < -180 or lon > 180:
            return False, "La longitud debe estar entre -180 y 180"
        return True, "Longitud válida"