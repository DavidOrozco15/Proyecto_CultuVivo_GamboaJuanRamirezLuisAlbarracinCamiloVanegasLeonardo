import json
import re
import os


archivoJson = "artistas.json"

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
    if not nRegistro.isdigit():
        return False
    return int(nRegistro)


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
    artista = lista_artista()
    
    print("ㅤㅤㅤㅤRegistro de Artistaㅤㅤㅤㅤ")

    
    nRegistro = input("Ingrese su numero de registro: ").strip()
    nombre = input("Nombre del artista: ").strip()
    tipo_presentacion = input("Tipo de presentación: ").strip()
    duracion = input("Duración de la actuación (en minutos): ").strip()

   
    errores = []

    if not validar_registro(nRegistro):
        errores.append(" El Nro. de registro deben ser solo numeros.")
    if nRegistro in artista:
        errores.append("El numero de registro ya se encuentra registrado")
    if not validar_nombre(nombre):
        errores.append(" El nombre deben ser solo letras.")
    if not validar_tipo(tipo_presentacion):
        errores.append(" El tipo de presentación no puede estar vacío.")
    if not validar_duracion(duracion):
        errores.append(" La duración debe ser un número entero positivo.")

    if errores:
        print("\n".join(errores))
        return

   
    datos_artista = {
        
        "nombre": nombre,
        "tipo_presentacion": tipo_presentacion,
        "duracion_minutos": int(duracion)
    }
    guardar_artista(nRegistro, datos_artista)
    print("El artista se ha registrado exitosamente.")







if __name__ == "__main__":
    registrar_artista()