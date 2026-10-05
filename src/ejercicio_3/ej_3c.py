from datetime import datetime
import os
import sys
import csv
from pathlib import Path

current = Path(os.path.abspath(""))
"""
Toma una fecha, un formato y valida si una fecha cumple con el formato indicado y NO es posterior
a la fecha y hora actual del sistema.
"""
def validar_fecha(fecha, formato):

    if fecha is None or fecha == "":
        return True
    
    formatos = [formato] if isinstance(formato, str) else formato
    
    for fmt in formatos:
        try:
            # 1. Convertimos el texto a objeto datetime
            fecha_objeto = datetime.strptime(fecha, fmt)
            
            # 2. Si el formato tiene zona horaria (%z), comparamos con el ahora con zona horaria.
            # Si no, comparamos de forma ingenua (naive).
            if fecha_objeto.tzinfo is not None:
                ahora = datetime.now(fecha_objeto.tzinfo)
            else:
                ahora = datetime.now()
                
            # 3. Corroboramos que no sea posterior al momento actual
            if fecha_objeto > ahora:
                return False  # Es una fecha del futuro, no es válida
                
            return True
        except ValueError:
            continue
    return False


def validar_fecha_registro(registro: dict, columna, formato) -> bool:
    if columna in registro:
        return validar_fecha(registro[columna], formato)
    return True
"""
 recorrer_y_validar recorre el dataset e identifica los valores de fecha no válidos utilizando
    una función lambda para modularizar el filtrado de filas erróneas.
"""

def recorrer_y_validar(columna, ruta, delimitador, formato):

    with open(ruta, mode='r', encoding='utf-8') as archivo_csv:
        lector = list(csv.DictReader(archivo_csv, delimiter=delimitador))
        
        # MODULARIZACIÓN CON LAMBDA:
        # Filtramos las filas que NO pasan la validación de registro
        filas_erroneas = filter(lambda fila: not validar_fecha_registro(fila, columna, formato), lector)
        
        # Mapeamos para quedarnos únicamente con el string de la fecha conflictiva
        fechas_erroneas = [fila[columna] for fila in filas_erroneas]
        
    return fechas_erroneas