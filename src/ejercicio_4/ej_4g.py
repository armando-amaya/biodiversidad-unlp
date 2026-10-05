import sys
from pathlib import Path
import csv

sys.path.append(str(Path(__file__).resolve().parent.parent))
from rutas import PROCESSED_DATASETS

from ejercicio_2.ej_2b import obtener_columnas
from ejercicio_4.ej_4b import generar_registro_vacio
from ejercicio_4.ej_4c import validar_registro_completo
from ejercicio_4.ej_4d import construir_fila
from ejercicio_4.ej_4f import ingresar_registro_por_teclado

# Importo funciones del ejercicio 7 para el log (Ejercicio 7.C)
from src.ejercicio_7.registro import crear_linea_log, registrar_en_archivo

def insertar_multiples_registros(ruta_original, separador, encoding, columnas, formato_fecha="%Y-%m-%d"):
    """
    Esta función pide registros por teclado hasta que el usuario decida parar,
    valida cada uno, los acumula y los agrega al dataset original.

    ruta_original: path, ruta al dataset original.
    separador: str, delimitador correspondiente al dataset.
    encoding: str, codificación del dataset.
    columnas: list, columnas del dataset obtenidas con (2.B).
    formato_fecha: str, formato esperado para eventDate.
    Retorna: una lista con los registros válidos insertados o None si hubo errores.
    """
    # Variables para el log (7.C)
    registros_afectados = 0
    nombre_dataset = ruta_original.name

    try:
        # creamos una lista para ir guardando los registros válidos
        registros_validos = []
        cant_registro = 1
        columnas = obtener_columnas(ruta_original, separador, encoding)

        # generamos un bucle para el múltiple ingreso de registros
        while True:
            print(f"\n{'='*50}")
            print("\nIngrese su registro:")

            # generamos un registro vacío para cada iteracion
            registro_none = generar_registro_vacio(columnas)
            registro_cargado = ingresar_registro_por_teclado(registro_none)

            # validamos el nuevo registro
            es_valido = validar_registro_completo(registro_cargado, formato_fecha)

            if es_valido:
                registro_final = construir_fila(registro_none, registro_cargado, ruta_original)
                registros_validos.append(registro_final)
                print("\nRegistro válido.")
                print(f"\nRegistro ingresado #{cant_registro}")
            else:
                print("Registro inválido. Revisar campos ingresados")

            cant_registro += 1

            # preguntamos si se quiere seguir agregando regisros
            continuar = input("\n¿Deseás ingresar otro registro? (si/no): ").strip().lower()
            if continuar != "si":
                break

        # agregamos una condición por si no se ingresó ningun registro y así no se carga un archivo vacío.
        if not registros_validos:
            print("No se escribió ningún archivo/ ningún registro fue válido.")
            # Registro de error por falta de datos válidos (7.C)
            linea_err = crear_linea_log(nombre_dataset, "INSERT", 0, "ERROR")
            registrar_en_archivo(linea_err)
            return None

        ruta_salida = PROCESSED_DATASETS / f"{ruta_original.parent.name.lower()}_insercion_multiple.csv"

        with open(ruta_original, "r", encoding=encoding) as archivo_og:
            with open(ruta_salida, "w", encoding=encoding, newline="") as archivo_nv:

                lector = csv.DictReader(archivo_og, delimiter=separador)
                escritor = csv.DictWriter(archivo_nv, fieldnames=columnas, delimiter=separador)

                escritor.writeheader()

                for fila in lector:
                    escritor.writerow(fila)

                # iteramos lista con regsitros nuevos y agregamos al dataset
                for registro_final in registros_validos:
                    escritor.writerow(registro_final)
                    registros_afectados += 1 # Contador para el log (7.C)

        print(f"Incersión de {registros_afectados} registros exitosa")

        # Registro exitoso en el log (7.C)
        linea_ok = crear_linea_log(nombre_dataset, "INSERT", registros_afectados, "OK")
        registrar_en_archivo(linea_ok)
        
        return registros_validos

    except Exception as e:
        # Registro de error generico 7.F
        print(f"Error inesperado: {e}")
        linea_fail = crear_linea_log(nombre_dataset, "INSERT", 0, "ERROR")
        registrar_en_archivo(linea_fail)
        return None