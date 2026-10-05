
from src.ejercicio_3.ej_3a import validar_registro as validar_coordenadas_rango
from src.ejercicio_3.ej_3b import coordenadas_incompletas
from src.ejercicio_3.ej_3c import validar_fecha_registro
from src.ejercicio_3.ej_3h import coordenadas_en_america
from src.ejercicio_3.ej_3e import validar_registro
from src.ejercicio_3.ej_3f import incertidumbre_invalida_fila
from src.CodigosPaises import CODES

"""La función toma un registro (diccionario con claves nombres de columnas) y el formato
de las fechas a evaluar y devuelve si el registro es válido o no: True/False (como para insertarlo en un
dataset)"""

def validar_registro_completo(reg, formato_fecha="%Y-%m-%d"):  # registro es un diccionario creado para insertar a un dataset

    es_valida = True

    # Validacion 3a: coordenadas fuera de rango
    if not validar_coordenadas_rango(reg):
        es_valida = False


    # Validacion 3c: formato de fecha
    if not validar_fecha_registro(reg, "eventDate", formato_fecha):
        es_valida = False
    
    #Validacion 3e: codigo de pais
    if validar_registro(reg, "countryCode", CODES) is not None:
            es_valida = False
    
    # Validacion 3h: coordenadas pertenecen a América
    if not coordenadas_en_america(reg):
        es_valida = False

    if not incertidumbre_invalida_fila(reg, "coodinateUncertaintyInMeters") == None:
        es_valida = False
    return es_valida