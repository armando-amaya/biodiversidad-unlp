import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import datetime 
from src.ejercicio_4.ej_4c import validar_registro_completo
from src.ejercicio_5.ej_5c import actualizar_multiples_campos
from src.ejercicio_5.ej_5d import validar_campo_individual
from src.ejercicio_2.ej_2f import porcentaje_registro_nulo_columna
from funciones_pandas.eliminar_en_dataset import obtengo_separador

#Ejercicio 3a
def obtener_columna_geografica(df: pd.DataFrame) -> str:
    """
    Determina la columna geográfica óptima para agrupar según el dataset.
    Si no encuentra ninguna, devuelve una columna de texto segura para evitar errores.
    Parámetros > df : pandas.DataFrame con los datos de biodiversidad.    
    Retorna: str: El nombre de la columna ('country', 'stateProvince' o 'locality')
    """
    
    paises = df['country'].dropna().unique() if 'country' in df.columns else []
    if len(paises) > 1:
        return 'country'
    
    # Si es un solo país, probamos en orden de prioridad cuáles existen realmente
    if 'stateProvince' in df.columns:
        return 'stateProvince'
    if 'locality' in df.columns:
        return 'locality'
    
    # Si no hay ninguna de las anteriores, buscamos columnas comunes de texto
    columnas_seguras = ['recordedBy', 'scientificName', 'family', 'genus']
    for c in columnas_seguras:
        if c in df.columns:
            return c
            
    # Devolvemos la primera columna que tenga el DataFrame
    return df.columns[0]

def generar_grafico_barras(df: pd.DataFrame, col: str):
    """
    Genera y muestra un gráfico de barras interactivo.
    Parámetros > df : pandas.DataFrame con los datos.
                 col : str, columna por la cual se van a agrupar los datos.
    """
    # Conte de datos y slider interactivo
    conteos = df[col].value_counts()
    if conteos.empty:
        st.warning(f"⚠️ La columna geográfica '{col}' no contiene datos válidos en este dataset.")
        return
    
    top_n = st.slider(f"Cantidad de {col} a mostrar", 1, len(conteos), min(5, len(conteos)))
    datos = conteos.head(top_n)
    
    fig, ax = plt.subplots(figsize=(8, 4))

    nombres_limpios = list(map(lambda x: str(x).strip(), datos.index))
    
    ax.bar(nombres_limpios, datos.values, color='#4CAF50', label='Registros')

    ax.set_title(f"Top {top_n} por {col.capitalize()}", fontsize=12, fontweight='bold')
    ax.set_xlabel(col.capitalize(), fontsize=10)
    ax.set_ylabel("Cantidad de Registros", fontsize=10)
    ax.legend(loc='upper right')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

#Ejercicio 3b
def generar_grafico_lineas_temporal(df: pd.DataFrame):
    """Genera un gráfico de líneas por año basado en eventDate.
       Parámetros > df : pandas.DataFrame con los datos.
    """
   
    col_fecha = next((c for c in df.columns if c.lower() == 'eventdate'), None)
    
    if not col_fecha:
        st.warning("⚠️ El dataset seleccionado no contiene información de fechas para el análisis temporal.")
        return
    
    # Convertimos a fecha usando la columna real encontrada (unificamos zonas horarias a UTC)
    fechas = pd.to_datetime(df[col_fecha], errors='coerce', utc=True)
    anos = fechas.dropna().dt.year.astype(int)
    anos_validos = anos[anos >= 1900]
    
    st.info(f"ℹ️ Registros excluidos: {len(df) - len(anos_validos)}")
    
    if list(anos_validos):
        conteos = anos_validos.value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.plot(conteos.index, conteos.values, color='#FF5722', marker='o', label='Registros')
        
        ax.set_title("Registros por Año")
        ax.set_xlabel("Año")
        ax.set_ylabel("Cantidad")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)
    else:
        st.warning("⚠️ No hay años válidos suficientes para graficar.")

#Ejercicio 3c
def generar_grafico_taxonomico(df: pd.DataFrame):
    """Genera un gráfico de distribución según el nivel taxonómico seleccionado.
       Parámetros > df : pandas.DataFrame con los datos.
    """
    
    # Selector interactivo 
    opciones = {"Clase": "class", "Orden": "order", "Familia": "family"}
    seleccion = st.selectbox("Seleccioná el nivel taxonómico:", list(opciones.keys()))
    columna = opciones[seleccion]
    
    if columna not in df.columns:
        st.error(f"La columna '{columna}' no existe en este dataset.")
        return
        
    # Nos quedamos con los 10 más frecuentes para que no se sature el gráfico
    conteos = df[columna].dropna().value_counts().head(10)
    
    if conteos.empty:
        st.warning(f"⚠️ No hay datos disponibles para el nivel: {seleccion}.")
        return
        
    # Gráfico de barras horizontales
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.barh(conteos.index, conteos.values, color='#9C27B0', label='Registros')
    
    # Requisitos obligatorios
    ax.set_title(f"Top 10 por {seleccion}")
    ax.set_xlabel("Cantidad de Registros")
    ax.set_ylabel(seleccion)
    ax.legend()
    ax.invert_yaxis()  # Para que el más grande quede arriba de todo
    
    plt.tight_layout()
    st.pyplot(fig)

  
 #Ejercicio 3d

def generar_grafico_completitud(df):
    """
    Genera un gráfico con el porcentaje
    de registros no nulos por columna.
    Reutiliza la función del Ejercicio 2.F.
    """

    nombre_dataset = st.session_state["dataset_nombre"]
    ruta_dataset = f"processed_datasets/{nombre_dataset}"

    separador = obtengo_separador(nombre_dataset)

    porcentajes_nulos = porcentaje_registro_nulo_columna(
        ruta_dataset,
        separador,
        "utf-8"
    )

    porcentajes_completos = {}

    for columna, porcentaje_nulo in porcentajes_nulos.items():
        porcentajes_completos[columna] = 100 - porcentaje_nulo

    datos = sorted(
        porcentajes_completos.items(),
        key=lambda x: x[1],
        reverse=True
    )

    columnas = []
    valores = []

    for columna, valor in datos:
        columnas.append(columna)
        valores.append(valor)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(columnas, valores, color="#4CAF50")

    ax.set_title("Completitud de columnas")
    ax.set_xlabel("Porcentaje")
    ax.set_ylabel("Columnas")

    ax.invert_yaxis()

    st.pyplot(fig)


# EJERCICIO 3.E: Tabla Comparativa (versión simplificada y directa)
from pathlib import Path
"""
    La función procesar_dataset_individual recorre los archivos CSV y TXT en la carpeta "processed_datasets",
    Sus parámetros son: ruta_str: str (la ruta al archivo individual) y mtime: float (el tiempo de modificación del archivo).
"""

@st.cache_data
def procesar_dataset_individual(ruta_str: str, mtime: float) -> dict:
    ruta = Path(ruta_str)
    sep = "\t" if "iadiza" in ruta.name.lower() else ","
    # Lectura simple: si falla utf-8 probamos latin1, no más capas
    try:
        df = pd.read_csv(ruta, sep=sep, encoding='utf-8', on_bad_lines='skip')
    except Exception:
        try:
            df = pd.read_csv(ruta, sep=sep, encoding='latin1', on_bad_lines='skip')
        except Exception:
            return {'Dataset': ruta.name, 'Registros': 0, '% Coordenadas Válidas': 0.0, '% Fechas Válidas': 0.0, '% Campos Completados': 0.0}

    total = len(df)
    if total == 0:
        return {'Dataset': ruta.name, 'Registros': 0, '% Coordenadas Válidas': 0.0, '% Fechas Válidas': 0.0, '% Campos Completados': 0.0}

    cols = list(df.columns)

    # Buscamos sólo los nombres que sabemos que existen en estos datasets
    def find_lat(cols):
        pats = ['decimallatitude', 'latitudedecimal']
        return next((c for c in cols if c.lower() in pats), None)

    def find_lon(cols):
        pats = ['decimallongitude', 'longitudedecimal']
        return next((c for c in cols if c.lower() in pats), None)

    lat_c, lon_c = find_lat(cols), find_lon(cols)

    # Validación ligera de coordenadas (rangos válidos)
    pct_coords = 0.0
    if lat_c and lon_c:
        lat = pd.to_numeric(df[lat_c].astype(str).str.replace(',', '.').str.strip(), errors='coerce')
        lon = pd.to_numeric(df[lon_c].astype(str).str.replace(',', '.').str.strip(), errors='coerce')
        valid = lat.between(-90, 90) & lon.between(-180, 180)
        pct_coords = round(valid.sum() / total * 100, 2)

    # Fecha: buscamos sólo `eventDate` (nombre estándar en los datos procesados)
    date_c = next((c for c in cols if c.lower() == 'eventdate'), None)
    pct_fecha = 0.0
    if date_c:
        # Forzamos a UTC para evitar errores por zonas horarias mezcladas
        fechas = pd.to_datetime(df[date_c], errors='coerce', utc=True)
        anos = fechas.dt.year
        valid = anos.notna() & (anos >= 1900)
        pct_fecha = round(valid.sum() / total * 100, 2)

    # Completitud simple: promedio de no-nulos por columna
    pct_completo = round(df.notnull().mean().mean() * 100, 2)

    return {'Dataset': ruta.name, 'Registros': int(total), '% Coordenadas Válidas': pct_coords, '% Fechas Válidas': pct_fecha, '% Campos Completados': pct_completo}


@st.cache_data
def analizar_comparativa_datasets(ruta_base: str = "processed_datasets") -> pd.DataFrame:
    ruta = Path(ruta_base)
    if not ruta.exists():
        return pd.DataFrame()

    archivos = [*ruta.glob("*.csv"), *ruta.glob("*.txt")]
    if len(archivos) <= 1:
        return pd.DataFrame()

    resultados = []
    for a in archivos:
        resultados.append(procesar_dataset_individual(str(a), a.stat().st_mtime))

    return pd.DataFrame(resultados)


def detectar_columna_id(df: pd.DataFrame) -> str:
    candidatas = ('gbifID', 'id', 'occurrenceID', 'catalogNumber')
    return next((col for col in candidatas if col in df.columns), df.columns[0])


def obtener_separador_dataset(nombre_dataset: str) -> str:
    return '\t' if 'iadiza' in nombre_dataset.lower() else ','


def valor_a_texto(valor) -> str:
    return '' if pd.isna(valor) else str(valor)


#EJERCICIO 4.C
# Muestra un formulario editable con los valores del registro localizado en 4.B.
# Valida cada campo modificado (ej_5d), luego aplica todos los cambios al archivo
# con actualizar_multiples_campos (ej_5c). Muestra un resumen de los cambios aplicados.

def renderizar_edicion_registro(df: pd.DataFrame, nombre_dataset: str):
    """
    La Función renderizar_edicion_registro toma los parámetros df (DataFrame del dataset) y nombre_dataset (nombre del archivo) 
    para mostrar un formulario de edición del registro encontrado en 4.B. 
    Valida los cambios y los guarda en un nuevo archivo.
    """
    registro = st.session_state.get('registro_encontrado')
    if registro is None:
        st.info('Busque primero un registro usando 4.B.')
        return

    columna_id = df.columns[0]
    id_valor   = valor_a_texto(registro[columna_id])
    sep        = obtener_separador_dataset(nombre_dataset)
    ruta       = Path('processed_datasets') / nombre_dataset
    nombre_sal = Path(nombre_dataset).stem + '_edicion'

    st.subheader('4.C - Editar registro encontrado')
    cols_edit = [c for c in df.columns if c != columna_id]

    with st.form('form_4c'):
        st.text_input(columna_id, value=id_valor, disabled=True)
        entradas = {c: st.text_input(c, value=valor_a_texto(registro[c]), key=f'4c_{c}') for c in cols_edit}
        submit = st.form_submit_button('Guardar cambios')

    if not submit:
        return

    # Solo los campos que realmente cambiaron
    cambios = {c: v.strip() for c, v in entradas.items()
               if v.strip() and v.strip() != valor_a_texto(registro[c])}
    if not cambios:
        st.info('No hay cambios para aplicar.')
        return

    # Validar con ej_5d
    errores = [f'{c}: valor inválido' for c, v in cambios.items()
               if not validar_campo_individual(c, v)]
    if errores:
        list(map(st.error, errores))
        return

    # Actualizar en archivo con ej_5c
    resultado = actualizar_multiples_campos(ruta, sep, 'utf-8', id_valor, cambios, nombre_sal, 'processed_datasets')
    if 'exitosa' not in resultado:
        st.error(resultado)
        return

    # Recargar df en memoria desde el archivo generado
    ruta_salida = Path('processed_datasets') / f"{nombre_sal}{Path(nombre_dataset).suffix}"
    try:
        st.session_state['df'] = pd.read_csv(ruta_salida, sep=sep, encoding='utf-8', on_bad_lines='skip')
    except Exception:
        pass  # no es crítico; la UI seguirá mostrando el df anterior

    resumen = pd.DataFrame([{'Campo': c, 'Antes': valor_a_texto(registro[c]), 'Ahora': v}
                            for c, v in cambios.items()])
    st.success(f'Cambios guardados en {ruta_salida.name}.')
    st.dataframe(resumen, use_container_width=True)



# EJERCICIO 5.B

def calcular_nulos_por_columna(df):
    """
    Calcula la cantidad total de registros y el porcentaje
    de valores nulos por columna.

    Retorna:
    - total_registros
    - DataFrame con columnas:
        * Columna
        * Porcentaje de Nulos
    """

    total_registros = len(df)

    porcentajes_nulos = {}

    for columna in df.columns:

        if total_registros > 0:
            porcentaje_nulo = (
                df[columna].isnull().sum()
                / total_registros
            ) * 100
        else:
            porcentaje_nulo = 0.0

        porcentajes_nulos[columna] = round(
            porcentaje_nulo,
            2
        )

    df_resultado = pd.DataFrame({
        "Columna": list(porcentajes_nulos.keys()),
        "Porcentaje de Nulos": list(
            porcentajes_nulos.values()
        )
    })

    df_resultado = df_resultado.sort_values(
        by="Porcentaje de Nulos",
        ascending=False
    )

    return total_registros, df_resultado