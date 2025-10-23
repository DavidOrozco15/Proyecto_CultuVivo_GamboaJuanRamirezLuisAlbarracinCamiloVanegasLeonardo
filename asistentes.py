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