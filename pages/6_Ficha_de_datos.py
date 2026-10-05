import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
from funciones_pandas.mapeo_dataset import son_coordenadas_validas
from funciones_pandas.navegacion_sidebar import mostrar_sidebar

# CONFIGURACION DE LA PAGINA
st.set_page_config(page_title="Ficha de Datos", page_icon="🔍")

mostrar_sidebar()

# Configuracion de la página
st.title("🔍 Ficha de Datos")

# Verifico si hay registros seleccionados
if "registros_mapa" not in st.session_state:
    st.warning("No hay registros seleccionados. Vuelva a la página de búsqueda.")
    st.stop()
else:
    df = st.session_state["registros_mapa"]

# Ejercicio 6.B
st.subheader("Mapa de Geográfico de las observaciones 🗺️")

# Guardamos columnas con coordenadas
columna_lat = "decimalLatitude" if "decimalLatitude" in df.columns else "latitudeDecimal"
columna_lon = "decimalLongitude" if "decimalLongitude" in df.columns else "longitudeDecimal"

# Reutilizamos 3.A, filtramos columnas válidas
validos_r = df.apply(son_coordenadas_validas, axis=1)
df_validos = df[validos_r].copy()
registros_excluidos = len(df) - len(df_validos)

st.warning(f"Cantidad de registros con coordenadas inválidas: {(registros_excluidos)}")

# Opciones disponibles según el dataset
criterio = ["scientificName", "institutionCode", "country", "countryCode"]
criterio_existente = [opt for opt in criterio if opt in df.columns]

if not criterio_existente:
    st.error("❌ No hay columnas válidas para colorear el mapa")
    st.stop()

criterio_mapa = st.selectbox(
    "Colorear puntos geográficos por:",
    options=criterio_existente
)

# Creamos mapa con centro en Argentina
mapa = folium.Map(location=(-37,-67), zoom_start=5, control_scale=True)

# Asignamos colores por criterio
valores_unicos = df_validos[criterio_mapa].dropna().unique()

colores = ["red","blue","green","purple","orange","beige","pink",
           "darkred","lightred","darkblue","lightblue","darkgreen","cadetblue"]

mapa_colores = {
    val: colores[i % len(colores)]
    for i, val in enumerate(valores_unicos)
}

st.info(f"Mostrando mapa con registros válidos ({len(df_validos)})")

columnas_id_posibles = ["id", "gbifID"]

valor_id = None
for col in columnas_id_posibles:
    if col in df_validos.columns:
        valor_id = col
        break

if valor_id is None:
    valor_id = df_validos.columns[0]


# Agregamos cada punto al mapa
for indice, fila in df_validos.iterrows():
    latitud = float(fila[columna_lat])
    longitud = float(fila[columna_lon])
    color = mapa_colores.get(fila.get(criterio_mapa), "gray")

    folium.CircleMarker(
        location=[latitud,longitud],
        radius=5,
        tooltip=(f"{fila.get(criterio_mapa)} | Haz clic para más info"),
        color=color,
        fill=True,
        popup=folium.Popup(str(fila[valor_id]), max_width=300)
    ).add_to(mapa)

# le damos vida al mapa
datos_mapa = st_folium(mapa,width=800,height=800)

# EJERCICIO 6.C
if datos_mapa and datos_mapa.get("last_object_clicked_popup"):
    id_seleccionado = str(datos_mapa["last_object_clicked_popup"]).strip()

    registro_seleccionado = df_validos[
        df_validos[valor_id].astype(str).str.strip() == id_seleccionado
    ]

    if not registro_seleccionado.empty:
        st.subheader("📋 Ficha de la observación seleccionada")
        o_fila = registro_seleccionado.iloc[0]

        st.subheader("Información Taxonomica")
        st.table({
            "Campo": [
                "Reino", "Filo", "Clase", "Orden",
                "Familia", "Género", "Especie"
            ],
            "Valor":[
                o_fila.get("kingdom", "N/A"),
                o_fila.get("phylum", "N/A"),
                o_fila.get("class", "N/A"),
                o_fila.get("order", "N/A"),
                o_fila.get("family", "N/A"),
                o_fila.get("genus", "N/A"),
                o_fila.get("scientificName", "N/A"),
            ]
        })
        st.markdown("**Lugar y Fecha**")
        st.table({
            "Campo": ["País", "Provincia", "Localidad", "Fecha"],
            "Valor": [
                o_fila.get("country","N/A"),
                o_fila.get("stateProvince","N/A"),
                o_fila.get("locality","N/A"),
                o_fila.get("eventDate","N/A"),
            ]
        })
    else:
        st.warning("No se encontró registro.")

    # EJERCICIO 6.D
    st.markdown("---")
    if not registro_seleccionado.empty:
        st.subheader("Material Multimedia Asociado")
        m_fila = registro_seleccionado.iloc[0]

        url_media = None
        
        # 1. Intentamos buscar en el dataset cruzado de multimedia si existe en session_state
        if "df_multimedia" in st.session_state:
            df_multi = st.session_state["df_multimedia"]
            id_col_multi = df_multi.columns[0]
            multimedia_row = df_multi[df_multi[id_col_multi].astype(str).str.split('.').str[0] == id_seleccionado]
            
            if not multimedia_row.empty:
                # Buscamos columnas comunes de link multimedia
                for col in ["identifier", "accessURI", "references", "goodQualityAccessURI"]:
                    if col in multimedia_row.columns:
                        url_media = multimedia_row.iloc[0][col]
                        break

        # 2. Si no se encontró en la tabla auxiliar, buscamos en columnas del registro base
        if pd.isna(url_media) or str(url_media).strip() == "" or str(url_media).lower() == "n/a":
            for col in ["associatedMedia", "references", "image_url"]:
                if col in m_fila.index and str(m_fila[col]) != "N/A":
                    url_media = m_fila[col]
                    break

        # 3. Procesamos y filtramos según la consigna 
        if pd.notna(url_media) and str(url_media).strip() != "" and str(url_media).lower() != "n/a":
            url_string = str(url_media).strip()
            url_lower = url_string.lower()
            
            # Identificamos el origen (Xeno-Canto o iNaturalist)
            dataset_origen = str(m_fila.get("institutionCode", "")).lower()
            es_xeno_canto = "xeno" in dataset_origen or "canto" in dataset_origen or "xeno" in url_lower

            if es_xeno_canto:
                # Solo reproducir sonidos
                url_audio_directo = f"https://xeno-canto.org/{id_seleccionado}/download"
                st.audio(url_audio_directo)
            else:
                # iNaturalist u otros: Mostrar fotos si contienen extensiones de imagen o es iNaturalist
                if any(ext in url_lower for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) or "inaturalist" in url_lower:
                    st.image(url_string, caption="Evidencia fotográfica", use_container_width=True)
                elif any(ext in url_lower for ext in [".mp3", ".wav", ".ogg"]):
                    st.audio(url_string)
                else:
                    st.warning("El formato multimedia no se puede previsualizar directamente.")
                    st.link_button("🔗 Abrir enlace externo", url_string)
        else:
            st.info("El dataset no registra material multimedia disponible para esta ocurrencia.")
            
    else:
        st.warning(f"No se pudo mapear la selección. El ID de Folium '{id_seleccionado}' no coincide con los registros activos.")
