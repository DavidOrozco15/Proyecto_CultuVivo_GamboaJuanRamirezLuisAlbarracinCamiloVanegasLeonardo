import json
import re
import os

ARCHIVO_JSON = "asistentes.json"

def cargar_asistentes():
    if not os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []
    

def guardar_asistentes(asistentes):
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(asistentes, f, indent=4, ensure_ascii=False) 

def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None