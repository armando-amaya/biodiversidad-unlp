from pathlib import Path
import csv

def validar_registro(registro: dict) -> bool:
    """
    Esta función valida que las coordenadas geográficas de un registro sean válidas.
    registro: diccionario que representa una fila del dataset, donde las claves son los nombres de las columnas.
    return: True si las coordenadas son válidas o están ausentes/vacías, False si alguna coordenada está fuera de rango definido
    o si no puede convertirse a número.
    """
    lat_key = "decimalLatitude" if "decimalLatitude" in registro else "latitudeDecimal"
    lon_key = "decimalLongitude" if "decimalLongitude" in registro else "longitudeDecimal"

    try:
        lat = registro[lat_key]
        lon = registro[lon_key]
        
        if lat is None or lat == "" or lon is None or lon == "":
            return True
        
        lat = float(lat)
        lon = float(lon)
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return False
    except ValueError:
        return False
    return True

def deteccion_de_errores(path_ruta, separador, encoding):    
#Abro el archivo
    with open (path_ruta, "r", encoding=encoding) as archivo:
#Creo el lector
        lector = csv.reader(archivo, delimiter=separador)
        encabezado = next(lector)
#Creo una lista para devolver los incorrectos y un contador para saber cuantos errores hay 
        lista = []
        contador = 0
#Veo cual de los dos nombre me toca para latitud y longitud
        if "decimalLatitude" in encabezado:
            i_lat = encabezado.index("decimalLatitude")
        else:    
            i_lat = encabezado.index("latitudeDecimal")
        if "decimalLongitude" in encabezado:
            i_long = encabezado.index("decimalLongitude")
        else:    
            i_long = encabezado.index("longitudeDecimal")
# Recorro fila 
        for fila in lector:
#Convierto la fila a diccionario y delego la validacion
            registro = dict(zip(encabezado, fila))
            validacion = validar_registro(registro)
#Si esta en falso, lo agrego y sumo 
            if validacion == False: 
                contador += 1
                lista.append(fila)
    return lista, contador