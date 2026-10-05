import csv

#Importo funciones del ejercicio 7 
from src.ejercicio_7.registro import crear_linea_log, registrar_en_archivo

def cumple_condicion(valor_celda, condicion, valor):
    """
    Evalua si un valor cumple una condición dada.
    Retorna: True si el valor de la celda cumple la condición respecto al valor dado, 
    False en caso contrario o ante errores de tipo/conversión.
    valor_celda: valor a evaluar.
    condicion: operador de comparación ("==", "!=", ">", ">=", "<", "<=").
    valor: valor contra el cual se compara.
"""
    try:
        if condicion == "==": return valor_celda == valor
        elif condicion == "!=": return valor_celda != valor
        elif condicion == ">":  return float(valor_celda) > float(valor)
        elif condicion == ">=": return float(valor_celda) >= float(valor)
        elif condicion == "<":  return float(valor_celda) < float(valor)
        elif condicion == "<=": return float(valor_celda) <= float(valor)
        else: raise ValueError("Condición inválida")
    except (ValueError, TypeError):
        return False

def eliminar_registros(ruta_csv, columna, condicion, valor, ruta_salida, delimiter=","):


    """
    Elimina registros de un archivo según una condición aplicada a una columna.
    Retorna: Genera un nuevo archivo CSV sin los registros que cumplen la condición y registra la operación en un log.
    ruta_csv: ruta al archivo CSV de entrada.
    columna: columna sobre la cual se aplica la condición.
    condicion: operador de comparación ("==", "!=", ">", ">=", "<", "<=").
    valor: valor contra el cual se compara.
    ruta_salida: ruta donde se guarda el archivo resultante.
    delimiter: delimitador del archivo (por defecto ",").
"""
    eliminados = 0 # agrego variable contadora para el log
    try: 
        with ruta_csv.open(encoding="utf-8") as archiv_entrada, ruta_salida.open("w", encoding="utf-8", newline="") as archiv_salida:
            lector = csv.DictReader(archiv_entrada, delimiter=delimiter)
            
            if columna not in lector.fieldnames:
                # registramos el error
                linea_error = crear_linea_log(ruta_csv.name, "DELETE", 0, estado="ERROR")
                registrar_en_archivo(linea_error)
    
                raise ValueError(f"La columna '{columna}' no existe")
    
            escritor = csv.DictWriter(archiv_salida, fieldnames=lector.fieldnames, delimiter=delimiter)
            escritor.writeheader()
    
            for fila in lector:
                if not cumple_condicion(fila.get(columna), condicion, valor):
                    escritor.writerow(fila)
                else:
                    eliminados += 1
    
        linea_exito = crear_linea_log(ruta_csv.name, "DELETE", eliminados, "OK")
        registrar_en_archivo(linea_exito)
        
    except Exception as e:
        # nueva linea de error (por cualquier otro fallo tecnico) 7.F
        linea_error_gen = crear_linea_log(ruta_csv.name, "DELETE", 0, estado="ERROR")
        registrar_en_archivo(linea_error_gen)
        print(f"Ocurrió un error inesperado: {e}")