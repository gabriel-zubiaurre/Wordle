import re

from preparar_partida import preparar_partida
from archivos import (
    guardar_jugadores_palabras,
    cargar_jugadores_estadisticas,
    guardar_jugadores_estadisticas,
)

def obtener_colores():

    return {
        "verde": '\u001b[42;30m',
        "amarillo": '\u001b[43;30m',
        "gris": '\u001b[47;30m',
        "reset": '\u001b[0m'
    }

def normalizar(palabra):

    palabra = palabra.lower()

    palabra= re.sub("[áàäâ]", "a", palabra)
    palabra = re.sub("[éèëê]", "e", palabra)
    palabra = re.sub("[íìïî]", "i", palabra)
    palabra = re.sub("[óòöô]", "o", palabra)
    palabra = re.sub("[úùüû]", "u", palabra)
    palabra = re.sub("ç", "c", palabra)

    return palabra

def evaluar_intento(intento, palabra):

    intento = normalizar(intento)
    palabra = normalizar(palabra)

    longitud = len(palabra)
    fondo = ["gris"] * longitud

    letras_disponibles = {}
    indice = 0
    while indice < longitud:
        if intento[indice] == palabra[indice]:
            fondo[indice] = "verde"
        else:
            letra = palabra[indice]
            if letra in letras_disponibles:
                letras_disponibles[letra] = letras_disponibles[letra] + 1
            else:
                letras_disponibles[letra] = 1
        indice = indice + 1


    indice = 0
    while indice < longitud:
        if fondo[indice] != "verde":
            letra_intento = intento[indice]
            if (letra_intento in letras_disponibles) and (letras_disponibles[letra_intento] > 0):
                fondo[indice] = "amarillo"
                letras_disponibles[letra_intento] = letras_disponibles[letra_intento] - 1
        indice = indice + 1

    acierto = (intento == palabra)
    return fondo, acierto


def colorear_intento(intento, palabra):

    colores = obtener_colores()
    intento = intento.upper()

    fondo, acierto = evaluar_intento(intento, palabra)

    letras_fondo = [
        f"{colores[fondo[i]]} {intento[i]} {colores['reset']}"
        for i in range(len(intento))
    ]

    resultado = " ".join(letras_fondo)
    return resultado, acierto

def imprimir_historial(historial):

    for intento in historial:
        print(intento)

def calcular_puntaje(acierto, nro_intento, intentos_disponibles):

    if not acierto:
        return 0
    if nro_intento == 1:
        return 150
    bajar_puntos = 100 // intentos_disponibles
    puntos = 100 - (nro_intento - 1) * bajar_puntos
    if puntos < 0:
        puntos = 0
    return puntos


def jugar_partida(jugador):

    idioma, longitud, palabra, intentos_disponibles = preparar_partida(jugador)

    if (
        idioma is None
        or longitud is None
        or palabra is None
        or intentos_disponibles is None
    ):
        return None, None

    historial = []
    intento_actual = 0
    acierto = False
    puntos = 0

    print(f"Palabra de {longitud} letras. Intentos permitidos: {intentos_disponibles}.")
    print("Verde: letra correcta en posición correcta. Amarillo: letra en otra posición. Gris: letra ausente.")

    while (intento_actual < intentos_disponibles) and (not acierto):
        if intento_actual == intentos_disponibles - 1:
            print("¡ÚLTIMO INTENTO!")

        patron_intento = rf"[A-Za-zÁÉÍÓÚáéíóúÑñÇç]{{{longitud}}}"

        while True:
            intento = input(
                f"Intento {intento_actual + 1}/{intentos_disponibles} - Ingrese una palabra: "
            ).strip()

            if not re.fullmatch(patron_intento, intento):
                print(
                    f"La palabra debe tener exactamente {longitud} letras "
                    f"y solo puede contener letras (sin espacios ni números)."
                )
                continue

            break

        resultado, acierto = colorear_intento(intento, palabra)
        historial.append(resultado)
        imprimir_historial(historial)

        if acierto:
            puntos = calcular_puntaje(True, intento_actual + 1, intentos_disponibles)

        intento_actual = intento_actual + 1

    if acierto:
        print(f"¡Correcto! La palabra era: {palabra.upper()}. Puntos del juego: {puntos}")
    else:
        puntos = 0
        print(f"Sin intentos. La palabra era: {palabra.upper()}. Puntos del juego: {puntos}")

    guardar_jugadores_palabras(jugador, palabra)

    while True:
        respuesta = input("¿Jugar otra vez? (S/N): ").strip().lower()

        if re.fullmatch(r"s[ií]?", respuesta):
            seguir = True
            break

        if re.fullmatch(r"n[oó]?", respuesta):
            seguir = False
            break

        print("Respuesta no válida. Ingresá S o N.")

    return seguir, puntos


def actualizar_estadisticas(jugador, puntos):

    jugadores_estadisticas = cargar_jugadores_estadisticas()
    if jugador not in jugadores_estadisticas:
        jugadores_estadisticas[jugador] = {"juegos": 0, "puntos": 0, "promedio": 0}
    estadisticas = jugadores_estadisticas[jugador]
    estadisticas["juegos"] = estadisticas.get("juegos", 0) + 1
    estadisticas["puntos"] = estadisticas.get("puntos", 0) + puntos

    estadisticas["promedio"] = 0
    if estadisticas["juegos"] > 0:
        estadisticas["promedio"] = estadisticas["puntos"] // estadisticas["juegos"]

    guardar_jugadores_estadisticas(jugadores_estadisticas)