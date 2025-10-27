import json
import os
from .administracion import crear_evento, modificar_evento, eliminar_evento, listar_eventos, generar_reporte
from .artistas import registrar_artista
from .asistentes import cargar_asistentes, registrar_asistente
from modules.utils import clear_screen, pause 


def menu_asistente():
    clear_screen()
    while True:
        print("\n🎟️ --- Menú de Asistente --- 🎟️")
        print("1. 📅 Mostrar Eventos y Registrarme")
        print("2. 🚪 Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("⚠️ Función aún no disponible...")
            pause()
        elif opcion == "2":
            print("👋 Saliendo del menú de asistente...")
            pause()
            break
        else:
            print("❌ Opción inválida. Intente nuevamente.")
            pause()

def menu_admin():
    while True:
        clear_screen()
        print("\n🔧 ===== PANEL DE ADMINISTRADOR ===== 🔧")
        print("1. ➕ Crear evento")
        print("2. ✏️ Modificar evento")
        print("3. 🗑️ Eliminar evento")
        print("4. 👀 Ver eventos")
        print("5. 🎤 Registrar artistas")
        print("6. 📊 Generar reporte")
        print("7. 🚪 Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_evento()
        elif opcion == "2":
            modificar_evento()
        elif opcion == "3":
            eliminar_evento()
        elif opcion == "4":
            listar_eventos()
        elif opcion == "5":
            registrar_artista()
        elif opcion == "6":
            generar_reporte()
        elif opcion == "7":
            print("👋 Saliendo del panel de administrador...")
            pause()
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")
            pause()

def login():
    while True:
        clear_screen()
        print("\n🔐 --- Login --- 🔐")
        print("1. 👨‍💼 Iniciar sesión como Administrador")
        print("2. 🎟️ Iniciar sesión como Asistente")
        print("3. 📝 Registrar como Asistente")
        print("4. 🎤 Iniciar sesión como Artista")
        print("5. 🚪 Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            usuario = input("👤 Ingrese usuario: ").strip()
            if usuario == "admin":
                menu_admin()
            else:
                print("❌ Usuario incorrecto.")
                pause()
        elif opcion == "2":
            asistentes = cargar_asistentes()
            if not asistentes:
                print("⚠️ No hay asistentes registrados. Regístrese primero.")
                pause()
                continue
            id_asistente = input("🆔 Ingrese su ID de identificación: ").strip()
            if id_asistente in asistentes:
                print(f"✅ Bienvenido, {asistentes[id_asistente]['nombre']}.")
                pause()
                menu_asistente()
            else:
                print("❌ ID no encontrado. Regístrese primero.")
                pause()
        elif opcion == "3":
            resultado = registrar_asistente()
            if resultado:
                print("✅ Registro completado. Ahora puede iniciar sesión como asistente.")
                pause()
            else:
                print("ℹ️ Registro no completado.")
                pause()
            pause()
        elif opcion == "4":
            print("⚠️ Función aún no disponible...")
            pause()
        elif opcion == "5":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida.")
            pause()
