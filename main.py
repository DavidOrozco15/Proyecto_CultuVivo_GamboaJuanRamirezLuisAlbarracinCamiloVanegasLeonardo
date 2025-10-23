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
