import csv
from pathlib import Path

from src.ejercicio_3.ej_3a import validar_registro as validar_coordenadas_basico
from src.ejercicio_3.ej_3b import coordenadas_incompletas
from src.ejercicio_3.ej_3c import validar_fecha_registro
from src.ejercicio_3.ej_3d import deteccion_duplicados
from src.ejercicio_3.ej_3e import validar_registro as validar_country_code
from src.ejercicio_3.ej_3f import incertidumbre_invalida_fila


def generar_resumen_calidad(path_ruta, separador, encoding, lista_paises_validos, columnas_fecha, formato_fecha="%Y-%m-%d"):
    """
    Genera un resumen de calidad de datos de un archivo CSV.
    Retorna: tupla (resumen, reporte), donde:
    - resumen: diccionario (registros totales, coordenadas inválidas, fechas inválidas, duplicados, 
    countryCode erróneos, incertidumbre inválida y taxonomía incompleta).
    - reporte: string con el resumen de resultados.
    path_ruta: ruta al archivo CSV.
    separador: delimitador del archivo.
    encoding: codificación del archivo.
    lista_paises_validos: lista de códigos de país válidos.
    columnas_fecha: columnas con fechas a validar.
    formato_fecha: formato esperado de fecha.
"""


    path_ruta = Path(path_ruta)

    resumen = {
        "total_registros": 0,
        "coordenadas_invalidas": 0,
        "fechas_invalidas": 0,
        "duplicados_count": 0,
        "codigos_pais_erroneos": 0,
        "incertidumbre_elevada": 0,
        "taxonomia_incompleta": 0
    }

    # Duplicados (manejo de datasets con distinto ID)
    try:
        total_dup, _ = deteccion_duplicados(path_ruta)
        resumen["duplicados_count"] = total_dup
    except Exception:
        resumen["duplicados_count"] = 0

    with path_ruta.open(encoding=encoding) as archivo:
        lector = csv.DictReader(archivo, delimiter=separador)

        for fila in lector:
            resumen["total_registros"] += 1

            # 3.A + 3.B
            if (not validar_coordenadas_basico(fila)) or coordenadas_incompletas(fila):
                resumen["coordenadas_invalidas"] += 1

            # 3.C
            for col in columnas_fecha:
                if col in fila and not validar_fecha_registro(fila, col, formato_fecha):
                    resumen["fechas_invalidas"] += 1
                    break

            # 3.E
            if validar_country_code(fila, "countryCode", lista_paises_validos) is not None:
                resumen["codigos_pais_erroneos"] += 1

            # 3.F
            if incertidumbre_invalida_fila(fila, "coordinateUncertaintyInMeters") is not None:
                resumen["incertidumbre_elevada"] += 1

            # Taxonomía
            campos_taxo = ["kingdom", "genus", "scientificName"]
            if any(not fila.get(c) or fila.get(c).strip() == "" for c in campos_taxo):
                resumen["taxonomia_incompleta"] += 1

    reporte = f"""
REPORTE DE CALIDAD
==================================================
Archivo: {path_ruta.name}
Total registros: {resumen['total_registros']}

Coordenadas inválidas:        {resumen['coordenadas_invalidas']}
Fechas inválidas:             {resumen['fechas_invalidas']}
Duplicados:                   {resumen['duplicados_count']}
CountryCode inválidos:        {resumen['codigos_pais_erroneos']}
Incertidumbre inválida:       {resumen['incertidumbre_elevada']}
Taxonomía incompleta:         {resumen['taxonomia_incompleta']}
==================================================
"""

    return resumen, reporte