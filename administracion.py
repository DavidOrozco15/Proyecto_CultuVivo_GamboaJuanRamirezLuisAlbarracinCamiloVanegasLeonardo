
import json
import os
from modules.utils import validar_evento, validar_existencia
from artistas import registrar_artista

RUTA_JSON = os.path.join(os.path.dirname(__file__), "data/eventos.json")

def cargar_eventos():
    if not os.path.exists(RUTA_JSON):
        return []
    with open(RUTA_JSON, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
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
    print("====== CREAR EVENTO ======".center(50))
    nombre = input("Ingrese el nombre del evento: ").strip()
    fecha = input("Ingrese la fecha del evento (YYYY-MM-DD): ").strip()
    hora = input("Ingrese la hora del evento (HH:MM): ").strip()
    lugar = input("Ingrese el lugar del evento: ").strip()
    categoria= input("ingrese la categoria del evento: ").strip()
    capacidad= input ("ingrese la capacidad del evento: ").strip()


    artistas = cargar_artistas()
    artista_asignado = None

    if artistas:
        print("\nArtistas disponibles:")
        for id_art, a in artistas.items():
            print(f"{id_art}. {a['nombre']} - {a['tipo_presentacion']}")

        id_artista = input("Seleccione el ID del artista: ").strip()
        if id_artista in artistas:
            artista_asignado = artistas[id_artista]["nombre"]
        else:
            print("⚠️ Artista no encontrado. Se asignará None.")

    nuevo_evento = {
        "id": len(cargar_eventos()) + 1,
        "nombre": nombre,
        "fecha": fecha,
        "hora": hora,
        "lugar": lugar,
        "categoria": categoria,
        "capacidad": capacidad,
        "artista":  artista_asignado
    }

    if not validar_evento(nuevo_evento):
        return

    eventos= cargar_eventos()

    if validar_existencia(eventos, nuevo_evento):
        print("⚠️ El evento ya existe.")
        return
    
    eventos.append(nuevo_evento)
    guardar_eventos(eventos)
    print("✅ Evento creado exitosamente.")

def listar_eventos():

    print("====== LISTAR EVENTOS ======".center(50))
    eventos= cargar_eventos()

    if not eventos:
        print("No hay eventos registrados.")
        return
    
    for e in eventos :
        print(f"{e['id']}. {e['nombre']} - {e['fecha']} {e['hora']} - {e['lugar']} - {e['artista']}")

def modificar_evento():
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

    print("Deje vacío si no desea cambiar un campo.")
    nombre = input(f"Nuevo nombre ({evento['nombre']}): ").strip() or evento['nombre']
    fecha = input(f"Nueva fecha ({evento['fecha']}): ").strip() or evento['fecha']
    hora = input(f"Nueva hora ({evento['hora']}): ").strip() or evento['hora']
    lugar = input(f"Nuevo lugar ({evento['lugar']}): ").strip() or evento['lugar']
    categoria = input(f"Nueva categoría ({evento['categoria']}): ").strip() or evento['categoria']
    capacidad = input(f"Nueva capacidad ({evento['capacidad']}): ").strip() or evento['capacidad']
    artistas = cargar_artistas()
    if artistas:
        print("\nArtistas disponibles:")
        for id_art, a in artistas.items():
            print(f"{id_art}. {a['nombre']} - {a['tipo_presentacion']}")
        nuevo_artista = input(f"Nuevo artista (ID) [{evento['artista']}]: ").strip()
        if nuevo_artista in artistas:
            artista = artistas[nuevo_artista]["nombre"]
        else:
            artista = evento['artista']
    else:
        artista = evento['artista']
    actualizado = {
        "id": evento["id"],
        "nombre": nombre,
        "fecha": fecha,
        "hora": hora,
        "lugar": lugar,
        "categoria": categoria,
        "capacidad": capacidad,
        "artista": artista
    }

    if not validar_evento(actualizado):
        return

    for i, e in enumerate(eventos):
        if e["id"] == id_evento:
            eventos[i] = actualizado
            break

    guardar_eventos(eventos)
    print("✅ Evento actualizado correctamente.")

def eliminar_evento():
    listar_eventos()
    try:
        id_evento = int(input("\nIngrese el ID del evento a eliminar: "))
    except ValueError:
        print("❌ ID inválido.")
        return

    eventos = cargar_eventos()
    nuevos = [e for e in eventos if e["id"] != id_evento]

    if len(nuevos) == len(eventos):
        print("❌ No se encontró el evento.")
        return

    guardar_eventos(nuevos)
    print("🗑️ Evento eliminado correctamente.")

def generar_reporte():
    eventos =cargar_eventos()

    if not eventos :
        print ("no hay eventos para generar reportes.")
        return
    
    print ("\n"+ " REPORTE DE EVENTOS ".center(50,"="))

    total_eventos = len (eventos)
    print(f" total de eventos registrados: {total_eventos}")

    categorias= {}
    for e in eventos :
        cat = e ["categoria"]
        categorias[cat] = categorias.get(cat,0)+1

    print("\n eventos por categoria:")
    for cat, cant in categorias.items():
        print(f" - {cat}: {cant} evento(s)")

    eventos_con_artista = [ e for e in eventos if e ["artista"]]
    print(f"\n eventos con artista asignado: {len(eventos_con_artista)}")

    try:
        capacidad_total = sum(int(e["capacidad"])for e in eventos)

    except:
        capacidad_total = "error en datos de capacidad"

    print (f"\n capacidad total disponible: {capacidad_total}")
    print ("\n Reporte echo correctamente")

    

