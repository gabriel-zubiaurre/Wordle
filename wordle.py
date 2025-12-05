from archivos import verificar_archivos

from preparar_partida import (
    definir_jugador,
    iniciar_sesion)

from juego import (jugar_partida,
    actualizar_estadisticas,
)

from estadisticas import estadisticas

def menu_principal():

    banner = (
        "\n"
        "==========================================\n"
        "              W  O  R  D  L  E            \n"
        "==========================================\n"
    )
    menu = (
        "Presiona ENTER para jugar.\n"
        "Ingresa 1 para ver las instrucciones.\n"
        "Ingresa 5 para ver las estadísticas de jugadores.\n"
        "Escribi 9 para salir del juego.\n"
        "==========================================\n"
    )

    instrucciones = (
        "De que se trata?\n"
        "Adivinar la palabra oculta antes de que se te acaben los intentos.\n\n"
        "Cómo jugar\n"
        "1) Elegi idioma y largo de palabra. Cuanto mas larga sea la palabra, mas intentos para adivinarla vas a tener!\n"
        "2) Escribi en cada turno una palabra con ese largo. OJO: no es necesario respetar mayusculas ni acentos!\n"
        "3) Wordle te va a devolver tu palabra coloreada segun los siguientes criterios:\n"
        "   • Verde: letra correcta en posición correcta.\n"
        "   • Amarillo: letra presente pero en otra posición.\n"
        "   • Gris: letra ausente en la palabra palabra.\n\n"
        "Puntaje\n"
        "• Desde el 2º intento, el puntaje empieza en 100 y disminuye con cada intento usado hasta llegar a 0 si no se acierta en el ultimo.\n"
        "• Si acertás en el primer intento... Ganas 150 puntos!\n"
    )

    print(banner)
    print("MENU PRINCIPAL")
    print("==========================================")
    print(menu)

    listo_para_jugar = False
    while not listo_para_jugar:
        opcion = input("> ").strip()
        if opcion == "":
            listo_para_jugar = True
        elif opcion == "1":
            print("==========================================\n")
            print(instrucciones)
            print("==========================================\n")
            print(menu)
        elif opcion == "5":
            print("==========================================\n")
            estadisticas()
            print("\n==========================================\n")
            print(menu)
        elif opcion == "9":
            return False
        else:
            print("==========================================\n")
            print("Opción no válida.")
            print(menu)
    return True



def main():

    if not verificar_archivos():
        return

    activo = True
    while activo:
        jugar = menu_principal()
        if not jugar:
            print("Hasta la proxima!")
            return

        jugador = definir_jugador()
        sesion_ok = iniciar_sesion(jugador)
        if not sesion_ok:
            continue

        seguir = True
        while seguir:
            seguir, puntos = jugar_partida(jugador)

            if seguir is None and puntos is None:
                return

            if not seguir:
                actualizar_estadisticas(jugador, puntos)
                break

            actualizar_estadisticas(jugador, puntos)

main()