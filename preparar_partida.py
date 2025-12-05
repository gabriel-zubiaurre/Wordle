import random
import re
from archivos import (
    cargar_palabras,
    cargar_jugadores,
    cargar_jugadores_palabras,
    guardar_jugadores,
)

def definir_jugador():

    patron = r'^(?=(?:.*[A-Za-z0-9]){6,})[^\s]{8,16}$'

    while True:
        jugador = input("Ingrese el nombre de usuario: ").strip()

        if not jugador:
            print("El nombre de usuario no puede estar vacío.")
            continue

        if not re.fullmatch(patron, jugador):
            print(
                "El nombre de usuario debe tener entre 8 y 16 caracteres, "
                "al menos 6 letras o números y no puede contener espacios."
            )
            continue

        return jugador.lower()


def iniciar_sesion(jugador):

    jugadores = cargar_jugadores()

    if jugador in jugadores:
        datos = jugadores[jugador]
        contrasena_guardada = datos.get("contrasena", "")
        while True:
            contrasena = input("Ingresá tu contraseña (o -1 para volver al menú): ").strip()
            if contrasena == "-1":
                return False
            if contrasena == contrasena_guardada:
                print(f"Bienvenido de vuelta, {jugador}!")
                return True
            print("Contraseña incorrecta. Intentá de nuevo o escribí -1 para volver.")


    print(f"Bienvenido a tu primer juego de Wordle, {jugador}!")
    print("Vamos a crear una contraseña para tu usuario.")
    print("Requisitos: mínimo 8 caracteres, alfanumérica, al menos una mayúscula y un carácter especial.")

    patron = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'

    while True:
        contrasena = input("Elegí una contraseña: ").strip()

        if not re.fullmatch(patron, contrasena):
            print("La contraseña no cumple los requisitos. Intentá nuevamente.")
            continue

        repetir = input("Repetí la contraseña: ").strip()
        if contrasena != repetir:
            print("Las contraseñas no coinciden. Probá de nuevo.")
            continue

        jugadores[jugador] = {
            "contrasena": contrasena
        }
        guardar_jugadores(jugadores)
        print("Usuario registrado correctamente. ¡Vamos a jugar!")
        return True

def seleccionar_idioma():

    banco_palabras = cargar_palabras()
    if banco_palabras is None:
        return None

    idiomas_disponibles = sorted(banco_palabras.keys())

    if not idiomas_disponibles:
        print("No hay idiomas disponibles en el banco de palabras.")
        return None

    print("Idiomas disponibles:")
    print(", ".join(idiomas_disponibles))

    while True:
        idioma = input(f"Elegí idioma [{'/'.join(idiomas_disponibles)}]: ").strip().lower()

        if idioma in idiomas_disponibles:
            return idioma

        print("Idioma no válido. Intentá de nuevo.")


def seleccionar_longitud():

    banco_palabras = cargar_palabras()
    if banco_palabras is None:
        return None

    longitudes_disponibles = sorted(
        {longitud for palabras_por_longitud in banco_palabras.values() for longitud in palabras_por_longitud.keys()}
    )

    if not longitudes_disponibles:
        print("No hay longitudes disponibles en el banco de palabras.")
        return None

    print("Longitudes disponibles:")
    print(", ".join(str(l) for l in longitudes_disponibles))

    while True:
        entrada = input(f"Elegí longitud [{'/'.join(str(l) for l in longitudes_disponibles)}]: ").strip()

        if entrada.isdigit():
            longitud = int(entrada)
            if longitud in longitudes_disponibles:
                return longitud

        print("Longitud no válida. Intentá nuevamente.")


def elegir_palabra(idioma, longitud, jugador):

    banco_palabras = cargar_palabras()
    if banco_palabras is None:
        return None

    if idioma not in banco_palabras or longitud not in banco_palabras[idioma]:
        print("No hay palabras disponibles para el idioma y la longitud elegidos.")
        return None

    banco_palabras_idioma_longitud = banco_palabras[idioma][longitud]

    excluir_palabras = cargar_jugadores_palabras()
    excluir_palabras_jugador = excluir_palabras.get(jugador, set())

    palabras_disponibles = list(
        filter(
            lambda palabra: palabra not in excluir_palabras_jugador,
            banco_palabras_idioma_longitud
        )
    )

    if palabras_disponibles:
        palabras = palabras_disponibles
    else:
        palabras = banco_palabras_idioma_longitud

    if not palabras:
        print("No hay palabras disponibles para jugar.")
        return None

    indice = random.randint(0, len(palabras) - 1)
    return palabras[indice]

def preparar_partida(jugador):

    idioma = seleccionar_idioma()
    longitud = seleccionar_longitud()
    palabra = elegir_palabra(idioma, longitud, jugador)

    if longitud is None:
        intentos_disponibles = None
    else:
        intentos_disponibles = longitud + 1

    return idioma, longitud, palabra, intentos_disponibles