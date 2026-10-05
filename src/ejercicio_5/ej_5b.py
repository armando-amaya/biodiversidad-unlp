from pathlib import Path
import csv
import os
#Importo funciones del ejercicio 7 
from src.ejercicio_7.registro import crear_linea_log, registrar_en_archivo


def actualizar_registros(path_ruta, separador, encoding, id_valor, columna_nombre, valor_nuevo):
    """
    Esta función actualiza un campo en el registro correspondiente. 
    path_ruta: ruta a dataset pasado.
    separador: delimitador correspondiente al dataset pasado.
    encoding: codificación correspondiente al dataset pasado. 
    id_valor: identificador de registro.
    columna_nombre: columna a actualizar. 
    valor_nuevo: valor a cambiar.
    """ 

#Abro el archivo   
    registros_afectados = 0
    nombre_dataset = path_ruta.name #para usar en el log
    try:
            with open(path_ruta, 'r', encoding=encoding) as archivo:
                lector = csv.reader(archivo, delimiter=separador)
                encabezado = next(lector)
                #Creo una lista para guardar las modificacciones 
                datos_actualizados = []
                #Buscamos el índice de la columna que queremos cambiar
                try:
                    indice_a_modificar = encabezado.index(columna_nombre)
                except ValueError:
                    #7.F Registrar error si la columna no existe
                    linea_err = crear_linea_log (nombre_dataset, "UPDATE", 0 , "ERROR")
                    registrar_en_archivo (linea_err)
                    return f"Error: La columna {columna_nombre} no existe."
                    
                #Guardo el encabezado
                datos_actualizados.append(encabezado)
                #Recorro las filas
                for fila in lector:
                #Si el primer elemento (ID) coincide con lo que buscamos, actualizamos y agregaos
                    if fila[0] == str(id_valor):
                        fila[indice_a_modificar] = str(valor_nuevo)
                        #7.D contador para el log 
                        registros_afectados += 1 
                    datos_actualizados.append(fila)
                    
            # Creo la ruta de destino
            carpeta_destino = Path(carpeta_salida)
            # Nos aseguramos de que la carpeta exista
            carpeta_destino.mkdir(exist_ok=True)
            #El archivo se llamará igual que el original pero en la otra carpeta
            path_destino = carpeta_destino / (nombre_salida + path_ruta.suffix)
        
            #Escribo en el nuevo archivo y guardo
            with open(path_destino, 'w', encoding=encoding, newline='') as archivo_salida:
                escritor = csv.writer(archivo_salida, delimiter=separador)
                # Guardamos todas las filas juntas
                escritor.writerows(datos_actualizados)
            #7.D Registro exitoso
            linea_ok = crear_linea_log (nombre_dataset, "UPDATE", registros_afectados, "OK")
            registrar_en_archivo (linea_ok)
            return f"Archivo guardado exitosamente en processed_datasets"
    
    except Exception as e: 
        #7.F Registro error generico 
        linea_fail = crear_linea_log(nombre_dataset, "UPDATE", 0, "ERROR")
        registrar_en_archivo(linea_fail)
        return f"Error inesperado: {e}"
