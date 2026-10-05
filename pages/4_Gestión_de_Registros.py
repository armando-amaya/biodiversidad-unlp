# Compact, modular version
import streamlit as st
from pathlib import Path
import datetime
from src.ejercicio_4.ej_4b import generar_registro_vacio
from src.ejercicio_4.ej_4c import validar_registro_completo
from src.ejercicio_4.ej_4f import escribir_insercion_registro
from funciones_pandas.presentacion_dataset import renderizar_edicion_registro
from funciones_pandas.navegacion_sidebar import mostrar_sidebar
from funciones_pandas.eliminar_en_dataset import (
    eliminar_por_identificador_unico,
    eliminar_por_valores_columna,
    eliminar_por_condicion)


st.set_page_config(page_title="Gestión de Registros", page_icon="✏️")
st.title("✏️ Gestión de Registros")
st.write("Aqui se permitira realizar operaciones de inserción, actualización y eliminación de registros.")

mostrar_sidebar()

if 'df' not in st.session_state:
    st.warning('Seleccione un dataset en Inicio')
else:
    df = st.session_state['df']; nombre = st.session_state.get('dataset_nombre','sin_nombre')
    st.subheader(f'Dataset activo: {nombre}')
    registro_none = generar_registro_vacio(df.columns.tolist())
    ruta = Path('processed_datasets')/nombre
    sep = '\t' if 'iadiza' in nombre.lower() else ','
    salida = Path('processed_datasets')/f"{ruta.parent.name.lower()}_insercion_registro.csv"

    st.caption(f'Archivo de salida previsto: {salida}')
    cols = st.multiselect('Columnas a completar', options=list(registro_none.keys()))
    parse_fecha = lambda s: datetime.datetime.strptime(s.strip(), '%d/%m/%Y').strftime('%Y-%m-%d')

    with st.form('form_insert'):
        # a cada columna seleccionada se le asigna un nombre "key" en formato k__columna
        # se arma un diccionario con todas las claves y respuestas
        # si la columna contiene la palabra "date" se avisa el formato en que se debe ingresar la fecha
        entradas = {c: st.text_input(f"{c}{' (dd/mm/aaaa)' if 'date' in c.lower() else ''}", key=f'k__{c}') for c in cols}
        submit = st.form_submit_button('Añadir registro')

    if submit:
        datos = {k: None for k in registro_none}; errs=[]
        #datos guarda en formato diccionario el registro nulo
        for k,v in entradas.items():
            if v and str(v).strip():
                try:
                    datos[k] = parse_fecha(v) if 'date' in k.lower() or k.lower()=='eventdate' else v
                except Exception:
                    errs.append(f'Fecha inválida en {k}: dd/mm/aaaa')
        if errs:
            [st.error(e) for e in errs]
        else:
            if not validar_registro_completo(datos, formato_fecha='%Y-%m-%d'):
                st.error('El registro no pasó la validación. No se inserta.')
            else:
                fila = escribir_insercion_registro(ruta, sep, 'utf-8', registro_none, datos)
                if fila is not None:
                    import pandas as pd
                    st.session_state['df'] = pd.concat([df, pd.DataFrame([fila])], ignore_index=True)
                    st.success(f'Registro insertado en archivo: {salida.name}')
                else:
                    st.error('Error al escribir archivo.')

    #EJERCICIO 4.B 
    st.divider()

    st.header("Búsqueda de registros")

    columna_id = df.columns[0]

    id_buscado = st.text_input(f"Ingrese el identificador ({columna_id})")

    if id_buscado:
        registro = df[df[columna_id].astype(str) == str(id_buscado)]

        if registro.empty:
            st.error(f"No se encontró ningún registro con el identificador '{id_buscado}'.")

        else:
            st.success("Registro encontrado.")
            registro = registro.iloc[0]

            #Registro guardado para usar en el 4C
            st.session_state["registro_encontrado"] = registro

            #EJERCICIO 4.C
            renderizar_edicion_registro(df, nombre)

        # Ejercicio 4D
    st.markdown("---")

    st.subheader("Eliminación de registro en dataset: ")
    modo_eliminacion = st.radio(
        "Seleccione el modo de eliminación:",
        ["Por ID único", "Por valores de columna", "Por condición"],
        horizontal=True
        )
    
    if modo_eliminacion == "Por ID único":
        st.write("Escriba un identificador")
        eliminar_por_identificador_unico(df, nombre)
    
    elif modo_eliminacion == "Por valores de columna":
        eliminar_por_valores_columna(df, nombre)

    elif modo_eliminacion == "Por condición":
        st.write("Seleccione una columna")
        
        eliminar_por_condicion(df,nombre)