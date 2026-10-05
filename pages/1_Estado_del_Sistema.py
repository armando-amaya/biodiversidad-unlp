import streamlit as st
from pathlib import Path
import pandas as pd
from funciones_pandas.navegacion_sidebar import mostrar_sidebar

st.set_page_config(
    page_title="Aplicación de Biodiversidad-44", page_icon="🌿"
)

mostrar_sidebar()

st.title("📄 Estado del Sistema")
st.write("Es un registro de actividad, que muestra de forma tabular los logs, para revisar fechas, datasets, operaciones, registros y estados.")
ruta_log = Path("logs/operations.log")

if not ruta_log.exists():
    st.warning("No se encontró el archivo de logs.")
else:
    registros = []

    with ruta_log.open(encoding="utf-8") as f:
        for linea in f:
            partes = [p.strip() for p in linea.strip().split("|")]

            if len(partes) < 4:
                continue

            fecha = partes[0]
            dataset = partes[1]
            operacion = partes[2]
            cantidad = partes[3].replace("registros", "").strip()
            estado = partes[4] if len(partes) == 5 else "OK"

            registros.append({
                "Fecha": fecha,
                "Dataset": dataset,
                "Operación": operacion,
                "Cantidad": cantidad,
                "Estado": estado
            })

    st.subheader("Logs de operaciones")


#EJERCICIO 4.E: Filtros de LOGS ----------------------------
    from funciones_pandas.procesar_dataset import aplicar_filtros_logs_4e, obtener_metricas_logs_4e

    if registros:
        df_logs = pd.DataFrame(registros)

        st.markdown("---")
        st.header("Filtros Combinables")

        opciones_operaciones = sorted(df_logs['Operación'].dropna().unique().tolist()) + ['Registro con ERROR']
        filtro_operaciones = st.multiselect(
            "Filtrar por tipo de operación:",
            options=opciones_operaciones
        )

        st.write("Filtrar por rango de fechas:")
        fechas_logs = pd.to_datetime(df_logs['Fecha'], errors='coerce').dropna()

        if not fechas_logs.empty:
            fecha_min_rec = fechas_logs.min().date()
            fecha_max_rec = fechas_logs.max().date()
            filtro_fechas = st.date_input(
                "Seleccioná el rango de inicio y fin:",
                value=(fecha_min_rec, fecha_max_rec),
                min_value=fecha_min_rec,
                max_value=fecha_max_rec
            )
        else:
            filtro_fechas = None

        df_resultado = aplicar_filtros_logs_4e(
            df_logs,
            operaciones=filtro_operaciones,
            fechas=filtro_fechas
        )

        st.write(f"Resultados encontrados tras los filtros: **{len(df_resultado)}** de {len(df_logs)}")
        st.dataframe(df_resultado)

        metricas = obtener_metricas_logs_4e(df_resultado)
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Inserciones", metricas['INSERT'])
        col2.metric("Actualizaciones", metricas['UPDATE'])
        col3.metric("Eliminaciones", metricas['DELETE'])
        col4.metric("Errores", metricas['ERROR'])