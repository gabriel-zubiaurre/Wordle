import os
import json

DATOS = os.path.join(os.path.dirname(__file__), "datos")
ARCHIVO_PALABRAS = os.path.join(DATOS, "palabras.json")
ARCHIVO_JUGADORES = os.path.join(DATOS, "jugadores.json")
ARCHIVO_ESTADISTICAS = os.path.join(DATOS, "estadisticas.json")
ARCHIVO_PARTIDAS = os.path.join(DATOS, "partidas.json")

def verificar_archivos():

    if not os.path.isdir(DATOS):
        print("No se encontró la carpeta de datos del juego.")
        respuesta = input("¿Querés crearla ahora? (S/N): ").strip().lower()

        if respuesta.startswith("s"):
            try:
                os.makedirs(DATOS, exist_ok=True)
                print("Carpeta de datos creada.")
            except OSError as error:
                print(f"No se pudo crear la carpeta de datos: {error}")
        else:
            print("Sin la carpeta de datos no se puede continuar.")

        print("Cargá manualmente el archivo palabras.json en la carpeta de datos y volvé a ejecutar el juego.")
        return False

    if not os.path.exists(ARCHIVO_PALABRAS):
        print("No se encontró el archivo palabras.json (banco de palabras).")
        print("No se puede continuar sin este archivo.")
        return False

    archivos = [
        ("jugadores", ARCHIVO_JUGADORES),
        ("estadísticas", ARCHIVO_ESTADISTICAS),
        ("partidas", ARCHIVO_PARTIDAS),
    ]

    for nombre, ruta in archivos:
        if os.path.exists(ruta):
            continue

        print(f"No se encontró el archivo de {nombre} ({os.path.basename(ruta)}).")
        respuesta = input(f"¿Querés crear un archivo vacío de {nombre}? (S/N): ").strip().lower()

        if not respuesta.startswith("s"):
            print(f"Sin el archivo de {nombre} no se puede continuar.")
            return False

        try:
            with open(ruta, "w", encoding="utf-8"):
                pass
            print(f"Archivo de {nombre} creado.")
        except OSError as error:
            print(f"No se pudo crear el archivo de {nombre}: {error}")
            return False

    return True

def cargar_palabras():

    banco_palabras = {}
    try:
        with open(ARCHIVO_PALABRAS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                idioma, longitud, palabra = linea.split(",")
                longitud = int(longitud)
                banco_palabras.setdefault(idioma, {})
                banco_palabras[idioma].setdefault(longitud, [])
                banco_palabras[idioma][longitud].append(palabra)
    except FileNotFoundError:
        print("No se encontró el archivo palabras.json (banco de palabras).")
        print("No se puede continuar sin este archivo.")
        print("Cargá manualmente el archivo palabras.json en la carpeta de datos y volvé a ejecutar el juego.")
        return None

    return banco_palabras

def cargar_jugadores():

    jugadores = {}
    try:
        with open(ARCHIVO_JUGADORES, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                registro = json.loads(linea)
                jugador = registro.get("jugador")
                if not jugador:
                    continue
                contrasena = registro.get("contrasena", "")
                jugadores[jugador] = {
                    "contrasena": contrasena
                }
    except FileNotFoundError:
        print("No se encontró el archivo de jugadores. ¿Querés crear uno nuevo? (S/N)")
        respuesta = input("> ").strip().lower()
        if respuesta == "s":
            os.makedirs(DATOS, exist_ok=True)
            with open(ARCHIVO_JUGADORES, "w", encoding="utf-8"):
                pass
    return jugadores


def cargar_jugadores_estadisticas():

    jugadores_estadisticas = {}
    try:
        with open(ARCHIVO_ESTADISTICAS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                registro = json.loads(linea)
                jugador = registro.get("jugador")
                if not jugador:
                    continue
                juegos = registro.get("juegos", 0)
                puntos = registro.get("puntos", 0)
                promedio = registro.get("promedio", 0)
                jugadores_estadisticas[jugador] = {
                    "juegos": juegos,
                    "puntos": puntos,
                    "promedio": promedio,
                }
    except FileNotFoundError:
        print("No se encontró el archivo de estadísticas. ¿Querés crear uno nuevo? (S/N)")
        respuesta = input("> ").strip().lower()
        if respuesta == "s":
            os.makedirs(DATOS, exist_ok=True)
            with open(ARCHIVO_ESTADISTICAS, "w", encoding="utf-8"):
                pass
    return jugadores_estadisticas


def cargar_jugadores_palabras():

    jugadores_palabras = {}
    try:
        with open(ARCHIVO_PARTIDAS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                registro = json.loads(linea)
                jugador = registro.get("jugador")
                palabra = registro.get("palabra")
                if jugador and palabra:
                    if jugador not in jugadores_palabras:
                        jugadores_palabras[jugador] = set()
                    jugadores_palabras[jugador].add(palabra)
    except FileNotFoundError:
        print("No se encontró el archivo de partidas. ¿Querés crear uno nuevo? (S/N)")
        respuesta = input("> ").strip().lower()
        if respuesta == "s":
            os.makedirs(DATOS, exist_ok=True)
            with open(ARCHIVO_PARTIDAS, "w", encoding="utf-8"):
                pass
    return jugadores_palabras

def guardar_jugadores(jugadores):

    tmp_path = ARCHIVO_JUGADORES + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as archivo:
        for jugador, datos in jugadores.items():
            registro = {
                "jugador": jugador,
                "contrasena": datos.get("contrasena", ""),
            }
            archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
    os.replace(tmp_path, ARCHIVO_JUGADORES)

def guardar_jugadores_estadisticas(jugadores_estadisticas):

    os.makedirs(DATOS, exist_ok=True)
    tmp_path = ARCHIVO_ESTADISTICAS + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as archivo:
        for jugador, datos in jugadores_estadisticas.items():
            registro = {
                "jugador": jugador,
                "juegos": datos.get("juegos", 0),
                "puntos": datos.get("puntos", 0),
                "promedio": datos.get("promedio", 0),
            }
            archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
    os.replace(tmp_path, ARCHIVO_ESTADISTICAS)

def guardar_jugadores_palabras(jugador, palabra):

    os.makedirs(DATOS, exist_ok=True)
    registro = {"jugador": jugador, "palabra": palabra}
    with open(ARCHIVO_PARTIDAS, "a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
