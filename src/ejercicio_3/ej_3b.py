import csv 
from pathlib import Path 

def coordenadas_incompletas(registro: dict) -> bool:
    """
    Esta funcion verifica si una coordenada geográfica y le falta la otra.
    registro: dict, representa una fila del dataset.
    Retorna: True, si tiene una coordenada pero le falta la otra.
             False, si existen ambas coordenadas. 
    """
    if "decimalLatitude" in registro:
        lat_key = "decimalLatitude"
    else:
        lat_key = "latitudeDecimal"
    if "decimalLongitude" in registro:
        lon_key = "decimalLongitude"
    else:
        lon_key = "longitudeDecimal"

    #if (registro[lat_key] is None or registro[lat_key] == "" 
    #    or registro[lon_key] is None or registro[lon_key] == ""):
    # Si ambas coordenadas están ausentes/vacías -> no consideramos "incompleto"
    lat_empty = registro[lat_key] is None or registro[lat_key] == ""
    lon_empty = registro[lon_key] is None or registro[lon_key] == ""
    
    if lat_empty and lon_empty:
        return False
    if lat_empty or lon_empty:
        return True
    
    return False
    
    #latitud  = registro[lat_key].strip()
    #longitud = registro[lon_key].strip()

    # Caso 1: Tiene latitud pero le falta longitud
    #if latitud != "" and longitud == "":
    #    return True
    # Caso 2: Tiene longitud pero le falta latitud
    #elif longitud != "" and latitud == "":
    #    return True
    #return False


def analizar_coordenadas(path_route, separador, encoding): 
    """
    Esta función recorre un dataset e identifica si las coordenadas estan
    incompletas, y delega la validación a coordenadas_incompletas():
    path_ruta: path, ruta a dataset.
    separador: str, delimitador del dataset.
    encoding: str, codificacion del dataset.
    return: list, ids de los registros con coordenadas incompletas.
    """
    try: 
        with open (path_route, "r", encoding=encoding) as file:
            csv_reader = csv.reader(file, delimiter=separador)
            #Obtengo encabezado para buscar indices de colummnas 
            encabezado = next(csv_reader)
             
            #Busco los índices de las columnas necesarias, el id es para una lista 
            if "decimalLatitude" in encabezado:
                indice_lat = encabezado.index("decimalLatitude")
            else:
                indice_lat = encabezado.index("latitudeDecimal")

            # Buscamos Longitud (puede estar de dos formas)
            if "decimalLongitude" in encabezado:
                indice_lon = encabezado.index("decimalLongitude")
            else:
                indice_lon = encabezado.index("longitudeDecimal")
                
            indice_id = encabezado.index("occurrenceID")

            #Creo mi lista de incompletos para guardarme sus ids 
            ids_incompletos = []

            #Recorro el resto con el iterador para no cargar todo 
            for fila in csv_reader:
                # Verificamos que la fila tenga todas las columnas necesarias antes de procesar
                if len(fila) > max(indice_lat, indice_lon, indice_id):
                    #Convierto la fila a diccionario y delego la validacion
                    registro = dict(zip(encabezado, fila))
                    if coordenadas_incompletas(registro):
                        ids_incompletos.append(fila[indice_id])

            return ids_incompletos

    except Exception as e:
        print(f"Ocurrió un error en la validación 3.B: {e}")
        return []