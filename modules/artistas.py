import json
import re
import os
from modules.utils import clear_screen, pause, pedir_identificacion, validar_identificacion

archivoJson = "data/artistas.json"

def lista_artista(nombre_a=archivoJson):
    if not os.path.exists(nombre_a):
        return {}
    with open(nombre_a, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def guardar_artista(nRegistro, datos, nombre_a=archivoJson):
    registros = lista_artista()
    registros[str(nRegistro)] = datos
    with open(nombre_a, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=4, ensure_ascii=False)

def validar_registro(nRegistro):
    """Valida que el registro sea numérico."""
    return validar_identificacion(nRegistro)


def validar_nombre(nombre):
    if not isinstance(nombre, str):
        return False
    n = nombre.strip()
    if not n:
        return False
    patron = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$')
    return bool(patron.match(n))


def validar_tipo(tipo):
    return bool(tipo.strip())


def validar_duracion(duracion):
    if not duracion.isdigit():
        return False
    return int(duracion) > 0


def registrar_artista():
    clear_screen()
    artista = lista_artista()

    print("🎤 ㅤㅤㅤㅤRegistro de Artistaㅤㅤㅤㅤ 🎤")

    while True:
        nRegistro = pedir_identificacion("Ingrese su número de registro: ")
        if nRegistro in artista:
            print("❌ El número de registro ya se encuentra registrado")
            if input("¿Desea intentar con otro número? (s/N): ").strip().lower() != "s":
                return
            continue
        break

    while True:
        nombre = input("Nombre del artista: ").strip()
        if validar_nombre(nombre):
            break
        print("❌ El nombre debe contener solo letras y espacios.")

    while True:
        tipo_presentacion = input("Tipo de presentación: ").strip()
        if validar_tipo(tipo_presentacion):
            break
        print("❌ El tipo de presentación no puede estar vacío.")

    while True:
        duracion = input("Duración de la actuación (en minutos): ").strip()
        if validar_duracion(duracion):
            break
        print("❌ La duración debe ser un número entero positivo.")

   
    datos_artista = {
        
        "nombre": nombre,
        "tipo_presentacion": tipo_presentacion,
        "duracion_minutos": int(duracion)
    }
    guardar_artista(nRegistro, datos_artista)
    print("El artista se ha registrado exitosamente.")
    pause()
