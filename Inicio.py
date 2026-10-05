import streamlit as st
import os
import datetime
#importo funcion 1a 
from funciones_pandas.procesar_dataset import cargar_dataset
from funciones_pandas.navegacion_sidebar import mostrar_sidebar

st.set_page_config(
    page_title="Aplicación de Biodiversidad-44", page_icon="🌿"
)

mostrar_sidebar()
#


# TÍTULO
st.title("""
🌎 Proyecto de Biodiversidad - Grupo 44""")


st.header("Proyecto de análisis de datos de biodiversidad")

# DESCRIPCIÓN GENERAL
st.write("""
El propósito de la aplicación es brindar accesibilidad a información sobre biodiversidad de la región 
a cualquier grupo de interés al que le sea de utilidad. Además, nos permite analizar datasets de biodiversidad 
para detectar errores, validar información y mejorar la calidad de los datos.
""")

st.header("Importancia del análisis de datos de biodiversidad")

st.write("""
El fácil acceso de los datos de biodiversidad de nuestra región tiene muchas implicancias. Entre ellas: 
           
- Asegurar una fuente confiable y centralizada de datos de muchas fuentes e instituciones, que gracias 
al formato Darwin Core se han vuelto comprensibles y comparables.
         
- Brindar información de calidad a cualquier interesado con fines educativos.
         
- Permitir un reconocimiento más claro de la distribución de especies y sus hábitos comportamentales a 
través de insights, como estadísticas descriptivas y visualización gráfica, tanto a entidades públicas 
como privadas, interesadas en la conservación ambiental.
""")


# DARWIN CORE
st.header("📊 Estándar Darwin Core ")

st.write("""
Darwin Core es un **estándar internacional** de datos diseñado para facilitar el intercambio 
de información sobre biodiversidad. Es un lenguaje común o un "diccionario universal" 
que utilizan los científicos y organizaciones de todo el mundo. Consiste en un conjunto de términos 
(columnas de datos) que permiten organizar información compleja.

El objetivo principal es que los datos de diferentes fuentes sean compatibles entre sí. Sus usos principales son:
         
1.  **Interoperabilidad:** Permite que una base de datos en Colombia se entienda perfectamente con una en España o Australia.

2.  **Publicación Global:** Es el formato requerido para subir datos a grandes plataformas como GBIF 
(Global Biodiversity Information Facility).

3.  **Investigación Científica:** Facilita que los investigadores descarguen millones de registros de diferentes autores 
y puedan analizarlos todos juntos sin tener que limpiar nombres de columnas distintos.

4.  **Preservación Histórica:** Asegura que la información de las colecciones biológicas (herbarios, museos) no se pierda 
y esté organizada de forma lógica a largo plazo.
""")

# INSTRUCCIONES DE USO

st.header("Instrucciones de uso")

st.write("""
- **Para navegar entre páginas:**
Utilizar el menú lateral (sidebar) para acceder a las distintas secciones como estado del sistema, búsqueda y visualización.
         
### Páginas:
- **Estado del sistema**: Es un registro de actividad, que muestra de forma tabular los logs, para revisar fechas, datasets, operaciones, registros y estados.
- **Búsqueda**: Utiliza los filtros del panel central para locaizar registros especificos.
- **Visualización**: En esta pagina se visualizarán estadísticas del dataset.
- **Gestion de Registros**: Esta pagina permitira realizar operaciones de inserción, actualización y eliminación de registros.
- **Datasets**: Se presenta una vista general de todos los datasets disponibles en el sistema.
- **Ficha de Datos**: Ofrece una mapa con las observaciones/ocurrencias seleccionadas en la página de búsqueda (privada).


""")