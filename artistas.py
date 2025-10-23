import json


def validar_nombre(nombre):
    return bool(nombre.strip())


def validar_tipo(tipo):
    return bool(tipo.strip())


def validar_duracion(duracion):
    if not duracion.isdigit():
        return False
    return int(duracion) > 0


def registrar_artista():
    print("Registro de Artista")

    nombre = input("Nombre del artista: ").strip()
    tipo_presentacion = input("Tipo de presentación: ").strip()
    duracion = input("Duración de la actuación (en minutos): ").strip()

   
    errores = []

    if not validar_nombre(nombre):
        errores.append(" El nombre no puede estar vacío.")
    if not validar_tipo(tipo_presentacion):
        errores.append(" El tipo de presentación no puede estar vacío.")
    if not validar_duracion(duracion):
        errores.append(" La duración debe ser un número entero positivo.")

    if errores:
        print("\n".join(errores))
        return

   
    artista = {
        "nombre": nombre,
        "tipo_presentacion": tipo_presentacion,
        "duracion_minutos": int(duracion)
    }

    
    with open("artista.json", "w", encoding="utf-8") as archivo:
        json.dump(artista, archivo, indent=4, ensure_ascii=False)

    print(" Artista registrado y guardado en 'artista.json'")


registrar_artista()