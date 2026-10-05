import csv
from pathlib import Path

# Ruta según tu estructura de carpetas
#file_route1 = Path('..') / '..' / '..' / 'Datos' / 'xeno-canto' / 'Ocurrencia.txt'
#file_route2 = Path('..') / '..' / '..' / 'Datos' / 'inaturalist' / 'Ocurrencia.csv'
#file_route3 = Path('..') / '..' / '..' / 'raw_datasets' / 'IADIZA' / 'occurrence.txt'

"""se le ingresa la ruta al archivo y devuelve un print de las primeras 10 filas en formato diccionario"""

def imprimir_primeras_filas_dict(ruta, delimitador=","):
        # Carga el archivo linea por linea en formato lectura, como lo pide el ejercicio.
    with open(ruta, mode='r', encoding='utf-8') as archivo_csv:
            #Con DictReader el csv se traduce a un diccionario, con claves de nombres de columnas y los datos de cada fila.
            #el delimeter depende del archivo, puede ser , o \t !
            lector = csv.DictReader(archivo_csv, delimiter=delimitador)

            # fieldnames es una lista con los nombres de las columnas - se imprime para mostrar los campos del archivo
            print("ENCABEZADO DEL ARCHIVO:")
            print("-" * 50)
            print(f"Columnas: {lector.fieldnames}\n")

            # Inicializamos contador para limitar a 10 filas
            contador = 1

            # Iteramos directamente sobre el lector (no usamos next antes)
            for fila in lector:
                if contador > 10:
                    break

                # Formato personalizado para mayor visibilidad
                print(f"--- FILA {contador} ---")
                print(fila)        # Imprimimos el diccionario directamente
                print() 

                contador += 1

            # Mensaje informativo si el archivo tenía más de 10 filas
            if contador > 10:
                print(f"... (mostradas solo las primeras 10 filas de datos)")


#imprimir_primeras_filas_dict(file_route3)


