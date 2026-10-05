import csv

"""
Esta función recibe la ruta del dataset y un delimitador e identifica (y devuelve) 
las columnas (lista de nombres de columnas) cuyo contenido sea completamente nulo en
todos los registros.
"""

def identificando_columnas_nulas(ruta, separador=","):

    with open(ruta, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo, delimiter=separador)
        titulos = lector.fieldnames  # nombres de columnas

        # creamos un conjunto para llevar registro de columnas que contengan
        # al menos un valor
        columnas_no_nulas = set()

        # recoremo
        for fila in lector:
            for columna in titulos:
                valor = fila[columna]
                # preguntamos si no está vacío y comparamos al aplicar .strip
                if valor and valor.strip():
                    columnas_no_nulas.add(columna)

        # separamos columnas nulas de las que no aparecieron en el conjunto
        columnas_nulas = [c for c in titulos if c not in columnas_no_nulas]

    print(f"Columnas completamente vacías: {columnas_nulas}")
