from asistentes import registrar_asistente

if __name__ == "__main__":
    while True:
        print("\n--- Menú de Registro de Asistentes ---")
        print("1. Registrar asistente")
        print("2. Mostrar Eventos y Registrarme")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_asistente()
        elif opcion == "2":
            print("Funcion aun no disponible...")
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

from administracion import crear_evento, modificar_evento, eliminar_evento, listar_eventos

def menu_admin():
    while True:
        print("\n===== PANEL DE ADMINISTRADOR =====")
        print("1. Crear evento")
        print("2. Modificar evento")
        print("3. Eliminar evento")
        print("4. Ver eventos")
        print("5. Salir")

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
            print("👋 Saliendo del panel de administrador...")
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu_admin()
