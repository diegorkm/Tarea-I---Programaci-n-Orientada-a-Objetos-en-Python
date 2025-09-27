from dungeon_generator import (Habitacion, Mapa, Explorador, Visualizador,guardar_partida, cargar_partida)

def main():
    # Parámetros básicos
    ancho = 10
    alto = 10
    numero_habitaciones = 20
    archivo_json = "partida.json"

    # Crear mapa
    mapa = Mapa(
        ancho=ancho,
        alto=alto,
        habitaciones={},
        habitacion_inicial=Habitacion(
            id=0, x=0, y=0, inicial=False, contenido=None, conexiones={}, visitada=False
        ),
    )

    print("Generando estructura del mapa")
    mapa.generar_estructura(numero_habitaciones)

    print("Colocando contenido monstruos, tesoros, eventos y jefe")
    mapa.colocar_contenido()

    # Crear el explorador en la habitación inicial
    pos_ini = (mapa.habitacion_inicial.x, mapa.habitacion_inicial.y)
    explorador = Explorador(vida=5, inventario=[], posicion_actual=pos_ini, mapa=mapa)

    # Visualizador
    visualizarCosas = Visualizador(mapa)

    # Mostrar estado inicial
    print("\nMAPA COMPLETO")
    visualizarCosas.mostrar_mapa_completo()

    print("\nHABITACIÓN ACTUAL")
    print(explorador.explorar_habitacion())
    visualizarCosas.mostrar_habitacion_actual(explorador)

    print("\nMINIMAPA (VISITADAS)")
    visualizarCosas.mostrar_minimapa(explorador)

    print("\nESTADO DEL EXPLORADOR")
    visualizarCosas.mostrar_estado_explorador(explorador)

    print("\nESTADÍSTICAS DEL MAPA")
    stats = mapa.obtener_estadisticas_mapa()
    for clave, valor in stats.items():
        print(clave, ":", valor)

    # MENÚ
    print("\nOpciones: n/s/e/o para moverte, 'guardar', 'cargar' o 'salir'.")
    while True:
        comando = input("¿Qué quieres hacer?: ").strip().lower()

        if comando == "salir":
            break

        elif comando == "guardar":
            guardar_partida(mapa, explorador, archivo_json)
            print("Partida guardada en", archivo_json)

        elif comando == "cargar":
            mapa, explorador = cargar_partida(archivo_json)
            print("Partida cargada desde", archivo_json)
            # Actualizar el visualizador al nuevo mapa
            visualizarCosas = Visualizador(mapa)
            # Mostrar contexto tras cargar
            visualizarCosas.mostrar_habitacion_actual(explorador)
            visualizarCosas.mostrar_minimapa(explorador)
            visualizarCosas.mostrar_estado_explorador(explorador)

        elif comando in ["n", "s", "e", "o"]:
            # traducir letra a dirección completa
            if comando == "n":
                direccion = "norte"
            elif comando == "s":
                direccion = "sur"
            elif comando == "e":
                direccion = "este"
            else:
                direccion = "oeste"

            exito = explorador.mover(direccion)
            if exito:
                print("Te moviste a", direccion, "-> posición:", explorador.posicion_actual)
                print(explorador.explorar_habitacion())
                visualizarCosas.mostrar_habitacion_actual(explorador)
                visualizarCosas.mostrar_minimapa(explorador)
            else:
                print("No puedes ir en esa dirección desde aquí.")

        else:
            print("Comando no válido. Usa n/s/e/o, guardar, cargar o salir.")

    print("\nListo.")

if __name__ == "__main__":
    main()
