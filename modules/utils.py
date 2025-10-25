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
        fecha_dt = datetime.strptime(evento["fecha"], "%Y-%m-%d")
    except ValueError:
        print("⚠️ La fecha debe tener el formato YYYY-MM-DD.")
        pause()
        return False

    # Validar formato de hora
    try:
        hora_dt = datetime.strptime(evento["hora"], "%H:%M")
    except ValueError:
        print("⚠️ La hora debe tener el formato HH:MM (24h).")
        pause()
        return False

    # Validar que la fecha/hora no sea en el pasado
    fecha_hora_completa = datetime.combine(fecha_dt.date(), hora_dt.time())
    if fecha_hora_completa < datetime.now():
        print("⚠️ La fecha y hora del evento no pueden ser en el pasado.")
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
        if e["nombre"].lower() == nuevo_evento["nombre"].lower():
            return True
    return False

def validar_disponibilidad_artista(artistas, id_artista, fecha, hora):
    if not id_artista or id_artista not in artistas:
        return True  # Si no hay artista asignado o no existe, se considera disponible
    # Verificar si el artista ya tiene un evento en la misma fecha y hora
    from administracion import cargar_eventos
    eventos = cargar_eventos()
    for e in eventos:
        if e.get("artista") == artistas[id_artista]["nombre"] and e["fecha"] == fecha and e["hora"] == hora:
            return False
    return True


