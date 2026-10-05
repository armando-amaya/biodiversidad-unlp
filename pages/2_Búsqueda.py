import streamlit as st
import pandas as pd
import math
import datetime
from funciones_pandas.procesar_dataset import buscar_por_campo, aplicar_filtros_avanzados, obtener_pagina_dataframe
from funciones_pandas.navegacion_sidebar import mostrar_sidebar

#CONFIURACION DE LA PAGINA
st.set_page_config(page_title="Busqueda de Regisros", page_icon="🔍")

mostrar_sidebar()

st.title("🔍 Pagina de Busqueda")
st.write("Utiliza los filtros del panel central para locaizar registros especificos")

#1. VALIDACION: Verifico si hay un dataset seleccionado en el Inicio
if "df" not in st.session_state:
    st.warning("Por favor, seleccione un dataset en la pagina de Inicio para poder realizar busquedas.")
else:
    #Recupero el DataFrame
    df = st.session_state["df"]

#------------------------------------------------------------------------------------------------------------------------------
    #EJERCICIO 2.A: Buqueda por texto libre en columna seleccionada
    st.header("Busqueda por campo espcifico")

    #El usuario elige una columna de las disponibles
    columnas_disponibles = df.columns.tolist()
    columna_busqueda = st.selectbox(f"Selecciona la columna por la que deseas buscar:", options=columnas_disponibles)

    #El usuario ingresa el texto a buscar
    texto_buscado = st.text_input(f"Ingresa el valor a encontrar en '{columna_busqueda}':")

    #Llamo a la funcion 
    df_filtrado = buscar_por_campo(df, columna_busqueda, texto_buscado)
    
    #Muestro los registros y cantidad
    st.write(f"Resultados encontrados: **{len(df_filtrado)}**")
    st.dataframe(df_filtrado)

#---------------------------------------------------------------------------------------------------------------------------------------
    #EJERCICIO 2.B: Filtros combinables
    st.markdown("---")
    st.header("Filtros Combinables")
    
    #Generamos las opciones únicas extrayéndolas del dataframe (eliminando nulos)
    opciones_especies = sorted(df['scientificName'].dropna().unique().tolist()) if 'scientificName' in df.columns else []
    opciones_paises = sorted(df['country'].dropna().unique().tolist()) if 'country' in df.columns else []
    opciones_provincias = sorted(df['stateProvince'].dropna().unique().tolist()) if 'stateProvince' in df.columns else []
    
    #Creamos los componentes en la interfaz
    filtro_especies = st.multiselect("Filtrar por Nombre Científico:", options=opciones_especies)
    filtro_obs = st.text_input("Filtrar por Observador:")
    filtro_paises = st.multiselect("Filtrar por País:", options=opciones_paises)
    filtro_prov = st.multiselect("Filtrar por Provincia/Estado:", options=opciones_provincias)
    
    #Filtro de fecha con un rango
    st.write("Filtrar por Rango de Fechas:")
    df_fechas = pd.to_datetime(df['eventDate'], errors='coerce').dropna()
    
    if not df_fechas.empty:
        fecha_min_rec = df_fechas.min().date()
        fecha_max_rec = df_fechas.max().date()
        
        #Selector de rango de fechas
        filtro_fechas = st.date_input(
            "Seleccioná el rango de inicio y fin:",
            value=(fecha_min_rec, fecha_max_rec),
            min_value=fecha_min_rec,
            max_value=fecha_max_rec
        )
    else:
        filtro_fechas = None

    #Aplicamos los filtros avanzados sobre el resultado de la primera búsqueda
    df_resultado = aplicar_filtros_avanzados(
        df_filtrado, 
        nombres_cientificos=filtro_especies, 
        observador=filtro_obs, 
        paises=filtro_paises, 
        provincias=filtro_prov,
        fechas=filtro_fechas)
    
    #Muestro los registros y cantidad
    st.write(f"Resultados encontrados tras los filtros: **{len(df_resultado)}** de {len(df)}")
    st.dataframe(df_resultado)

#----------------------------------------------------------------------------------------------------------------
    #EJERCICIO 2.C: Muestra de registros filtrados 

    st.markdown("---")
    st.header("Registros Encontrados")
    total = len(df_resultado)
    st.write(f"Resultados: **{total}** de {len(df)}")

    nombre_dataset = st.session_state.get("dataset_actual")
    
    if total > 0:
        COLUMNAS_A_MOSTRAR = [
    "id", "gbifID", "ocurrenceID", "ocurrencID", "catalogNumber", "datasetKey", 
    "institutionCode", "collectionCode", "basisOfRecord", "modified", "references", "rightsHolder",
    "scientificName", "acceptedScientificName", "genericName", "specificEpithet", "specificEpitht",
    "vernaculaName", "kingdom", "phylum", "class", "order", "family", "genus", "species", "taxonRank", "taxonID",
    "continent", "country", "contryCode", "countryCode", "publishingCountry",
    "stateProvince", "county", "locality", "verbatimeLocality",
    "longitudeDecimal", "latitudeDecimal", "decimalLongitude", "decimalLatitude", 
    "coordinateUncertaintyInMeters", "verbatimElevation",
    "eventDate", "eventTime", "dateIdentified", "year", "recorderBy", "identifiedBy", "inaturalistLogin",
    "sex", "lifeStage", "vitality", "behavior", "captive_cultivated", 
    "fieldNotes", "preparations", "Associated Taxa", "dynamicProperties", "identificationID"
]
        
        # Nos quedamos con todas las columnas del DataFrame EXCEPTO las que queremos ocultar
        columnas_relevantes =[col for col in COLUMNAS_A_MOSTRAR if col in df_resultado.columns]
        df_mostrar = df_resultado[columnas_relevantes]

        # Resolvemos la cantidad de páginas
        REG_POR_PAG = 20
        total_paginas = math.ceil(total / REG_POR_PAG)
        
        # Un selector numérico simple reemplaza a los botones Anterior/Siguiente y sus estados
        pag_elegida = st.number_input("Página:", min_value=1, max_value=total_paginas, value=1, step=1)
        
        # Mostramos la porción de la tabla correspondiente
        df_paginado = obtener_pagina_dataframe(df_mostrar, pag_elegida, REG_POR_PAG)
        st.dataframe(df_paginado, use_container_width=True)
    else:
        st.info("No se encontraron registros.")

#------------------------------------------------------------------------------------------------------
    #EJERCICIO 2.D: Exporta resultados de la pagina actual
    st.markdown(" ") 

    #Convertimos las 20 filas visibles de la página actual a formato CSV (texto) (index=False para que no guarde la columna de números de fila de Pandas)
    csv_data = df_paginado.to_csv(index=False).encode('utf-8')
    
    #Tomamos el nombre del archivo activo de la sesión y le sacamos la extensión (.csv o .txt), para el nombre del archivo a guardar
    nombre_base = st.session_state["dataset_nombre"].split('.')[0]
    # Agregamos la fecha actual en formato 
    fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    nombre_archivo_csv = f"exportacion_{nombre_base}_{fecha_hoy}.csv"
    
    #Componente de Streamlit para descargar
    st.download_button(
        label="📥 Exportar resultados actuales",
        data=csv_data,
        file_name=nombre_archivo_csv,
        mime="text/csv",
        key="boton_exportar_2d")

#------------------------------------------------------------------------------------------------------
    #EJERCICIO 2.E: Resumen estadístico del subconjunto filtrado
    st.markdown("---")
    st.subheader("📊 Resumen Estadístico de la Búsqueda")
    
    #Usamos st.columns para mostrar las 4 métricas en tarjetas horizontales
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        #Cantidad de especies únicas 
        cant_especies = df_resultado['scientificName'].nunique() if 'scientificName' in df_resultado.columns else 0
        st.metric(label="Especies Únicas", value=cant_especies)
        
    with m2:
        #Países representados
        cant_paises = df_resultado['country'].nunique() if 'country' in df_resultado.columns else 0
        st.metric(label="Países", value=cant_paises)
        
    with m3:
        #Provincias representadas
        cant_provincias = df_resultado['stateProvince'].nunique() if 'stateProvince' in df_resultado.columns else 0
        st.metric(label="Provincias", value=cant_provincias)
        
    with m4:
        #Cantidad de observadores únicos 
        cant_observadores = df_resultado['recordedBy'].nunique() if 'recordedBy' in df_resultado.columns else 0
        st.metric(label="Observadores", value=cant_observadores)

#------------------------------------------------------------------------------------------------------
    #EJERCICIO 6.A
    st.markdown("---")

    # Verificamos que se haya aplicado algún filtro
    filtro_aplicado = (
        texto_buscado != "" or
        len(filtro_especies) > 0 or
        filtro_obs != "" or
        len(filtro_paises) > 0 or
        len(filtro_prov) > 0
    )

    if filtro_aplicado and len(df_resultado) > 0:
        st.write(f"registros con filtro aplicado {len(df_resultado)}")
        
        if st.button("Ver ficha", icon=":material/quick_reference_all:"):
            # Guardamos registros filtrados en sesion_state
            st.session_state["registros_mapa"] = df_resultado
            # Redirigimos a P6
            st.switch_page("pages/6_Ficha_de_datos.py")

    # warning 
    else:
        if filtro_aplicado and len(df_resultado) == 0:
            st.warning("No existen registros que coincidan con los filtros.")