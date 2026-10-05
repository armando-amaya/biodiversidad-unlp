import pandas as pd
import os 
import datetime
from pathlib import Path

#EJERCICIO 1A
"""
    Carga un dataset CSV como DataFrame de pandas.
    Parámetros: Nombre o ruta del archivo CSV, Separador del archivo., Encoding del archivo.
    Retorna: pandas.DataFrame
"""

def cargar_dataset(nombre_dataset, separador=",", encoding="utf-8"):

    ruta = Path(nombre_dataset)

    dataframe = pd.read_csv(
        ruta,
        sep=separador,
        encoding=encoding,
        on_bad_lines='skip'
    )

    return dataframe
#descomentar lo de abajo para ver el dataframe
"""
df = cargar_dataset(
    "processed_datasets/iadiza_filtrado.csv",
    separador="\t",
    encoding="utf-8"
)

print(df.head())
"""
#---------------------------------------------------------------------------------------------
#EJERCICIO 2A
def buscar_por_campo(df, columna, texto):
    """
    Filtra el DataFrame buscando coincidencias parciales (subcadenas)
    en una columna específica, ignorando mayúsculas y minúsculas.
    """
    # Si el usuario no escribió nada en el buscador, devolvemos todo el dataset
    if not texto:
        return df
        
    # Convertimos la columna a string (por si hay números o nulos) y filtramos
    # case=False hace que sea case-insensitive (le da igual "A" o "a")
    # na=False evita errores si hay celdas vacías en esa columna
    resultado = df[df[columna].astype(str).str.contains(texto, case=False, na=False)]
    
    return resultado

#----------------------------------------------------------------------------------------------------------------------------------
#EJERCICIO 2B
def aplicar_filtros_avanzados(df, nombres_cientificos=None, observador=None, paises=None, provincias=None, fechas=None):
    """
    Aplica filtros múltiples combinados (intersección) sobre el DataFrame.
    Recibe el Dataframe, nombre del cientifico, observador, pais, provincia, rango.
    Devuelve el Dataframe filtrado.
    """
    res = df.copy()
    
    # 1. Filtros de selección múltiple (Se procesan todos en este bucle corto)
    mapeo = {'scientificName': nombres_cientificos, 'country': paises, 'stateProvince': provincias}
    for col, valores in mapeo.items():
        if valores:
            res = res[res[col].isin(valores)]
            
    # 2. Filtro de texto libre (Observador)
    if observador:
        res = res[res['recordedBy'].astype(str).str.contains(observador, case=False, na=False)]
        
    # 3. Filtro de rango de fechas
    if fechas and len(fechas) == 2:
        fechas_dt = pd.to_datetime(res['eventDate'], errors='coerce').dt.date
        res = res[(fechas_dt >= fechas[0]) & (fechas_dt <= fechas[1])]

    return res

#-----------------------------------------------------------------------------------------------------------------------
#EJERCICIO 2C
def obtener_pagina_dataframe(df, numero_pagina, registros_por_pagina=20):
    """
    Devuelve un subconjunto de filas (una página) del DataFrame.
    Recibe el Dataframe, el numero de pag, la cantidad de registros por pagina
    """
    #Calculamos los índices de inicio y fin para el recorte (slice)
    inicio = (numero_pagina - 1) * registros_por_pagina
    fin = inicio + registros_por_pagina
    
    #Retornamos el fragmento de la tabla correspondiente a esa página
    return df.iloc[inicio:fin]

#-----------------------------------------------------------------------------------------------------------------------
#EJERCICIO 5A
def obtener_metadatos_archivos(ruta_carpeta: str, archivos: list) -> pd.DataFrame:
    """Lee el tamaño y la fecha de modificación de los archivos en disco
       Recibe ruta al directorio y una lista de strings con los nombres de los archivos.
       Devuelve un df con las columnas: nombre del archivo, tamaño y ultima modificacion
    """
    datos = []
    for arch in archivos:
        ruta = os.path.join(ruta_carpeta, arch)
        estado = os.stat(ruta)
        
        # Convertimos el tamaño a MB y la fecha a formato legible
        tamaño_mb = estado.st_size / (1024 * 1024)
        fecha_mod = datetime.datetime.fromtimestamp(estado.st_mtime).strftime("%d/%m/%Y %H:%M:%S")
        
        datos.append({
            "Nombre del archivo": arch,
            "Tamaño (MB)": round(tamaño_mb, 2),
            "Última modificación": fecha_mod
        })
    return pd.DataFrame(datos)


#-----------------------------------------------------------------------------------------------------------------------
#EJERCICIO 4E
"""
    Aplica filtros avanzados al dataset de logs del sistema.
    Permite filtrar por tipo de operación y por rango de fechas.
    Toma los parámetros df_logs (DataFrame de logs), operaciones (lista de operaciones a filtrar) y fechas (tupla con fecha inicio y fin).
"""

def aplicar_filtros_logs_4e(df_logs, operaciones=None, fechas=None):
    res = df_logs.copy()

    if operaciones:
        con_error = 'Registro con ERROR' in operaciones
        operaciones = [op for op in operaciones if op != 'Registro con ERROR']
        if operaciones or con_error:
            res = res[(res['Operación'].isin(operaciones)) | (con_error & (res['Estado'] == 'ERROR'))]

    if fechas and len(fechas) == 2:
        fecha_inicio, fecha_fin = fechas
        fechas_dt = pd.to_datetime(res['Fecha'], errors='coerce').dt.date
        res = res[(fechas_dt >= fecha_inicio) & (fechas_dt <= fecha_fin)]

    return res


def obtener_metricas_logs_4e(df_logs):
    """
    Calcula métricas resumidas para el log filtrado.
    """
    return {
        'INSERT': int((df_logs['Operación'] == 'INSERT').sum()),
        'UPDATE': int((df_logs['Operación'] == 'UPDATE').sum()),
        'DELETE': int((df_logs['Operación'] == 'DELETE').sum()),
        'ERROR': int((df_logs['Estado'] == 'ERROR').sum())
    }
