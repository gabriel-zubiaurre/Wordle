# WORDLE

## 1. Estructura General

El programa está dividido en módulos especializados:

- **wordle.py** – Punto de entrada, menú principal y ciclo del juego.
- **archivos.py** – Gestión de archivos: jugadores, estadísticas, partidas y banco de palabras.
- **preparar_partida.py** – Manejo de usuarios, inicio de sesión y configuración de partida.
- **juego.py** – Lógica completa de la partida (evaluación, coloreado, puntaje).
- **estadisticas.py** – Visualización y consulta de estadísticas.
- **test_juego.py** – Pruebas unitarias de la lógica principal del juego.

---

## 2. Flujo General del Programa

1. **main()** verifica archivos necesarios.
2. El usuario accede al **menú principal**.
3. Se define usuario y se inicia sesión.
4. Se prepara la partida:
   - Selección de idioma.
   - Selección de longitud.
   - Elección de palabra (evitando repetidas).
5. Se juega una partida:
   - Validación de entrada por regex.
   - Coloreado estilo Wordle.
   - Puntaje según número de intentos.
6. Se guardan:
   - La palabra jugada.
   - Las estadísticas del jugador.
7. El jugador decide continuar o volver al menú.

---

## 3. Persistencia en Archivos

La carpeta **datos/** contiene:

- **palabras.json** → archivo de texto línea a línea con `idioma,longitud,palabra`
- **jugadores.json** → JSON por línea con usuario y contraseña
- **estadisticas.json** → JSON por línea con juegos, puntos y promedio
- **partidas.json** → JSON por línea con palabras ya jugadas por cada jugador

Cada módulo usa cargadores y guardadores específicos para leer y escribir estos archivos.

---

## 4. Preparación de Partida

Incluye:

- Validación de nombre de usuario con regex.
- Inicio de sesión o registro nuevo.
- Selección dinámica de idioma y longitud según el contenido del banco.
- Elección de palabra evitando repetir palabras ya jugadas por ese jugador.

Devuelve:
```
(idioma, longitud, palabra, intentos)
```

---

## 5. Lógica del Juego

Incluye:

- Normalización de palabras para ignorar acentos.
- Comparación por letra:
  - Verde → posición correcta
  - Amarillo → letra presente en otra posición
  - Gris → no presente
- Historial de intentos coloreados.
- Cálculo de puntaje:
  - Primer intento → 150
  - Resto → decrece desde 100
- Pregunta para volver a jugar.

---

## 6. Estadísticas

Tres vistas principales:

- **Generales** → cada jugador con juegos, puntos, promedio.
- **Ranking TOP 5** → ranking ordenado por promedio y puntos.
- **Buscar jugador** → ver estadísticas individuales.

Cada operación usa un diccionario cargado desde archivo JSON.

---

## 7. Tests unitarios

Se incluyen pruebas unitarias sobre la lógica central del juego en el archivo `test_juego.py`.  
Estas pruebas cubren:

- la normalización de palabras,
- la evaluación de intentos (aciertos y colores),
- el cálculo de puntajes en distintos escenarios.


## 8. Resumen Final


El programa está modularizado, validado y estructurado para:

- Manejo completo de usuarios.
- Persistencia robusta.
- Evitar repetir palabras por jugador.
- Validación fuerte con regex.
- Lógica clara de puntajes y partidas.
- Estadísticas completas por jugador.
