import json
import re
import os
from modules.utils import validar_correo, clear_screen, pause, pedir_identificacion


ARCHIVO_JSON = "data/asistentes.json"

def cargar_asistentes(nombre_a=ARCHIVO_JSON):
    if not os.path.exists(nombre_a):
        return {}
    with open(nombre_a, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def guardar_asistentes(data, nombre_a=ARCHIVO_JSON):
    with open(nombre_a, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def registrar_asistente():
    clear_screen()
    asistentes = cargar_asistentes()

    print("===REGISTRO DE ASISTENTE===")

    while True:
        identificacion = pedir_identificacion("Ingrese su número de identificación: ")
        if identificacion in asistentes:
            print("❌ Ya existe un asistente con esa identificación.")
            if input("¿Desea intentar con otra identificación? (s/N): ").strip().lower() != "s":
                return
            continue
        break
    
    nombre = input("Ingrese su nombre completo: ").strip()
    
    
    while True:
        correo = input("Ingrese su correo electronico: ").strip()
        if validar_correo(correo):
            break
        print("ERROR: El correo electrónico no es válido. Por favor, inténtelo de nuevo.")
    
    tipo_boleto = input("Ingrese el tipo de boleto (general/VIP/Cortesia): ").strip().capitalize()

    if not identificacion or not nombre or not tipo_boleto:
        print("ERROR: Todos los campos son obligatorios.")
        return

    if identificacion in asistentes:
        print("ERROR: Ya existe un asistente con esa identificacion.")
        return

    confirmar = input("Desea confirmar el registro? (s/n): ").lower()
    if confirmar != "s":
        print("El registro ha sido cancelado.")
        return

    nuevo_asistente = {
        "nombre": nombre,
        "correo": correo,
        "tipo_boleto": tipo_boleto,
        "estado": "En espera"
    }

    asistentes[identificacion] = nuevo_asistente
    guardar_asistentes(asistentes)
    print("Registro exitoso, su estado es: En espera.")
    pause()

"""def mostrar_asistentes():
    asistentes = cargar_asistentes()
    if not asistentes:
        print("No hay asistentes registrados.")
        return

    print("===LISTA DE ASISTENTES===")
    for idx, (identificacion, asistente) in enumerate(asistentes.items(), start=1):
        print(f"\nAsistente #{idx}")
        print(f"Identificación: {identificacion}")
        print(f"Nombre: {asistente['nombre']}")
        print(f"Correo: {asistente['correo']}")
        print(f"Tipo de Boleto: {asistente['tipo_boleto']}")
        print(f"Estado: {asistente['estado']}")"""
