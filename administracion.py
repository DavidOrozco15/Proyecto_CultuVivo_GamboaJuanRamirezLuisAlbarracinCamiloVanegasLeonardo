
import json
import os
from artistas import registrar_artista
from modules.utils import (
    pedir_texto, pedir_fecha, pedir_hora, pedir_capacidad,
    validar_evento, validar_existencia, pedir_categoria_n, pedir_nombre_n,
    pedir_fecha_n, pedir_hora_n, pedir_capacidad_n,
    clear_screen, pause
)

RUTA_JSON = os.path.join(os.path.dirname(__file__), "data/eventos.json")

def cargar_eventos():
    if not os.path.exists(RUTA_JSON):
        return []
    with open(RUTA_JSON, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Error al leer eventos.json. El archivo puede estar corrupto. Se cargará una lista vacía.")
            pause()
            return []

def guardar_eventos(eventos):
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=4, ensure_ascii=False)

def cargar_artistas():
    ruta_artistas = os.path.join(os.path.dirname(__file__), "data/artistas.json")
    if not os.path.exists(ruta_artistas):
        print("⚠️ No existe artistas.json. No se podrán asignar artistas.")
        return {}
    with open(ruta_artistas, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Error al leer artistas.json")
            return {}


def crear_evento ():
    clear_screen()
    print("====== CREAR EVENTO ======".center(50))

    nombre = pedir_texto("Ingrese el nombre del evento: ")
    fecha = pedir_fecha("Ingrese la fecha (YYYY-MM-DD): ")
    hora = pedir_hora("Ingrese la hora (HH:MM): ")
    lugar = pedir_texto("Ingrese el lugar del evento: ")
    categoria = pedir_texto("Ingrese la categoría: ")
    capacidad = pedir_capacidad("Ingrese la capacidad: ")

    artistas = cargar_artistas()
    artista_asignado = None

    if artistas:
        print("\nArtistas disponibles:")
        for id_art, a in artistas.items():
            print(f"{id_art}. {a['nombre']} - {a['tipo_presentacion']}")

        while True:
            id_artista = input("Seleccione el ID del artista: ").strip()
            if id_artista in artistas:
                artista_asignado = artistas[id_artista]["nombre"]
                break
            print("❌ Artista no encontrado, intente de nuevo.")

    nuevo_evento = {
        "id": len(cargar_eventos()) + 1,
        "nombre": nombre,
        "fecha": fecha,
        "hora": hora,
        "lugar": lugar,
        "categoria": categoria,
        "capacidad": capacidad,
        "artista": artista_asignado
    }

    eventos = cargar_eventos()
    if validar_existencia(eventos, nuevo_evento):
        print("⚠️ El evento ya existe.")
        return

    eventos.append(nuevo_evento)
    guardar_eventos(eventos)
    print("✅ Evento creado exitosamente ✅")
    pause()

def listar_eventos():
    clear_screen()
    print("====== LISTAR EVENTOS ======".center(50))
    eventos= cargar_eventos()

    if not eventos:
        print("No hay eventos registrados.")
        pause() 
        return
    
    for e in eventos :
        print(f"{e['id']}. {e['nombre']} - {e['fecha']} {e['hora']} - {e['lugar']} - {e['artista']}")

def modificar_evento():
    clear_screen()
    listar_eventos()

    try:
        id_evento = int(input("\nIngrese el ID del evento a modificar: "))
    except ValueError:
        print("❌ ID inválido.")
        return
    
    eventos = cargar_eventos()
    evento = next((e for e in eventos if e["id"] == id_evento), None)
    if not evento:
        print("❌ No se encontró el evento.")
        return

    print("\n✏️ Edición del evento (deje vacío para mantener el anterior):\n")

    evento["nombre"] = pedir_nombre_n(evento["nombre"])
    evento["fecha"] = pedir_fecha_n(evento["fecha"])
    evento["hora"] = pedir_hora_n(evento["hora"])
    evento["lugar"] = input(f"Nuevo lugar ({evento['lugar']}): ").strip() or evento["lugar"]
    evento["categoria"] = pedir_categoria_n(evento["categoria"])
    evento["capacidad"] = pedir_capacidad_n(evento["capacidad"])

    artistas = cargar_artistas()
    if artistas:
        print("\nArtistas disponibles:")
        for id_art, a in artistas.items():
            print(f"{id_art}. {a['nombre']} - {a['tipo_presentacion']}")
        
        nuevo_art = input(f"Nuevo artista (ID) [{evento['artista']}]: ").strip()
        if nuevo_art in artistas:
            evento["artista"] = artistas[nuevo_art]["nombre"]

    guardar_eventos(eventos)
    print("✅ Evento actualizado correctamente ✅")

    
def eliminar_evento():
    clear_screen()
    listar_eventos()
    while True:
        try:
            id_evento = int(input("\nIngrese el ID del evento a eliminar: "))
            break
        except ValueError:
            print("❌ ID inválido. Intente nuevamente.")
            pause()

    eventos = cargar_eventos()
    nuevos = [e for e in eventos if e["id"] != id_evento]

    if len(nuevos) == len(eventos):
        print("❌ No se encontró el evento.")
        pause()
        return

    guardar_eventos(nuevos)
    print("🗑️ Evento eliminado correctamente.")
    pause()

def generar_reporte():
    clear_screen()
    eventos =cargar_eventos()

    if not eventos :
        print ("no hay eventos para generar reportes.")
        pause()
        return
    
    print ("\n"+ " REPORTE DE EVENTOS ".center(50,"="))

    for e in eventos:
        print("\n"+ "-"*60)
        print(f"\n📌 Tipo/categoria : {e['categoria']}")
        print(f"🏷️ Nombre del evento : {e['nombre']}")
        print(f"👥 Capacidad : {e['capacidad']}")
        print(f"🎙️ artista : {e['artista'] if e ['artista'] else 'sin artista registrado'}")

        print(f"\nℹ️ informacion del evento:")
        
        print (f"\n🏦 lugar: {e['lugar']}")
        print(f"📆 fecha: {e['fecha']}")
        print(f"⏰ hora: {e['hora']}")

    print ("\n✅Reporte generado con exito ")



    

