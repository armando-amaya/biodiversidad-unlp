## Justificación de la Selección de Columnas Relevantes 

Para la visualización de los resultados en la interfaz de usuario desarrollada con Streamlit, se decidió aplicar un criterio de selección de columnas basado en la relevancia de la información y en la calidad de los datos disponibles. Esta decisión se fundamenta en los siguientes aspectos:

### 1. Densidad de la información y calidad de los datos

Durante las etapas de exploración, limpieza y análisis de los tres datasets, se identificó que varias columnas presentaban un elevado porcentaje de valores nulos, vacíos o incompletos. La inclusión de estos atributos en la visualización principal generaría ruido visual y dificultaría la interpretación de la información por parte del usuario.

Por este motivo, se optó por excluir de la vista principal aquellas columnas con baja densidad de datos o con escaso aporte informativo, priorizando únicamente los campos con un nivel aceptable de completitud.

### 2. Relevancia de la información para el dominio de análisis

Con el objetivo de facilitar la lectura y comprensión de los registros, se seleccionaron únicamente aquellos atributos considerados esenciales para identificar y caracterizar cada observación. Esta estrategia permite destacar la información más significativa del dominio de estudio y evita sobrecargar la interfaz con datos secundarios o redundantes.

### 3. Usabilidad y experiencia de usuario

La reducción del número de columnas también responde a criterios de usabilidad. Mostrar una gran cantidad de atributos en tablas interactivas puede provocar desplazamientos horizontales excesivos, dificultando la navegación y la comparación entre registros. Al limitar la visualización a los campos más relevantes, se obtiene una interfaz más clara, ordenada y fácil de utilizar.

### Conclusión

La selección de columnas no implicó una pérdida de información crítica, sino una adaptación de los datos para mejorar su interpretación visual. El criterio aplicado buscó equilibrar la calidad de los datos, la relevancia de los atributos y la experiencia de usuario, permitiendo presentar información significativa de manera clara y eficiente.