import csv
from pathlib import Path

# Constantes para América del Sur (aproximadas)
LAT_MAX = 13.0
LAT_MIN = -56.0
LON_MAX = -34.0
LON_MIN = -92.0


def coordenadas_en_america(registro: dict) -> bool:
    """
    Valida si las coordenadas de un único registro en formato diccionario
    pertenecen al rango de América.
    Retorna True si están dentro del rango, False si están fuera.
    Reutilizable externamente para validar registros individuales.
    """
    val_lat = (registro.get("decimalLatitude") or "").strip()
    val_lon = (registro.get("decimalLongitude") or "").strip()

    # Solo validamos si AMBOS campos tienen datos
    if val_lat != "" and val_lon != "":
        try:
            lat = float(val_lat)
            lon = float(val_lon)

            # Verificamos si la coordenada cae fuera de las constantes
            if not (LAT_MIN <= lat <= LAT_MAX) or not (LON_MIN <= lon <= LON_MAX):
                return False
        except ValueError:
            # Si el dato no es un número, lo ignoramos
            return True
    return True


def validar_pertenencia_america(path_route, separador, encoding):
    """
    Esta función recorre el dataset y detecta registros que geográficamente no pertenecen a América del Sur.
    Delega la lógica de validación a la función coordenadas_en_america.
    path_route: ruta al dataset analizado.
    separador: delimitador correspondiente al dataset pasado.
    encoding: codificación correspondiente al dataset pasado.
    Retorna: una lista con los occurrenceID de los registros que están fuera de rango.
    """
    ids_fuera_rango = []
    try:
        with open(path_route, "r", encoding=encoding) as file:
            # Usamos DictReader para que el código sea más legible y robusto
            csv_reader = csv.DictReader(file, delimiter=separador)
            
            for fila in csv_reader:
                val_id = fila.get("occurrenceID", "ID_No_Encontrado")
                # Delega la validacion a la funcion intermedia
                if not coordenadas_en_america(fila):
                    ids_fuera_rango.append(val_id)
                        
        return ids_fuera_rango

    except Exception as e:
        print(f"Error en validación 3.H: {e}")
        return []

