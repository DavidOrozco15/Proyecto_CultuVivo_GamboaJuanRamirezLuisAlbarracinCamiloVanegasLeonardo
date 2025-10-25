import re
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("Presione Enter para continuar...")

def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None

from datetime import datetime

def validar_evento(evento):
    for campo, valor in evento.items():
        if campo != "id" and not str(valor).strip():
            print(f"⚠️ El campo '{campo}' no puede estar vacío.")
            pause()
            return False

    # Validar formato de fecha
    try:
        datetime.strptime(evento["fecha"], "%Y-%m-%d")
    except ValueError:
        print("⚠️ La fecha debe tener el formato YYYY-MM-DD.")
        pause()
        return False

    # Validar formato de hora
    try:
        datetime.strptime(evento["hora"], "%H:%M")
    except ValueError:
        print("⚠️ La hora debe tener el formato HH:MM (24h).")
        pause()
        return False

    # Validar capacidad numérica
    try:
        if int(evento["capacidad"]) <= 0:
            print("⚠️ La capacidad debe ser un número positivo.")
            pause()
            return False
    except ValueError:
        print("⚠️ La capacidad debe ser un número entero.")
        pause()
        return False

    return True

def validar_existencia(eventos, nuevo_evento):
    for e in eventos:
        if e["nombre"].lower() == nuevo_evento["nombre"].lower() and e["fecha"] == nuevo_evento["fecha"]:
            return True
    return False


