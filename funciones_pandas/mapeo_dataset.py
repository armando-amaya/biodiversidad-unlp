import streamlit as st
import pandas as pd

from src.ejercicio_3.ej_3a import validar_registro
from src.ejercicio_3.ej_3b import coordenadas_incompletas

def son_coordenadas_validas(fila):
    """Esta función reutiliza el ejercicio de 3.A y 3.B para verificar
    que las coordenadas están completas y se encuentran en un rango válido.
    fila: fila del dataframe/ data set / serie
    retorna un booleano dependiendo de las validaciones
    """
    # Convertimos cada fila a registro dado que las funciones reciben registros
    try:
        registro = fila.to_dict()
        # verificamos si existen ambas coordenadas
        if coordenadas_incompletas(registro):
            return False

        # verificamos que las coordenadas estén en rango
        if not validar_registro(registro):
            return False
        
        return True
    
    except Exception:
        return False

