import streamlit as st
import os
import sys
from funciones_pandas.navegacion_sidebar import mostrar_sidebar


from funciones_pandas.procesar_dataset import (
    obtener_metadatos_archivos,
    cargar_dataset
)

from funciones_pandas.presentacion_dataset import (
    calcular_nulos_por_columna,
    analizar_comparativa_datasets
)

from funciones_pandas.eliminar_en_dataset import (
    obtengo_separador
)

from pathlib import Path


# Nos aseguramos de encontrar la ruta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

mostrar_sidebar()

st.title("🗃️ Exploración de Datasets Globales")
st.write("Aquí se presenta una vista general de todos los datasets disponibles en el sistema.")

RUTA_DATASETS = "processed_datasets"

# Buscamos los archivos disponibles en la carpeta
archivos = os.listdir(RUTA_DATASETS) if os.path.exists(RUTA_DATASETS) else []
archivos_disponibles = list(filter(lambda x: x.strip().lower().endswith(('.csv', '.txt')), archivos))

if not archivos_disponibles:
    st.warning("⚠️ No se encontraron datasets en la carpeta 'processed_datasets'.")
else:
    st.header("Archivos en Disco")
    
    # Llamamos a la función y mostramos la tabla limpia sin índices
    df_meta = obtener_metadatos_archivos(RUTA_DATASETS, archivos_disponibles)
    st.dataframe(df_meta, use_container_width=True, hide_index=True)

    # EJERCICIO 5B

    st.header("Información detallada de un dataset")

    dataset_seleccionado = st.selectbox(
        "Seleccione un dataset",
        archivos_disponibles
    )

    ruta_dataset = os.path.join(
        RUTA_DATASETS,
        dataset_seleccionado
    )

    separador = obtengo_separador(dataset_seleccionado)

    df = cargar_dataset(
        ruta_dataset,
        separador=separador
    )

    total_registros, df_nulos = calcular_nulos_por_columna(df)

    st.subheader("Lista de columnas")
    st.write(df.columns.tolist())

    st.subheader("Cantidad total de registros")
    st.write(total_registros)

    st.subheader("Porcentaje de valores nulos por columna")
    st.dataframe(
        df_nulos,
        use_container_width=True,
        hide_index=True
    )

    # EJERCICIO 5C

    st.header("Comparativa de datasets")

    df_comparativa = analizar_comparativa_datasets(
        RUTA_DATASETS
    )

    if df_comparativa.empty:
        st.info(
            "Se necesitan al menos dos datasets para realizar la comparación."
        )
    else:
        st.dataframe(
            df_comparativa,
            use_container_width=True,
            hide_index=True
        )

# EJERCICIO 5D

st.header("Documentación")

ruta_documentacion = Path("documentation")

archivos_md = sorted(
    [archivo.name for archivo in ruta_documentacion.glob("*.md")]
)

if not archivos_md:
    st.info("No se encontraron archivos Markdown en la carpeta documentation.")
else:
    documento_seleccionado = st.selectbox(
        "Seleccione un documento",
        archivos_md
    )

    ruta_archivo = ruta_documentacion / documento_seleccionado

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()

    st.markdown(contenido)