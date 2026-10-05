import csv
from pathlib import Path 
from src.ejercicio_5.ej_5b import actualizar_registros
# Importamos las funciones para el 7.D
from src.ejercicio_7.registro import crear_linea_log, registrar_en_archivo

"""
La funcion toma la ruta del datasetm el separador, encoding, el valor del id de la fila, un diccionario con campos y valores,
el nombre de salida del archivo y la carpeta de salida.
Actualiza el dataset ingresado y guarda la nueva copia en la carpeta asignada
"""
def actualizar_multiples_campos(path_ruta, separador, encoding, id_valor, campos_y_valores, nombre_salida, carpeta_salida):
    registros_afectados = 0
    nombre_dataset = path_ruta.name
    
    try:
        with open(path_ruta, 'r', encoding=encoding) as archivo:
            lector = csv.reader(archivo, delimiter=separador)
            encabezado = next(lector)
            
            # Buscamos los índices de los campos solicitados en el diccionario
            indices = {campo: encabezado.index(campo) for campo in campos_y_valores}
            
            datos_actualizados = [encabezado]
            
            for fila in lector:
                # Si el ID coincide (asumiendo que está en la columna 0)
                if fila[0] == str(id_valor):
                    # Actualizamos todos los campos del diccionario en esta fila
                    for campo, nuevo_valor in campos_y_valores.items():
                        fila[indices[campo]] = str(nuevo_valor)
                    registros_afectados += 1
                datos_actualizados.append(fila)

        # Configuración de la ruta de salida
        carpeta_destino = Path(carpeta_salida)
        carpeta_destino.mkdir(exist_ok=True)
        path_destino = carpeta_destino / (nombre_salida + path_ruta.suffix)

        with open(path_destino, 'w', encoding=encoding, newline='') as f_out:
            escritor = csv.writer(f_out, delimiter=separador)
            escritor.writerows(datos_actualizados)

        #CUMPLO CON REGISTRO UNICO (varios update)
        # Registramos una sola vez la operación "UPDATE" para este ID
        linea_ok = crear_linea_log(nombre_dataset, "UPDATE", registros_afectados, "OK")
        registrar_en_archivo(linea_ok)
        
        return f"Actualización múltiple exitosa. Archivo guardado en {carpeta_salida}"

    except Exception as e:
        # Cumplo con el 7.F (incluir error)
        linea_err = crear_linea_log(nombre_dataset, "UPDATE", 0, "ERROR")
        registrar_en_archivo(linea_err)
        return f"Error en actualización múltiple: {e}"
        