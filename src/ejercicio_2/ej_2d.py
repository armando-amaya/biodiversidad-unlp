import csv 
from pathlib import Path

def cantidad_de_registros (path_route, separador, encoding):
    """
    Esta función cuenta la cantidad total de registros (filas de datos) del dataset.
    Se salta la cabecera y utiliza un iterador para no saturar la memoria.
    path_route: ruta al dataset original o procesado.
    separador: delimitador correspondiente al dataset pasado.
    encoding: codificación correspondiente al dataset pasado.
    Retorna: un entero con la cantidad total de registros o 0 si ocurre un error.
    """
    try: 
        with open (path_route, "r", encoding= encoding) as file:  
            csv_reader = csv.reader (file, delimiter=separador)
    
            #me salteo el nombre de las columnas que no aportan nada 
            next (csv_reader)
    
            #inicializo en 0 el contador de registros.
            cantidad_registros = 0 
    
            #Recorro fila por fila, con iteradores para no cargar la memoria y saturar
            for fila in csv_reader:
                cantidad_registros +=1
            #devuelvo la cantidad de registros contados para poder comparar 
            return cantidad_registros
       
        #preveo excepciones o posibles 
    except Exception as e:
        print(f"Error al contar: {e}")
        return 0