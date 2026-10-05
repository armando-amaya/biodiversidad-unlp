import sys
from pathlib import Path
import csv

# Armamos importacion de rutas
sys.path.append(str(Path(__file__).resolve().parent.parent))
from rutas import PROCESSED_DATASETS

from src.ejercicio_2.ej_2b import obtener_columnas
from src.ejercicio_4.ej_4b import generar_registro_vacio
from src.ejercicio_4.ej_4c import validar_registro_completo
from src.ejercicio_4.ej_4d import construir_fila

# Importo funciones del ejercicio 7 para el log (Ejercicio 7.C)
from src.ejercicio_7.registro import crear_linea_log, registrar_en_archivo

def ingresar_registro_por_teclado(registro_none):
    """
    Esta función recibe un registro con sus campos inicializados en None,
    hace una copia y la carga con datos ingresados por teclado.
    registro_none: dict, con columnas inicializadas en None (4.B).
    Retorna: un diccionario con los valores ingresados por el usuario.
    """
    # trabajamos con una copia para no modificar el original
    registro = registro_none.copy()
    print("Ingrese los datos:")
    for encabezado in registro:
        valor = input(f"{encabezado}: ").strip()
        if valor == "":
            continue
        registro[encabezado] = valor

    return registro

def escribir_insercion_registro(ruta_original, separador, encoding, registro_none, registro_cargado):
    """
    Reutiliza la lógica común de inserción para escribir el archivo y registrar el log.
    Recibe el registro ya cargado y validado desde otra interfaz.
    Retorna el registro final insertado o None si hubo errores.
    """
    registros_afectados = 0
    nombre_dataset = ruta_original.name

    try:
        columnas = obtener_columnas(ruta_original, separador, encoding)
        registro_final = construir_fila(registro_none, registro_cargado, ruta_original)

        archivo_salida = f"{ruta_original.parent.name.lower()}_insercion_registro.csv"
        ruta_salida = PROCESSED_DATASETS / archivo_salida

        with open(ruta_original, "r", encoding=encoding) as archivo_og:
            with open(ruta_salida, "w", encoding=encoding, newline="") as archivo_nv:

                lector = csv.DictReader(archivo_og, delimiter=separador)
                escritor = csv.DictWriter(archivo_nv, fieldnames=columnas, delimiter=separador)

                escritor.writeheader()

                for fila in lector:
                    escritor.writerow(fila)

                escritor.writerow(registro_final)
                registros_afectados += 1

        print("Inserción exitosa")
        linea_ok = crear_linea_log(nombre_dataset, "INSERT", registros_afectados, "OK")
        registrar_en_archivo(linea_ok)
        return registro_final

    except Exception as e:
        print(f"Error inesperado: {e}")
        linea_fail = crear_linea_log(nombre_dataset, "INSERT", 0, "ERROR")
        registrar_en_archivo(linea_fail)
        return None

def insertar_registro(ruta_original, separador, encoding, registro_none, formato_fecha="%Y-%m-%d"):        
    """
    Esta función pide los datos por teclado, luego lo valida y construye
    una fila con ID, luego copia el dataset original para mantener estructura
    y agrega el nuevo registro ingresado.
    
    ruta_original: path, ruta al dataset original.
    separador: str, delimitador correspondiente al dataset.
    encoding: str, codificacion del dataset.
    registro_none: dict, registro con sus columnaas inicializadas en None(4.B).
    formato_fecha: str, fortmato esperado para 4.C.
    Retorna: None. Informa el éxito o error de la operación por consola y en el log.
    """
    # Variables para el log (7.C)
    registros_afectados = 0
    nombre_dataset = ruta_original.name

    try:
        # Pedimos los datos por teclado
        registro_cargado = ingresar_registro_por_teclado(registro_none)

        # Validamos que esté correcto con 4.C
        es_valido = validar_registro_completo(registro_cargado, formato_fecha="%Y-%m-%d")

        if not es_valido:
            print("\n El registro no es válido. Revisar campos ingresados")
            # Registro de error por validación fallida (7.C)
            linea_err = crear_linea_log(nombre_dataset, "INSERT", 0, "ERROR")
            registrar_en_archivo(linea_err)
            return None

        # obtenemos columnas para reescribir el archivo
        # columnas = obtener_columnas(ruta_original, separador, encoding)

        # Generamos la fila con ID, 4.D
        # registro_final = construir_fila(registro_none, registro_cargado, ruta_original)

        # definimos ruta de salida
        # archivo_salida = f"{ruta_original.parent.name.lower()}_insercion_registro.csv"
        # ruta_salida = PROCESSED_DATASETS / archivo_salida

        # Leemos y escribimos el dataset original en nuevo archivo
        # with open(ruta_original, "r", encoding=encoding) as archivo_og:
        #     with open(ruta_salida, "w", encoding=encoding, newline="") as archivo_nv:

        #         lector   = csv.DictReader(archivo_og, delimiter=separador)
        #         escritor = csv.DictWriter(archivo_nv, fieldnames=columnas, delimiter=separador)

        #         escritor.writeheader()        # escribimos los encabezados

        #         for fila in lector:
        #             escritor.writerow(fila)
        #
        #         # agregamos la nueva fila
        #         escritor.writerow(registro_final)
        #         registros_afectados += 1 # Contador para el log (7.C)

        # informamos el exito de la incersión
        # print("Inserción exitosa")

        # Registro exitoso en el log (7.C)
        # linea_ok = crear_linea_log(nombre_dataset, "INSERT", registros_afectados, "OK")
        # registrar_en_archivo(linea_ok)
        escribir_insercion_registro(ruta_original, separador, encoding, registro_none, registro_cargado)

    except Exception as e:
        # Registro de error generico 7.F
        print(f"Error inesperado: {e}")
        linea_fail = crear_linea_log(nombre_dataset, "INSERT", 0, "ERROR")
        registrar_en_archivo(linea_fail)
        return None