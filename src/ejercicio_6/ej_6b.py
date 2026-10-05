from pathlib import Path
import csv
from rutas import PROCESSED_DATASETS
#Importo funciones del ejercicio 7 
from src.ejercicio_7.registro import crear_linea_log, registrar_en_archivo

"""
La funcion toma la ruta original del dataset, separador, encoding, nombre de columna y valores a eliminar 
en formato lista.
Devuelve un archivo sin los registros que contenian esos valores
"""

def eliminar_registros_por_lista(ruta_original, separador, encoding, nombre_columna, valores_a_eliminar):
    #nombre_salida = ruta_original.parent.name.lower() + "-procesado" + ruta_original.suffix
    #ruta_salida = ruta_original.parents[2] / "processed_datasets" / nombre_salida
    # definimos ruta de salida
    nombre_salida = f"{ruta_original.stem.lower()}_procesado{ruta_original.suffix}"
    ruta_salida = PROCESSED_DATASETS / nombre_salida
    eliminados = 0
    try: 
        with open(ruta_original, "r", encoding=encoding) as entrada:
            with open(ruta_salida, "w", encoding=encoding) as salida:
                lector = csv.reader(entrada, delimiter=separador)
                escritor = csv.writer(salida, delimiter=separador)
    
                encabezado = next(lector)
                escritor.writerow(encabezado)
    
                if nombre_columna not in encabezado:
                    # registramos si la linea no existe
                    linea_error = crear_linea_log(ruta_original.name, "DELETE", 0, "ERROR")
                    registrar_en_archivo(linea_error)
                    raise ValueError(f"La columna '{nombre_columna}' no existe")
    
                col_pos = encabezado.index(nombre_columna)
    
                for fila in lector:
                    if fila[col_pos] in valores_a_eliminar:
                        eliminados += 1
                    else:
                        escritor.writerow(fila)
    
        print(f"Se eliminaron {eliminados} registros. Guardado en processed_datasets")
        # registramos el exito
        linea_exito = crear_linea_log(ruta_original.name, "DELETE", eliminados, "OK")
        registrar_en_archivo(linea_exito)
        return True
        
    except Exception as e: 
    #nueva linea de error (por cualquier otro fallo tecnico) 7.F
        linea_error= crear_linea_log(ruta_original.name, "DELETE", 0, "ERROR")
        registrar_en_archivo(linea_error)
        print(f"Error al procesar la lista: {e}")
        return False