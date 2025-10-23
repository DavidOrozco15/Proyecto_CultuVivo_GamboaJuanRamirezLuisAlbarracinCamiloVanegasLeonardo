import json
import re
import os

ARCHIVO_JSON = "asistentes.json"

def estructura_asistente():
    return {
        "identificacion": "",
        "nombre": "",
        "correo": "",
        "tipo_boleto": "",
        "estado": "En espera"
    }

def cargar_asistentes(nombre_a=ARCHIVO_JSON):
    if not os.path.exists(nombre_a):
        datos = estructura_asistente()
        guardar_asistentes(datos, nombre_a)
        return datos
    with open(nombre_a, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            datos = estructura_asistente()
            guardar_asistentes(datos, nombre_a)
            return datos

    

def guardar_asistentes(data, nombre_a=ARCHIVO_JSON):
    with open(nombre_a, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None

def registrar_asistente():

    asistentes = cargar_asistentes()

    print("===REGISTRO DE ASISTENTE===")

    identificacion = input("ingrese su numero de identifeicacion: ").strip
    nombre = input("Ingrese su nombre completo: ").strip()
    correo = input("Ingrese su correo electronico: ").strip()
    tipo_boleto = input("Ingrese el tipo de boleto (general/VIP/Cortesia): ").strip().capitalize()

    if not identificacion or not nombre or not correo or not tipo_boleto:
        print("ERROR: Todos los campos son obligatorios.")
        return
    
    if not validar_correo(correo):
        print("ERROR: El correo electronico no es valido.")
        return
    
    for asistente in asistentes:
        if asistente["identificacion"] == identificacion:
            print("ERROR: Ya existe un asistente con esa identificacion.")
            return
        
    confirmar = input("Desea confirmar el registro? (s/n): ").lower()    
    if confirmar != "s":
        print("El registro ha sido cancelado.")
        return
    
    nuevo_asistente = {
        "identificacion": identificacion,
        "nombre": nombre,
        "correo": correo,
        "tipo_boleto": tipo_boleto,
        "estado": "En espera"
    }

    asistentes.append(nuevo_asistente)
    guardar_asistentes(asistentes)
    print("Registro exitoso, su estado es: En espera.")

def mostrar_asistentes():
    asistentes = cargar_asistentes()
    if not asistentes:
        print("No hay asistentes registrados.")
        return
    
    print("===LISTA DE ASISTENTES===")
    for idx, asistente in enumerate(asistentes, start=1):
        print(f"\nAsistente #{idx}")
        print(f"Identificación: {asistente['identificacion']}")
        print(f"Nombre: {asistente['nombre']}")
        print(f"Correo: {asistente['correo']}")
        print(f"Tipo de Boleto: {asistente['tipo_boleto']}")
        print(f"Estado: {asistente['estado']}")    

if __name__ == "__main__":
    while True:
        print("\n--- Menú de Registro de Asistentes ---")
        print("1. Registrar asistente")
        print("2. Mostrar asistentes")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_asistente()
        elif opcion == "2":
            mostrar_asistentes()
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")