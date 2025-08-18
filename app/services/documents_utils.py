import os
import json

documents = []

def cargar_documento():
    try:
        carpeta = "files"

        # Crea la carpeta si no existe
        if not os.path.exists(carpeta):
            os.mkdir(carpeta)
            
        for archivo in os.listdir(carpeta):
            if archivo.lower().endswith(".pdf"):
                documents.append(archivo)
                        
    except Exception as error:
        return json({f"Error leyendo un archivo: {error}"})