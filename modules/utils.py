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

# mejora pedida por el scrum master
def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("❌ Este campo no puede estar vacío.")


def pedir_fecha(mensaje):
    while True:
        fecha = input(mensaje).strip()
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return fecha
        except ValueError:
            print("❌ Fecha inválida. Ejemplo correcto: 2025-10-24")


def pedir_hora(mensaje):
    while True:
        hora = input(mensaje).strip()
        try:
            datetime.strptime(hora, "%H:%M")
            return hora
        except ValueError:
            print("❌ Hora inválida. Ejemplo correcto: 19:30")


def pedir_capacidad(mensaje):
    while True:
        capacidad = input(mensaje).strip()
        if capacidad.isdigit() and int(capacidad) > 0:
            return capacidad
        print("❌ Capacidad inválida. Solo números mayores a 0.")

# VALIDACIONES OBJETO EVENTO

def validar_evento(evento):
    try:
        datetime.strptime(evento["fecha"], "%Y-%m-%d")
        datetime.strptime(evento["hora"], "%H:%M")
        if not int(evento["capacidad"]) > 0:
            print("❌ Capacidad debe ser un número positivo.")
            return False
    except:
        print("❌ Error de validación en los datos del evento.")
        return False
    
    return True


def validar_existencia(eventos, nuevo):
    for e in eventos:
        if e["nombre"].lower() == nuevo["nombre"].lower() and e["fecha"] == nuevo["fecha"]:
            return True
    return False

def pedir_nombre_n(valor_actual=None):
    while True:
        nombre = input(f"Nuevo nombre ({valor_actual}): ").strip() if valor_actual else input("Nombre del evento: ").strip()
        if not nombre and valor_actual:
            return valor_actual
        if nombre and nombre.replace(" ", "").isalpha():
            return nombre
        print("❌ Nombre inválido. Solo letras.")

def pedir_categoria_n(valor_actual=None):
    while True:
        categoria = input(f"Nueva categoría ({valor_actual}): ").strip() if valor_actual else input("Categoría: ").strip()
        if not categoria and valor_actual:
            return valor_actual
        if categoria:
            return categoria
        print("❌ Categoría no puede estar vacía.")

def pedir_fecha_n(valor_actual=None):
    while True:
        fecha = input(f"Nueva fecha ({valor_actual}): ").strip() if valor_actual else input("Fecha (YYYY-MM-DD): ").strip()
        if not fecha and valor_actual:
            return valor_actual
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return fecha
        except ValueError:
            print("❌ Fecha inválida. Ejemplo: 2025-10-25")

def pedir_hora_n(valor_actual=None):
    while True:
        hora = input(f"Nueva hora ({valor_actual}): ").strip() if valor_actual else input("Hora (HH:MM): ").strip()
        if not hora and valor_actual:
            return valor_actual
        try:
            datetime.strptime(hora, "%H:%M")
            return hora
        except ValueError:
            print("❌ Hora inválida. Ejemplo: 14:30")

def pedir_capacidad_n(valor_actual=None):
    while True:
        capacidad = input(f"Nueva capacidad ({valor_actual}): ").strip() if valor_actual else input("Capacidad: ").strip()
        if not capacidad and valor_actual:
            return valor_actual
        if capacidad.isdigit() and int(capacidad) > 0:
            return int(capacidad)
        print("❌ Capacidad inválida (solo números positivos).")

# huevo de pascua jejejeje