
from pathlib import Path 
from src.ejercicio_5.ej_5b import actualizar_registros
from src.ejercicio_4.ej_4c import validar_registro_completo

#actualizar_registros(path_ruta, separador, encoding, id_valor, columna_nombre, valor_nuevo, nombre_salida, carpeta_salida)


#Funcion 5c transformada
def validar_actualizar_multiples_campos(path_ruta, separador, encoding, id_valor, campos_y_valores, nombre_salida, carpeta_salida): 
    if validar_registro_completo(campos_y_valores, formato_fecha="%Y-%m-%d"):
        print('el registro es válido')
        # Definimos dónde se guardará el archivo procesado
        carpeta_destino = Path(carpeta_salida)
        path_destino = carpeta_destino / (nombre_salida + path_ruta.suffix)
        
        # La primera vez, el archivo de entrada es el original
        archivo_a_leer = path_ruta

        for campo in campos_y_valores:
            # Llamamos a actualizar_registros
            resultado = actualizar_registros(archivo_a_leer, separador, encoding, id_valor, campo, campos_y_valores[campo], nombre_salida, carpeta_salida)
            
            # IMPORTANTE: Después de la primera edición exitosa, 
            # empezamos a leer del archivo que estamos creando (el de salida)
            if "exitosamente" in resultado:
                archivo_a_leer = path_destino
                
        return "Proceso múltiple finalizado"
    else: 
        print('el registro que desea ingresar no es válido')


from src.ejercicio_3.ej_3a import validar_registro as validar_coordenadas_rango
from src.ejercicio_3.ej_3b import coordenadas_incompletas
from src.ejercicio_3.ej_3c import validar_fecha_registro
from src.ejercicio_3.ej_3h import coordenadas_en_america
from src.ejercicio_3.ej_3f import incertidumbre_invalida_fila




from datetime import datetime


COLUMNAS_FECHA = {"eventDate", "verbatimEventDate", "modified", "dateIdentified", "lastInterpreted"}
FORMATOS_FECHA = ["%Y-%m-%d", "%Y-%m-%dT%H:%M%z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z"]

def _intenta(valor, fmt):
    try:
        datetime.strptime(valor, fmt)
        return True
    except ValueError:
        return False

def fecha_valida(valor):
    valor_normalizado = valor.strip().replace("Z", "+00:00")
    return any(_intenta(valor_normalizado, fmt) for fmt in FORMATOS_FECHA)


COLUMNAS_COORDENADAS = {"latitudeDecimal", "longitudeDecimal", "decimalLatitude", "decimalLongitude"}
COLUMNAS_INCERTIDUMBRE = {"coordinateUncertaintyInMeters"}

def validar_campo_individual(columna, valor):

    if columna in COLUMNAS_FECHA:
        resultado = fecha_valida(valor)
        print(f"{columna} = '{valor}' -> {'valido' if resultado else 'invalido'}")
        return resultado

    if columna in {"latitudeDecimal", "decimalLatitude"}:
        try:
            resultado = -90 <= float(valor) <= 90
        except ValueError:
            resultado = False
        print(f"{columna} = '{valor}' -> {'valido' if resultado else 'invalido'}")
        return resultado

    if columna in {"longitudeDecimal", "decimalLongitude"}:
        try:
            resultado = -180 <= float(valor) <= 180
        except ValueError:
            resultado = False
        print(f"{columna} = '{valor}' -> {'valido' if resultado else 'invalido'}")
        return resultado

    if columna in COLUMNAS_INCERTIDUMBRE:
        try:
            resultado = float(valor) > 0
        except ValueError:
            resultado = False
        print(f"{columna} = '{valor}' -> {'valido' if resultado else 'invalido'}")
        return resultado

    print(f"{columna} = '{valor}' -> sin validacion especifica, se acepta")
    return True

#validacion para el 5b
from src.ejercicio_5.ej_5b import actualizar_registros

def validar_y_actualizar(path_ruta, separador, encoding, id_valor, columna_nombre, valor_nuevo, nombre_salida, carpeta_salida):
    if validar_campo_individual(columna_nombre, valor_nuevo):
        return actualizar_registros(path_ruta, separador, encoding, id_valor, columna_nombre, valor_nuevo, nombre_salida, carpeta_salida)
    else:
        return f"No se actualizó: el valor '{valor_nuevo}' no es válido para la columna '{columna_nombre}'"

