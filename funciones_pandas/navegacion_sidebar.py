import streamlit as st
import os
import datetime
from funciones_pandas.procesar_dataset import cargar_dataset

# Ejercico 6.A_Configuramos la visualizacion de paginas en el sidebar
def mostrar_sidebar():
    """Esta funcion muestra el menú/ las paginas del sidebar.
    """
    #st.sidebar.title("Inicio")
    st.sidebar.page_link("Inicio.py")
    st.sidebar.page_link("pages/1_Estado_del_Sistema.py")
    st.sidebar.page_link("pages/2_Búsqueda.py")
    st.sidebar.page_link("pages/3_Visualización.py")
    st.sidebar.page_link("pages/4_Gestión_de_Registros.py")
    st.sidebar.page_link("pages/5_Datasets.py")
    #st.sidebar.page_link("pages/6_Fichas_de_Datos.py", visibility="hidden")

    #Trabajo con ejercicio 1b: Selector en el Sidebar
    st.sidebar.header ("Configuracion del Dataset")
    RUTA_DATASETS = "processed_datasets"

    archivos = os.listdir (RUTA_DATASETS) if os.path.exists (RUTA_DATASETS) else []
    archivos_disponibles = list(filter(lambda x: x.strip().lower().endswith('.csv') or x.strip().lower().endswith('.txt'), archivos))

    indice_actual = 0
    if "dataset_nombre" in st.session_state and st.session_state["dataset_nombre"] in archivos_disponibles:
        indice_actual = archivos_disponibles.index(st.session_state["dataset_nombre"])

    dataset_elegido = st.sidebar.selectbox (
        "Seleccioná un dataset para trabajar:", 
        options=archivos_disponibles, 
        index=indice_actual,
        key="selector_dataset"
    )

    #Guardamos la seleccion para que persista
    if dataset_elegido:
        ruta_completa = os.path.join (RUTA_DATASETS, dataset_elegido)

        #Cargamos el dataframe si el usuario cambio de archivo
        if "dataset_nombre" not in st.session_state or st.session_state ["dataset_nombre"] != dataset_elegido: 
            st.session_state ["dataset_nombre"]= dataset_elegido

            #Deteccion del separador
            nombre_lower = dataset_elegido.lower()
            if "iadiza" in nombre_lower:
                sep_correcto = "\t"
            else:
                sep_correcto = ","

            st.session_state ["df"] = cargar_dataset (ruta_completa, separador= sep_correcto, encoding= "utf-8")

        
    #EJERCICIO 1C: Agregar un indicador que mueste el nombre del dataset actualmente seleccionado,cantidad de registros del dataset, fecha y hora de la selección. 
    if "df" in st.session_state:
        # 1. Si el usuario cambió de archivo, calculamos y guardamos la nueva fecha/hora

        if "fecha_guardada_para" not in st.session_state or st.session_state["fecha_guardada_para"] != dataset_elegido:
            st.session_state["fecha_seleccion"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            st.session_state["fecha_guardada_para"] = dataset_elegido

        st.sidebar.divider() # Línea divisoria visual prolija
        st.sidebar.subheader("📊 Dataset Activo")
        
        # Indicador 1: Nombre del dataset actualmente seleccionado
        st.sidebar.markdown(f"Archivo: `{st.session_state['dataset_nombre']}`")
        
        # Indicador 2: Cantidad de registros (calculado al vuelo con formato de miles)
        cant_filas = f"{len(st.session_state['df']):,}".replace(",", ".")
        st.sidebar.markdown(f"Cantidad de registros: {cant_filas}")
        
        # Indicador 3: Fecha y hora de la selección
        st.sidebar.markdown(f"Seleccionado el: {st.session_state['fecha_seleccion']}")