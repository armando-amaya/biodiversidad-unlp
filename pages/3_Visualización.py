import streamlit as st
from funciones_pandas.navegacion_sidebar import mostrar_sidebar

from funciones_pandas.presentacion_dataset import (
    analizar_comparativa_datasets,
    obtener_columna_geografica,
    generar_grafico_barras,
    generar_grafico_lineas_temporal,
    generar_grafico_taxonomico,
    generar_grafico_completitud
    )

st.set_page_config(
    page_title="Aplicación de Biodiversidad-44", page_icon="🌿"
)

mostrar_sidebar()

st.title("📊 Visualización")
st.write("Aquí se visualizarán estadísticas del dataset.")

#invocacion 3a,3b, 3c
if "df" in st.session_state:
    df_actual = st.session_state["df"]

    columna_filtrada = obtener_columna_geografica(df_actual)
    generar_grafico_barras(df_actual, columna_filtrada)

    generar_grafico_lineas_temporal(df_actual)

    generar_grafico_taxonomico(df_actual)

    generar_grafico_completitud(df_actual)

else:
    st.warning("Por favor, seleccione un dataset en la página de Inicio para poder continuar")


# EJERCICIO 3E
# Usamos Path solo para verificar si hay más de un dataset (requisito del enunciado)
from pathlib import Path 

# Creamos objetos ruta y buscamos con el método .glob aquellos archivos que terminen en .txt y .csv
# .glob devuelve un objeto iterable, pero al crear la lista archivos_validos extraemos todas las rutas y pasan a la memoria
archivos_validos = list(Path("processed_datasets").glob("*.csv")) + list(Path("processed_datasets").glob("*.txt"))

if len(archivos_validos) > 1:
    st.divider()
    st.subheader("Tabla comparativa de datasets")
    
    df_comparativa = analizar_comparativa_datasets("processed_datasets")
    if not df_comparativa.empty:
        st.dataframe(df_comparativa)
    else:
        st.info("No se pudo generar la comparativa. Revisa la terminal.")
else:
    st.info("Se necesitan 2 o + datasets en processed_datasets para comparar")