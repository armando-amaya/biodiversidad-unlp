import datetime 
import csv
from pathlib import Path
import os 

#ejercicio 7A 
def obtener_fecha_actual():
    """
    Utiliza la librería datetime para generar un formato legible (Año-Mes-Día Hora:Min:Seg).
    Retorna: un string con la fecha y hora formateada.
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def crear_linea_log(nombre_dataset, tipo_operacion, cantidad_registros, estado="OK"):
    """
    Esta función construye la cadena de texto con el formato pedido por la cátedra.
    Une la fecha, el dataset, el tipo de acción y el resultado.
    nombre_dataset: nombre del archivo analizado (ej. iadiza).
    tipo_operacion: acción realizada (INSERT, UPDATE, DELETE).
    cantidad_registros: número de filas afectadas.
    estado: indica si la operación fue exitosa o fallida (ERROR).
    Retorna: un string listo para ser escrito en el archivo de logs.
    """
    # Llamo funcion anterior para la fecha 
    fecha = obtener_fecha_actual() 
    #Armo el formato mostrado en la consigna 
    linea = f"{fecha} | {nombre_dataset} | {tipo_operacion} | {cantidad_registros} registros"
    
    if estado == "ERROR":
        linea += " | ERROR"
        
    return linea


#ejercicio 7B
def registrar_en_archivo(linea_log):
    """
    Esta función guarda la operación en el archivo físico 'operations.log'.
    Se asegura de crear la carpeta 'logs' si no existe y no sobrescribe el contenido previo.
    linea_log: la cadena de texto generada con los datos de la operación.
    """
    # Busco la carpeta del archivo actual
    directorio_actual = Path(__file__).parent
    
    # Subo dos niveles para llegar a la raíz y luego bajo a 'logs'
    ruta_log = directorio_actual.parent.parent / "logs" / "operations.log"
    
    # Nos aseguramos de que la carpeta exista
    ruta_log.parent.mkdir(parents=True, exist_ok=True)
    
    with open(ruta_log, "a", encoding="utf-8") as f:
        f.write(linea_log + "\n")