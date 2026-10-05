import csv
from pathlib import Path
from collections import defaultdict

from ejercicio_3.ej_3a import validar_registro as validar_coordenadas_rango
from ejercicio_3.ej_3b import coordenadas_incompletas
from ejercicio_3.ej_3c import validar_fecha_registro
from ejercicio_3.ej_3e import validar_registro
from ejercicio_3.ej_3h import coordenadas_en_america
from ejercicio_3.ej_3f import incertidumbre_invalida_fila
from src.CodigosPaises import CODES

# importamos funciones el ejercicio 7
from src.ejercicio_7.registro import crear_linea_log, registrar_en_archivo

# ── Etiquetas legibles para cada validación ───────────────────────────────────
MOTIVOS = {
    "coord_rango"     : "Coordenadas fuera de rango           (3a)",
    "coord_incompleta": "Coordenada incompleta                (3b)",
    "fecha_invalida"  : "Formato de fecha inválido            (3c)",
    "pais_invalido"   : "Código de país inválido              (3e)",
    "fuera_america"   : "Coordenadas fuera de América         (3h)",
    "incertidumbre"   : "Incertidumbre de coordenada inválida (3f)",
}


def _evaluar_motivos(reg, formato_fecha):
    """
    Llama a cada validación del ejercicio 4c por separado.
    Devuelve:
        es_valida (bool)
        fallidos  (list[str])  — claves de MOTIVOS que no pasaron
    """
    fallidos = []

    if not validar_coordenadas_rango(reg):
        fallidos.append("coord_rango")

    if coordenadas_incompletas(reg):
        fallidos.append("coord_incompleta")

    if not validar_fecha_registro(reg, "eventDate", formato_fecha):
        fallidos.append("fecha_invalida")

    if validar_registro(reg, "countryCode", CODES) is not None:
        fallidos.append("pais_invalido")

    if not coordenadas_en_america(reg):
        fallidos.append("fuera_america")

    if incertidumbre_invalida_fila(reg, "coodinateUncertaintyInMeters") is not None:
        fallidos.append("incertidumbre")

    return (len(fallidos) == 0), fallidos

"""
   La funcion recibe: ruta del dataset, separador, encoding y el formato de fecha a evaluar.
   
    Retorna: un nuevo archivo en processed_datasets sin los registros inválidos.
    AdemásImprime un reporte con cantidad eliminada, porcentaje y motivos.
"""

def limpiar_dataset(ruta_original: Path, separador: str = "\t",
                    encoding: str = "utf-8", formato_fecha: str = "%Y-%m-%d"):


    # ── Ruta de salida ────────────────────────────────────────────────────────
    # raw_datasets/IADIZA/occurrence.txt  →  processed_datasets/iadiza-procesado.txt
    nombre_salida = ruta_original.parent.name.lower() + "-procesado" + ruta_original.suffix
    ruta_salida   = ruta_original.parents[2] / "processed_datasets" / nombre_salida
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    conservados    = 0
    eliminados     = 0
    conteo_motivos = defaultdict(int)
    errores        = []

    # ── 1) Leer  2) Validar  3) Escribir válidos ──────────────────────────────
    try: 
        with open(ruta_original, "r", encoding=encoding) as entrada, \
             open(ruta_salida,   "w", encoding=encoding, newline="") as salida:
    
            lector   = csv.DictReader(entrada, delimiter=separador)
            escritor = csv.DictWriter(salida, fieldnames=lector.fieldnames, delimiter=separador)
            escritor.writeheader()
    
            for num_fila, fila in enumerate(lector, start=2):
                try:
                    es_valida, fallidos = _evaluar_motivos(fila, formato_fecha)
                    if es_valida:
                        escritor.writerow(fila)
                        conservados += 1
                    else:
                        eliminados += 1
                        for motivo in fallidos:
                            conteo_motivos[motivo] += 1
                except Exception as e:
                    eliminados += 1
                    errores.append((num_fila, str(e)))

# ── 4) Reporte ────────────────────────────────────────────────────────────
        total    = conservados + eliminados
        pct_elim = eliminados / total * 100 if total else 0
    
        print(f"\n{ruta_original.parent.name} ({ruta_original.name})")
        print(f"  total: {total:,}  |  eliminados: {eliminados:,} ({pct_elim:.1f}%)  |  conservados: {conservados:,}")
    
        # registramos operaciones exitosas
        linea_exito = crear_linea_log(ruta_original.name, "DELETE", eliminados, "OK")
        registrar_en_archivo(linea_exito)
        if conteo_motivos:
            print("  motivos:")
            for clave, n in conteo_motivos.items():
                print(f"    - {MOTIVOS[clave].strip()}: {n:,} ({n/total*100:.1f}%)")
    
        if errores:
            print(f"  errores inesperados: {len(errores)}")
    
            # registramos operaciones erroneas
            linea_error = crear_linea_log(ruta_original.name, "DELETE", len(errores), "ERROR")
            registrar_en_archivo(linea_error)
    

    except Exception as e: 
        #nueva linea de error (por cualquier otro fallo tecnico) 7.F
        linea_error = crear_linea_log(ruta_original.name, "DELETE", 0, "ERROR")
        registrar_en_archivo(linea_error)
        print(f"Error fatal en la limpieza: {e}")