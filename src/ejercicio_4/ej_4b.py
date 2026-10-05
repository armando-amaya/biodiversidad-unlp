def generar_registro_vacio(columnas):
    """
    Esta función recibe una lista de columnas de un dataset y retorna un
    diccionario con sus valores inicializados con None, " ", 0, entre otros.
    columnas: list, lista de los encabezados de las columnas de un dataset(2.B).
    valor: valor para iniciar (None, "" , 0)
    """
    # creamos diccionario {encabezados : (None, " ", 0)}
    # no incluimos "id"
    registro = {col: None
                for col in columnas 
                if col != "id" and col != "gbifID"}

    return registro