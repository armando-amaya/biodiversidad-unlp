# Trabajo Integrador 2026 - Seminario de Lenguajes (Python)

## Proyecto de Biodiversidad (Darwin Core)

Este proyecto es una aplicación desarrollada en Python para el procesamiento, validación y visualización de datos de biodiversidad bajo el estándar **Darwin Core**. Se enfoca en la limpieza de datos provenientes de instituciones científicas y su posterior presentación mediante una interfaz interactiva.

## Integrantes - Grupo 44
* Armando Amaya Flores
* Angeles Solange Cancinos
* Lara González
* Manuela Iglesias Delgado
* Amaranta Rode

## Estructura del Repositorio
Basado en las consignas de la cátedra, el repositorio se organiza de la siguiente manera:

* `documentation/`: Archivos Markdown con el análisis de cada dataset (IADIZA, Xeno-canto, iNaturalist).
* `src/`: Modulos de Python (.py), con la lógica de procesamiento y validación.
* `notebooks/`: Entorno de ejecución para los ejercicios de análisis y transformación de datos (del 2 al 7)
* `logs/`: Registro de operaciones (`operations.log`).
* `raw_datasets/`: Datasets originales (excluido del repositorio).
* `processed_datasets/`: Datasets post limpieza (excluido del repositorio).
* `pages/`: Páginas adicionales de la interfaz de Streamlit
* `Inicio.py`: Archivo principal de la aplicación Streamlit
* `funciones_pandas/`: Este archivo contiene las funciones encargadas de manipular los DataFrames para las operaciones de las páginas
 * `.streamlit/`: Controla la navegación / el comportamiento del sidebar para que no liste automáticamente ciertos archivos 



## Configuración del Entorno y Ejecución de la App (Streamlit)
Se deben seguir estos pasos en la terminal para configurar el espacio de trabajo de forma correcta:

### Creación del Entorno Virtual (venv)
Creamos un entorno virtual ejecutando:
py -m venv .venv

# Activar el entorno
# En Windows:
source .venv/Scripts/activate
# En Linux/Mac:
source venv/bin/activate

### Instalación de streamlit y librerias
Con el entorno activo, instalamos los paquetes necesarios:
pip install streamlit
pip install pandas folium streamlit-folium

Con esto ya podemos desarrollar nuestra aplicación, teniendo el venv activo al ejecutarla para que se abra correctamente.
En este caso, ejecutamos un notebook para que las funciones se ejecuten y creen los logs dentro de operations.log.
Al estar creados los logs y tener nuestra app armada, estos se mostraran automáticamente.
Debemos tener cuidado de agregar el .venv a nuestro gitignore.

### Lanzar la aplicación y visualizar:
streamlit run Inicio.py


## License
Este proyecto se distribuye bajo una Licencia . Consulte el archivo `LICENSE` en la raíz del repositorio para más detalles.


    
