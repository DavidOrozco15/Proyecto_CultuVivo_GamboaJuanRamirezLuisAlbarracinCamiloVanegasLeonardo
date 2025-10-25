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
    # Identificación: solo números y única
    while True:
        identificacion = pedir_identificacion("Ingrese su número de identificación: ")
        if identificacion in asistentes:
            print("❌ Ya existe un asistente con esa identificación.")
            if input("¿Desea intentar con otra identificación? (s/N): ").strip().lower() != "s":
                return
            continue
        break

    # Nombre: solo letras y espacios
    while True:
        nombre = input("Ingrese su nombre completo: ").strip()
        if not nombre:
            print("❌ El nombre no puede estar vacío.")
            continue
        patron_nombre = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$')
        if not patron_nombre.match(nombre):
            print("❌ El nombre sólo puede contener letras y espacios. Intente de nuevo.")
            continue
        break

    # Correo: ya existe loop; mantener
    while True:
        correo = input("Ingrese su correo electronico: ").strip()
        if validar_correo(correo):
            break
        print("ERROR: El correo electrónico no es válido. Por favor, inténtelo de nuevo.")

    # Tipo de boleto: validar opción permitida
    tipos_permitidos = {"General", "Vip", "Cortesia"}
    while True:
        tipo_boleto = input("Ingrese el tipo de boleto (General/Vip/Cortesia): ").strip().capitalize()
        if not tipo_boleto:
            print("❌ El tipo de boleto no puede estar vacío.")
            continue
        if tipo_boleto not in tipos_permitidos:
            print(f"❌ Tipo de boleto inválido. Opciones: {', '.join(tipos_permitidos)}")
            continue
        break

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
