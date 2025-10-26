
import json
import os
from .artistas import registrar_artista
from modules.utils import (
    pedir_texto, pedir_fecha, pedir_hora, pedir_capacidad,
    validar_evento, validar_existencia, validar_disponibilidad_artista,
    pedir_categoria_n, pedir_nombre_n, pedir_fecha_n, pedir_hora_n, pedir_capacidad_n,
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


def crear_evento():
    """Crear evento con validaciones por campo y opción de reintento si algo falla."""
    clear_screen()
    print("🎉 ====== CREAR EVENTO ====== 🎉".center(50))

    while True:
        nombre = pedir_texto("Ingrese el nombre del evento: ")
        fecha = pedir_fecha("Ingrese la fecha (YYYY-MM-DD): ")
        hora = pedir_hora("Ingrese la hora (HH:MM): ")
        lugar = pedir_texto("Ingrese el lugar del evento: ")
        categoria = pedir_texto("Ingrese la categoría: ")
        capacidad = pedir_capacidad("Ingrese la capacidad: ")

        artistas = cargar_artistas()
        artista_asignado = None
        id_artista = None

        if artistas:
            print("\nArtistas disponibles:")
            for id_art, a in artistas.items():
                print(f"{id_art}. {a['nombre']} - {a['tipo_presentacion']}")

            while True:
                id_sel = input("Seleccione el ID del artista (ENTER para omitir): ").strip()
                if id_sel == "":
                    id_artista = None
                    artista_asignado = None
                    break
                if id_sel in artistas:
                    id_artista = id_sel
                    artista_asignado = artistas[id_artista]["nombre"]
                    if not validar_disponibilidad_artista(artistas, id_artista, fecha, hora):
                        print("❌ El artista no está disponible en la fecha/hora indicada. Elija otro artista o omita.")
                        continue
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
            print("⚠️ Ya existe un evento con el mismo nombre y fecha.")
            if input("¿Desea intentar de nuevo? (s/N): ").strip().lower() == "s":
                continue
            return

        if not validar_evento(nuevo_evento):
            print("⚠️ Error en los datos del evento. Se reiniciará el formulario.")
            if input("¿Desea reintentar? (s/N): ").strip().lower() == "s":
                continue
            return

        eventos.append(nuevo_evento)
        guardar_eventos(eventos)
        print("✅ Evento creado exitosamente ✅")
        pause()
        return

def listar_eventos():
    clear_screen()
    print("👀 ====== LISTAR EVENTOS ====== 👀".center(50))
    eventos= cargar_eventos()

    if not eventos:
        print("No hay eventos registrados.")
        pause() 
        return
    
    for e in eventos :
        print(f"{e['id']}. {e['nombre']} - {e['fecha']} {e['hora']} - {e['lugar']} - {e['artista']}")

def modificar_evento():
    """Modificar evento con validaciones inmediatas y opción de mantener valores anteriores."""
    clear_screen()
    listar_eventos()

    # Validar ID del evento en bucle
    while True:
        try:
            id_evento = int(input("\nIngrese el ID del evento a modificar (0 para cancelar): "))
            if id_evento == 0:
                print("Operación cancelada.")
                return
            eventos = cargar_eventos()
            evento_original = next((e for e in eventos if e["id"] == id_evento), None)
            if evento_original:
                break
            print("❌ No se encontró el evento.")
        except ValueError:
            print("❌ ID inválido. Debe ser un número.")

    # Crear copia para trabajar y mantener original para comparaciones
    evento = evento_original.copy()
    print("\n✏️ Edición del evento (deje vacío para mantener el valor actual):\n")

    # Modificar campos con validación inmediata
    while True:
        # Campos básicos con sus validadores
        evento["nombre"] = pedir_nombre_n(evento_original["nombre"])
        evento["fecha"] = pedir_fecha_n(evento_original["fecha"])
        evento["hora"] = pedir_hora_n(evento_original["hora"])
        evento["categoria"] = pedir_categoria_n(evento_original["categoria"])
        evento["capacidad"] = pedir_capacidad_n(evento_original["capacidad"])
        
        # Lugar (validación simple de no-vacío si se proporciona)
        nuevo_lugar = input(f"Nuevo lugar ({evento_original['lugar']}): ").strip()
        evento["lugar"] = nuevo_lugar if nuevo_lugar else evento_original["lugar"]

        # Artista (con validación de disponibilidad)
        artistas = cargar_artistas()
        if artistas:
            print("\nArtistas disponibles:")
            for id_art, a in artistas.items():
                print(f"{id_art}. {a['nombre']} - {a['tipo_presentacion']}")
            
            while True:
                nuevo_art = input(f"Nuevo artista (ID) [{evento_original['artista']}] (ENTER para mantener): ").strip()
                if not nuevo_art:  # Mantener artista actual
                    break
                if nuevo_art in artistas:
                    # Verificar disponibilidad solo si cambia artista o fecha/hora
                    if (nuevo_art != evento_original.get("artista") or 
                        evento["fecha"] != evento_original["fecha"] or 
                        evento["hora"] != evento_original["hora"]):
                        
                        if not validar_disponibilidad_artista(artistas, nuevo_art, evento["fecha"], evento["hora"]):
                            print("❌ El artista no está disponible en esa fecha/hora.")
                            if input("¿Desea elegir otro artista? (s/N): ").strip().lower() != "s":
                                break
                            continue
                    evento["artista"] = artistas[nuevo_art]["nombre"]
                    break
                print("❌ Artista no encontrado.")
                if input("¿Desea elegir otro artista? (s/N): ").strip().lower() != "s":
                    break

        # Validación final
        if not validar_evento(evento):
            print("⚠️ Los datos modificados no son válidos.")
            if input("¿Desea intentar de nuevo? (s/N): ").strip().lower() != "s":
                return
            continue

        # Verificar duplicados solo si cambió nombre o fecha
        if (evento["nombre"] != evento_original["nombre"] or 
            evento["fecha"] != evento_original["fecha"]):
            otros_eventos = [e for e in eventos if e["id"] != id_evento]
            if validar_existencia(otros_eventos, evento):
                print("⚠️ Ya existe otro evento con el mismo nombre y fecha.")
                if input("¿Desea intentar con otros datos? (s/N): ").strip().lower() != "s":
                    return
                continue

        # Todo válido: actualizar y guardar
        for i, e in enumerate(eventos):
            if e["id"] == id_evento:
                eventos[i] = evento
                break
                
        guardar_eventos(eventos)
        print("✅ Evento actualizado correctamente ✅")
        pause()
        return

    
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



    

