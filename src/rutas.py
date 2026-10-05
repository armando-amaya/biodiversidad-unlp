# archivo con los paths principales

from pathlib import Path
import sys

# Carpeta principal 'code'
DIR_PPL = Path(__file__).resolve().parent.parent

# Ruta a carpetas de archivos
DIR_RAW = DIR_PPL / "raw_datasets"
PROCESSED_DATASETS = DIR_PPL / "processed_datasets"
SRC = DIR_PPL / "src"

# Ruta a carpeta con codigo/ funciones
EJERCICIO_2 = SRC / "ejercicio_2"
EJERCICIO_3 = SRC / "ejercicio_3"
EJERCICIO_4 = SRC / "ejercicio_4"
EJERCICIO_6 = SRC / "ejercicio_6"

# Rutas a datasets
RUTA_IADIZA = DIR_RAW / "IADIZA" / "occurrence.txt"
RUTA_INATURALIST = DIR_RAW / "iNaturalist" / "observations.csv"
RUTA_XENO = DIR_RAW / "Xeno-canto" / "Occurrence.txt"
