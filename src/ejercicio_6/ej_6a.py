import sys
from pathlib import Path
import csv

#Importo funciones del ejercicio 7 
from src.ejercicio_7.registro import crear_linea_log, registrar_en_archivo

# Armamos importacion de rutas
sys.path.append(str(Path(__file__).resolve().parent.parent))
from rutas import PROCESSED_DATASETS

def elimino_registro_por_id(ruta_original, separador, encoding, nombre_columna, id_para_eliminar):
    """
    Esta función eliminia un registro del dataset dado un identificador.
    Si no se encuentra informa el error.
    ruta_original: ruta a dataset original.
    separador: delimitador correspondiente al dataset pasado.
    encoding: codificación correspondiente al dataset pasado.
    nombre_ columna: columna identificadora del dataset (puede tener distinto nombre)
    id_para_eliminar: valor del id a eliminar 
    Retorna: True si la eliminación fue exitosa, False si hubo algún error.
    """
    # definimos ruta de salida
    archivo_salida = f"{ruta_original.stem.lower()}_con_id_eliminado.csv"
    ruta_salida = PROCESSED_DATASETS / archivo_salida

    try: 
        # Leemos el encabezado primero para evitar errores
        with open(ruta_original, "r", encoding=encoding) as archivo_txt:
            encabezado = next(csv.reader(archivo_txt, delimiter=separador))
    
        # Validás antes de abrir el archivo de salida
        if nombre_columna not in encabezado:
    
            # registramos el error de la operacion
            linea_error = crear_linea_log(ruta_original.name, "DELETE", 0, estado="ERROR")
            registrar_en_archivo(linea_error)
    
            raise ValueError(f"La columna '{nombre_columna}' no existe")
    
        # incializamos un variable para controlar si existe o no el valor del id
        encontrado = False
    
        # leemos el dataset original y escribimos el nuevo
        with open(ruta_original, "r", encoding=encoding) as archivo_original:
            with open(ruta_salida, "w", encoding=encoding) as archivo_nuevo:
    
                lector = csv.reader(archivo_original, delimiter=separador)
                escritor = csv.writer(archivo_nuevo, delimiter=separador)
    
                # guardamos el encabezado
                encabezado = next(lector)
                # escribimos el encabezado en el archivo nuevo
                escritor.writerow(encabezado)
    
                # buscamos el indice de la columna pasada por parametro
                col_pos = encabezado.index(nombre_columna)
    
                # recorremos y filtramos 
                for fila in lector:
                    if fila[col_pos] == str(id_para_eliminar):
                        encontrado = True
                        # nos salteamos la fila si es que encontramos el valor a eliminar
                        continue
                    else:
                        escritor.writerow(fila)
    
        # preguntamos si el id existe o no
        if not encontrado:
            print(f"Error: no se encontró ningún registro con el id {id_para_eliminar}")
            # registramos el error si no se encontró columna con id
            linea_error = crear_linea_log(ruta_original.name, "DELETE", 0 , "ERROR")
            registrar_en_archivo(linea_error)
            return False
        else:
            print("Se elimnó correctamente")
            linea_exito = crear_linea_log(ruta_original.name, "DELETE", 1, "OK")
            registrar_en_archivo(linea_exito)
            return True
            
    except Exception as e: 
        #  nueva linea de error (por cualquier otro fallo tecnico) 7.F
        linea_fallo = crear_linea_log(ruta_original.name, "DELETE", 0, "ERROR")
        registrar_en_archivo(linea_fallo)
        print(f"Error inesperado al procesar: {e}")
        return False
