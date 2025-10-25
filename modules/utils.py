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
    """Valida que todos los campos del evento sean válidos y consistentes."""
    # Validar campos requeridos no vacíos
    campos_requeridos = ["nombre", "fecha", "hora", "lugar", "categoria", "capacidad"]
    for campo in campos_requeridos:
        if not str(evento.get(campo, "")).strip():
            print(f"⚠️ El campo '{campo}' no puede estar vacío.")
            pause()
            return False

    # Validar formato de fecha y que no sea pasada
    try:
        fecha_dt = datetime.strptime(evento["fecha"], "%Y-%m-%d")
        hora_dt = datetime.strptime(evento["hora"], "%H:%M")
        fecha_hora = datetime.combine(fecha_dt.date(), hora_dt.time())
        if fecha_hora < datetime.now():
            print("⚠️ La fecha y hora del evento no pueden ser en el pasado.")
            pause()
            return False
    except ValueError as e:
        print(f"⚠️ Formato de fecha/hora inválido: {str(e)}")
        pause()
        return False

    # Validar capacidad (debe ser int en el evento)
    if not isinstance(evento["capacidad"], int) or evento["capacidad"] <= 0:
        print("⚠️ La capacidad debe ser un número entero positivo.")
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

# Funciones de validación y entrada mejoradas
def validar_texto_no_vacio(texto):
    """Valida que un texto no esté vacío después de quitar espacios."""
    return bool(str(texto or "").strip())

def pedir_texto(mensaje, validacion_extra=None):
    """Pide texto con validación de no vacío y opcionalmente una validación extra."""
    while True:
        texto = input(mensaje).strip()
        if not validar_texto_no_vacio(texto):
            print("❌ Este campo no puede estar vacío.")
            continue
        if validacion_extra and not validacion_extra(texto):
            continue
        return texto


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
    """Pide y valida una capacidad como entero positivo."""
    while True:
        capacidad = input(mensaje).strip()
        try:
            capacidad_int = int(capacidad)
            if capacidad_int > 0:
                return capacidad_int  # Retorna int, no string
            print("❌ La capacidad debe ser mayor que 0.")
        except ValueError:
            print("❌ Capacidad inválida. Ingrese un número entero positivo.")

def validar_id_artista(artistas, id_artista):
    """Valida que un ID de artista exista y esté activo."""
    if not id_artista:  # Permitir omitir artista
        return True
    return id_artista in artistas

def validar_existencia(eventos, nuevo):
    """Valida que no exista un evento con el mismo nombre en la misma fecha."""
    return any(
        e["nombre"].lower() == nuevo["nombre"].lower() and e["fecha"] == nuevo["fecha"]
        for e in eventos
    )

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