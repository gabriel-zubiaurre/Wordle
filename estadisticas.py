from archivos import(
    cargar_jugadores_estadisticas,
    cargar_jugadores_palabras)
from preparar_partida import definir_jugador

def estadisticas():

    banner_estadisticas = (
        "\n==========================================\n"
        "          E S T A D Í S T I C A S  \n"
        "==========================================\n"
    )
    menu_estadisticas = (
        "Elegí una opción:\n"
        "1) Estadísticas generales\n"
        "2) TOP 5\n"
        "3) Buscar por jugador\n"
        "ENTER para volver\n"
    )

    print(banner_estadisticas)
    print(menu_estadisticas)

    opciones = {
        "1": estadisticas_general,
        "2": estadisticas_ranking,
        "3": estadisticas_jugador,
    }

    while True:
        opcion = input("> ").strip()

        if opcion == "":
            break

        if opcion in opciones:
            print("\n------------------------------------------")
            opciones[opcion]()
            print("------------------------------------------\n")
        else:
            print("Opción no válida. Probá de nuevo o ENTER para volver.")

        print(menu_estadisticas)


def estadisticas_general():

    jugadores_estadisticas = cargar_jugadores_estadisticas()

    if not jugadores_estadisticas:
        print("Todavía no hay estadísticas guardadas.")
        return

    print("Estadísticas generales:\n")
    for jugador, estadisticas in jugadores_estadisticas.items():
        texto = (
            f"- {jugador}: "
            f"Juegos: {estadisticas['juegos']}, "
            f"Puntos: {estadisticas['puntos']}, "
            f"Promedio: {estadisticas['promedio']}"
        )
        print(texto)


def estadisticas_ranking():

    jugadores_estadisticas = cargar_jugadores_estadisticas()

    if not jugadores_estadisticas:
        print("Todavía no hay estadísticas para armar un ranking.")
        return

    print("\n==========================================")
    print("                 T O P   5               ")
    print("==========================================")

    ranking = sorted(
        jugadores_estadisticas.items(),
        key=lambda item: (item[1]["promedio"], item[1]["puntos"]),
        reverse=True,
    )

    limite = min(5, len(ranking))

    for posicion in range(limite):
        jugador, estadisticas = ranking[posicion]
        print(f"#{posicion + 1} // {jugador} // Promedio: {estadisticas['promedio']}")

    print("\nIngresá ENTER para volver")
    while True:
        respuesta = input("> ").strip().lower()
        if respuesta == "":
            break
        print("Ingresá ENTER para volver")


def estadisticas_jugador():

    jugadores_estadisticas = cargar_jugadores_estadisticas()

    if not jugadores_estadisticas:
        print("Todavía no hay estadísticas guardadas.")
        return

    jugador = definir_jugador()

    if jugador in jugadores_estadisticas:
        estadisticas = jugadores_estadisticas[jugador]
        print(
            f"{jugador}: Juegos: {estadisticas['juegos']}, "
            f"Puntos: {estadisticas['puntos']}, Promedio: {estadisticas['promedio']}"
        )
    else:
        print(f"No hay registros para {jugador}.")

    jugadores_palabras = cargar_jugadores_palabras()
    palabras_jugador = jugadores_palabras.get(jugador, set())

    if palabras_jugador:
        print("\nPalabras jugadas:")
        lista_ordenada = sorted(palabras_jugador)
        mostrar_palabras(lista_ordenada)
        print(f"Total: {len(lista_ordenada)} palabra(s)")
    else:
        print("\nEste jugador todavía no tiene palabras jugadas registradas.")

def mostrar_palabras(lista_palabras, indice=0):

    if indice >= len(lista_palabras):
        return

    print(f"- {lista_palabras[indice]}")

    mostrar_palabras(lista_palabras, indice + 1)
