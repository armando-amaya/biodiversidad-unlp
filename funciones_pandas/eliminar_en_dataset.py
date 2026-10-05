import streamlit as st
import pandas as pd
from pathlib import Path

# llamamos funciones de la primera parte
from src.ejercicio_6.ej_6a import elimino_registro_por_id
from src.ejercicio_6.ej_6b import eliminar_registros_por_lista
from src.ejercicio_6.ej_6c import eliminar_registros, cumple_condicion


def eliminar_por_identificador_unico(df_actual, nombre):
    """ Esta funcion elimina un registro del dataset al pedir un identificador
    único. Muestra una vista previa de los registros a eliminar y pide
    confirmación para realizar la opeación.
    df_actual = dataFrame con el dataset seleccionado actual.
    nombre = nombre del dataset seleccionado actual.
    """
    columna_id = None
    if "gbifID" in df_actual.columns:
        columna_id = "gbifID"
    elif "id" in df_actual.columns:
        columna_id = "id"

    if columna_id is None:
        st.warning("El dataset no tiene columnda de identificación.")
    else:
        # obtenemos el dataset para pasar como parametro
        ruta_dataset = Path("processed_datasets") / nombre
        ejemplo = df_actual[columna_id].dropna().iloc[0]
        st.write(f"Ejemplo: {ejemplo}")

        # Input del ID a eliminar
        id_a_eliminar = st.text_input(f"Ingresá el {columna_id} a eliminar:")

        # Vista previa
        if id_a_eliminar:
            vista_previa = df_actual[df_actual[columna_id].astype(str) == str(id_a_eliminar)]

            if vista_previa.empty:
                st.info("No se encontró ningún registro con ese ID.")
            else:
                st.warning(f"Cantidad de registros coincidentes: **{len(vista_previa)}**")
                st.dataframe(vista_previa)

                # Pedimos confirmacion para eliminar definitivamente
                if confirmar_eliminacion():
                    if st.button("ELIMINAR", type="primary", icon=":material/delete:"):

                        exito = elimino_registro_por_id(
                            ruta_dataset,
                            separador = obtengo_separador(nombre),
                            encoding="utf-8",
                            nombre_columna=columna_id,
                            id_para_eliminar=id_a_eliminar
                        )

                        if exito:
                            st.success("Registro eliminado correctamente.")
                        else:
                            st.error("No se pudo eliminar el registro.")

# Por valor de una columna
def eliminar_por_valores_columna(df,nombre):
    """Esta funcion elimina registros de una columna del dataFrame actual
    si coinciden con los datos ingresados por el usuraio. Muestra una vista
    previa de los registros a eliminar y pide confirmación para realizar la
    opeación.
    df_actual = dataFrame con el dataset seleccionado actual.
    nombre = nombre del dataset seleccionado actual.
    """
    st.write("Seleecione una columna")
    columna_v = st.selectbox(
        "Columna",
        options=df.columns,
        key="col2_valor"
    )

    ejemplo = df[columna_v].dropna().iloc[1]
    st.write(f"Ejemplo: {ejemplo}")

    # pedir valores a eliminar
    valor_a_eliminar = st.text_input(f"Ingrese valor o valores de '{columna_v}' a eliminar (separados por coma)")
    
    # proceso de eliminacion
    if valor_a_eliminar and columna_v:
        lista_valores=[v.strip() for v in valor_a_eliminar.split(",")]
        vista_previa = df[df[columna_v].astype(str).isin(lista_valores)]

        if vista_previa.empty:
            st.warning("No se encontró ningun registro con ese valor")
        else:
            ruta_dataset = Path("processed_datasets") / nombre
            
            st.info(f"Cantidad de registros coincidentes: {len(vista_previa)}")
            st.dataframe(vista_previa)
            
            # Pedimos confirmacion para eliminar definitivamente
            if confirmar_eliminacion():
                if st.button("Eliminar",type="primary", icon=":material/delete:"):
                    exito = eliminar_registros_por_lista(
                        ruta_dataset,
                        separador,
                        'utf-8',
                        columna_v,
                        lista_valores,
                    )
                    if exito:
                        st.success("Registro/s eliminado correctamente.")
                    else:
                        st.error("No se pudo eliminar el registro/s.")

# Acá por condicion sobre una columna == != < <= > >=
def eliminar_por_condicion(df, nombre):
    """Esta funcion elimina registros que cumplean una condicion (==, !=,
    >, >=, <, <=) sobre una columna seleccionada del dataFrame actual
    seleccionada por el usuraio. Muestra una vista
    previa de los registros a eliminar y pide confirmación para realizar la
    opeación.
    df_actual = dataFrame con el dataset seleccionado actual.
    nombre = nombre del dataset seleccionado actual.
    retorna un booleano, True para confirmar que se elimanaron archivos,
    False si se cancela la operacion
    """
    columna_c = st.selectbox("Columna",
                             options=df.columns,
                             key="col3_elegida")

    condicion_elegida = st.selectbox(
        "Condición",
        options=["==", "!=", ">", ">=", "<", "<="],
        key="col3_condicion"
    )

    valor_a_evaluar = st.text_input("Valor", key="tab3_valor")

    if columna_c and condicion_elegida and valor_a_evaluar:
        try:
            vista_previa = df[df[columna_c].astype(str).apply(
                lambda x: cumple_condicion(x, condicion_elegida, valor_a_evaluar))]
            
            if vista_previa.empty:
                st.info("No existen registros para evaluar condicion.")
            else:
                st.info(f"Cantidad de coincidentes: {len(vista_previa)}")
                st.dataframe(vista_previa)

                ruta_salida = Path("processed_datasets")/f"{nombre}_por_condicion.csv"
                ruta_dataset = Path("processed_datasets") / nombre 

                # Pedimos confirmacion para eliminar definitivamente
                if confirmar_eliminacion():
                    if st.button("Eliminar", type="primary", icon=":material/delete:"):

                        eliminar_registros(
                            ruta_csv=ruta_dataset,
                            columna=columna_c,
                            condicion=condicion_elegida,
                            valor=valor_a_evaluar,
                            ruta_salida=ruta_salida,
                            delimiter=obtengo_separador(nombre),
                        )
                        st.success("Se eliminaron los registros correctamente.")
                        return True

        except Exception as e:
            st.error(f"Erro al generar la vista previa {e}")


def obtengo_separador(nombre):
    """Esta funcion averigua el delimitador del dataset.
    nombre: nombre del archivo Dataframe.
    retorna un string con el separador correspondiente.
    """
    if 'iadiza' in nombre.lower():
        return '\t'
    else:
        return ','

def confirmar_eliminacion():
    """Esta función pide la confirmación del usuraio ua vez presionado el
    botón de eliminar a través de un checkbox.
    Retorna un bololeano, True para confirmar la eliminacion, False para
    cancalear la operacion"""
    confirmacion = st.checkbox("¿Quiere eliminar los registros seleccionados?")
    
    if confirmacion:
        return True
    else:
        return False