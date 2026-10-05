"""
Esta función recibe una columna y un tipo ('numeric', 'coordinate' o 'text')
y retorna el mayor y el menor valor de la columna, dependiendo del tipo.
path_ruta: path, ruta hacia el dataset.
columna: lista, compuesta de los valores almacenados en el dataset.
tipo: string, valor de la columna a analizar.
"""

def metrica_de_columna(columna, tipo):

    # filtramos de la columna recibida los valores nulos y/o vacíos
    columna_fil = [c for c in columna if c not in (None, "", " ")]

    # preguntamos si columna no es vacía
    if not columna_fil:
        return {"mensaje": "La columna está vacía, no se puede analizar."}

    # Preguntamos si el tipo recibido coincide
    if tipo == "numeric":
        # Convertimos a float para calcular
        # Recorremos la columna recibida y guardamos en una lista
        numeros = [float(cf) for cf in columna_fil]
        return {
            "menor valor encontrado": min(numeros),
            "mayor valor encontrado": max(numeros),
            "promedio": sum(numeros) / len(numeros)
        }
    elif tipo == "coordinate":
        coordenada = [float(cf) for cf in columna_fil]
        return {
            "menor valor encontrado": min(coordenada),
            "mayor valor encontrado": max(coordenada)
        }
    elif tipo == "text":
        # Calculamos la cantidad de caracteres por string y guardamos en una lista
        longitudes = [len(str(cf)) for cf in columna_fil]
        return {
            "menor cantidad de caracteres": min(longitudes),
            "mayor cantidad de caracteres": max(longitudes)
        }
    else:
        raise ValueError("No se reconoce el tipo. Usa 'numeric', 'coordinate' o 'text'.")