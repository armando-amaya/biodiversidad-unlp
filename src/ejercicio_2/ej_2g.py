import csv 
from pathlib import Path


def buscar_columna (path_route, separador, encoding, nombre_columna):
    """
    Esta función cuenta la cantidad de valores distintos presentes en una columna específica.
    Si la columna no existe en el encabezado, informa la situación.
    path_route: ruta al dataset analizado.
    separador: delimitador correspondiente al dataset pasado.
    encoding: codificación correspondiente al dataset pasado.
    nombre_columna: nombre de la columna sobre la cual se quieren contar los valores únicos.
    Retorna: un entero con la cantidad de valores diferentes o None si la columna no existe.
    """
    try: 
        with open (path_route,"r", encoding=encoding) as file:
            csv_reader = csv.reader (file, delimiter=separador)

            #me quedo con la primer fila para encontrar el indice de mi columna requerida
            encabezado = next (csv_reader)
            if nombre_columna in encabezado: 
                #si esta guardo el indice (numero)
                indice = encabezado.index(nombre_columna)
            else: 
                # si no esta, informo la situacion y corto 
                print (f"el nombre de la columna {nombre_columna} no se encontró")
                return None 

            #creo conjunto sin repetidos para luego guardar 
            conjunto_unico = set()

            #recorro el resto de las filas 
            for fila in csv_reader: 
                #me quedo con el dato de la columna que me importa solo
                dato= fila[indice]
                #lo agrego al conjunto que ignora duplicados 
                conjunto_unico.add (dato)
            #devuelvo cantidad de unicos 
            return len (conjunto_unico)
            
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None