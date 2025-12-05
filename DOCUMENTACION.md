# Documentación Técnica

## 1. Visión general del proyecto

El proyecto implementa una versión de Wordle en consola con:

- **Usuarios con contraseña** y validación de formato.
- **Persistencia en archivos JSON línea a línea** para:
  - jugadores (usuario + contraseña),
  - estadísticas (juegos, puntos, promedio),
  - partidas (palabras jugadas por usuario),
- **Banco de palabras configurable** por archivo externo.
- **Elección dinámica de idioma y longitud**, según el contenido real del banco.
- **Evita repetir palabras** para un mismo jugador.
- **Sistema de puntajes** y módulo de estadísticas.

La lógica está organizada en módulos, respetando separación de responsabilidades:

- `wordle.py` → punto de entrada y menú principal.
- `archivos.py` → manejo de archivos y persistencia.
- `preparar_partida.py` → manejo de usuarios y armado de partida.
- `juego.py` → lógica interna de la partida.
- `estadisticas.py` → consultas de estadísticas.
- `test_juego.py` → tests unitarios.

---

## 2. Módulo `archivos.py`

### 2.1. Responsabilidad

Centraliza todo el acceso a disco:

- Verifica la existencia de la carpeta de datos.
- Verifica/crea archivos básicos:
  - banco de palabras,
  - jugadores,
  - estadísticas,
  - partidas.
- Carga y guarda la información en estructuras de Python (diccionarios y sets).

### 2.2. Constantes de rutas

```python
DATOS = os.path.join(os.path.dirname(__file__), "datos")
ARCHIVO_PALABRAS = os.path.join(DATOS, "palabras.json")
ARCHIVO_JUGADORES = os.path.join(DATOS, "jugadores.json")
ARCHIVO_ESTADISTICAS = os.path.join(DATOS, "estadisticas.json")
ARCHIVO_PARTIDAS = os.path.join(DATOS, "partidas.json")
```

> Nota: aunque la extensión sea `.json`, en el caso del banco de palabras se usa un formato **texto simple**, una línea por palabra, con el patrón:
> `idioma,longitud,palabra`

El resto de los archivos (`jugadores`, `estadísticas`, `partidas`) sí se guardan como **un JSON por línea**.

### 2.3. `verificar_archivos() -> bool`

Flujo:

1. Verifica si existe la carpeta `DATOS`.
   - Si no existe, pregunta si crearla.
   - Si no se crea, no se puede continuar.
   - Siempre indica que se debe cargar manualmente `palabras.json`.

2. Verifica que exista el archivo `ARCHIVO_PALABRAS` (banco de palabras):
   - Si falta, muestra mensaje y devuelve `False` (no se puede jugar sin banco).

3. Para el resto de archivos (`jugadores`, `estadísticas`, `partidas`):
   - Si no existen, pregunta si desea crear un archivo vacío.
   - Si el usuario acepta, crea el archivo.
   - Si no, devuelve `False`.

Si todo está correcto, devuelve `True`.

### 2.4. `cargar_palabras() -> dict | None`

- Intenta abrir `ARCHIVO_PALABRAS`.
- Para cada línea no vacía:
  - hace `idioma, longitud, palabra = linea.split(",")`,
  - convierte `longitud` a `int`,
  - agrega la palabra a un diccionario anidado:

```python
{
    "es": {5: ["perro", "carta", ...], 6: [...], ...},
    "en": {...},
    "pt": {...},
}
```

- Si el archivo **no existe**, muestra mensajes de error y devuelve `None`.

Se usa en:

- `seleccionar_idioma()`,
- `seleccionar_longitud()`,
- `elegir_palabra()`.

### 2.5. `cargar_jugadores() -> dict`

- Lee `ARCHIVO_JUGADORES`.
- Cada línea es un JSON con al menos `"jugador"` y `"contrasena"`:

```json
{"jugador": "usuario", "contrasena": "Secreta123!"}
```

- Devuelve:

```python
{
    "usuario": {"contrasena": "Secreta123!"},
    ...
}
```

- Si el archivo no existe:
  - pregunta si se quiere crear uno nuevo,
  - si la respuesta es “s”, crea un archivo vacío.

### 2.6. `cargar_jugadores_estadisticas() -> dict`

- Lee `ARCHIVO_ESTADISTICAS`.
- Cada línea es un JSON con forma:

```json
{"jugador": "usuario", "juegos": 3, "puntos": 250, "promedio": 83}
```

- Devuelve:

```python
{
    "usuario": {
        "juegos": 3,
        "puntos": 250,
        "promedio": 83,
    },
    ...
}
```

- Si el archivo no existe:
  - pregunta si se quiere crear uno nuevo,
  - si la respuesta es “s”, crea un archivo vacío.

### 2.7. `cargar_jugadores_palabras() -> dict`

- Lee `ARCHIVO_PARTIDAS`.
- Cada línea es un JSON:

```json
{"jugador": "usuario", "palabra": "carta"}
```

- Devuelve un diccionario que mapea jugador → set de palabras:

```python
{
    "usuario": {"carta", "perro", ...},
    "otro": {"gato", ...},
}
```

- Si no existe el archivo, ofrece crearlo vacío.

Se usa para **evitar repetir palabras** con el mismo jugador.

### 2.8. Funciones de guardado

#### `guardar_jugadores(jugadores: dict)`

- Escribe `jugadores` en `ARCHIVO_JUGADORES` usando un archivo temporal:
  - construye un `.tmp`,
  - escribe una línea JSON por jugador,
  - reemplaza el archivo original (`os.replace`).
- Este patrón evita archivos corruptos si algo sale mal a mitad de escritura.

#### `guardar_jugadores_estadisticas(jugadores_estadisticas: dict)`

- Mismo esquema de archivo temporal.
- Escribe una línea JSON por jugador con: juegos, puntos, promedio.

#### `guardar_jugadores_palabras(jugador, palabra)`

- Abre `ARCHIVO_PARTIDAS` en modo append.
- Agrega una línea JSON con el jugador y la palabra jugada.

---

## 3. Módulo `preparar_partida.py`

### 3.1. Responsabilidad

- Definir el nombre de usuario.
- Manejar el inicio de sesión y el registro.
- Permitir elegir:
  - idioma,
  - longitud de palabra.
- Elegir una palabra adecuada para el jugador.
- Devolver los datos para que `jugar_partida()` pueda funcionar.

### 3.2. `definir_jugador() -> str`

- Pide al usuario un nombre.
- Usa una expresión regular:

```python
patron = r'^(?=(?:.*[A-Za-z0-9]){6,})[^\s]{8,16}$'
```

Condiciones:

- Entre 8 y 16 caracteres.
- Al menos 6 alfanuméricos (letras o números).
- No se permiten espacios.
- Se devuelve siempre en minúsculas (`jugador.lower()`).

Si no se cumple el patrón, vuelve a pedir con `while True` + `continue`.

### 3.3. `iniciar_sesion(jugador) -> bool`

1. Carga los jugadores con `cargar_jugadores()`.
2. Si el `jugador` ya existe:
   - Pide contraseña en un bucle:
     - permite escribir `-1` para volver al menú principal (`False`),
     - si la contraseña coincide con la guardada, da la bienvenida y devuelve `True`.
3. Si el `jugador` **no existe**:
   - Muestra un mensaje de bienvenida y requisitos de contraseña:
     - mínimo 8 caracteres,
     - debe ser alfanumérica,
     - al menos una mayúscula,
     - al menos un carácter especial.
   - Usa regex para validar la contraseña:
     ```python
     patron = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'
     ```
   - Pide repetirla.
   - Si la confirmación coincide, guarda el nuevo usuario en `jugadores` y persiste con `guardar_jugadores`.

Devuelve:

- `True` si el login/registro fue exitoso.
- `False` si el usuario cancela con `-1`.

### 3.4. `seleccionar_idioma() -> str | None`

- Llama a `cargar_palabras()`:
  - Si devuelve `None`, retorna `None` (no hay banco).
- Obtiene los idiomas disponibles de las claves del diccionario.
- Si no hay idiomas, informa y devuelve `None`.
- Muestra la lista de idiomas (`es`, `en`, `pt`, etc.).
- Pide uno válido, repitiendo hasta que el usuario ingresa uno correcto.

### 3.5. `seleccionar_longitud() -> int | None`

- Llama a `cargar_palabras()`:
  - Si devuelve `None`, retorna `None`.
- Reúne todas las longitudes disponibles en todos los idiomas:

```python
longitudes_disponibles = sorted(
    {longitud for palabras_por_longitud in banco_palabras.values()
     for longitud in palabras_por_longitud.keys()}
)
```

- Si no hay longitudes, informa y devuelve `None`.
- Muestra las longitudes disponibles.
- Pide al usuario una longitud:
  - valida que sea número,
  - valida que esté en la lista de longitudes.
- Repite hasta obtener una longitud válida.

### 3.6. `elegir_palabra(idioma, longitud, jugador) -> str | None`

- Vuelve a llamar a `cargar_palabras()`:
  - Si devuelve `None`, retorna `None`.
- Verifica que existan palabras para ese idioma/longitud.
- Obtiene la lista de palabras base: `banco_palabras[idioma][longitud]`.
- Carga las palabras ya jugadas por el jugador con `cargar_jugadores_palabras()`.
- Filtra las palabras que ese jugador aún no jugó:

```python
palabras_disponibles = [
    palabra for palabra in banco_palabras_idioma_longitud
    if palabra not in excluir_palabras_jugador
]
```

- Si hay palabras disponibles, elige entre ellas.
- Si el jugador ya usó todas esas palabras, se permite repetir.
- Elige una palabra al azar con `random.randint`.

### 3.7. `preparar_partida(jugador) -> (idioma, longitud, palabra, intentos_disponibles)`

- Llama a:
  - `seleccionar_idioma()`,
  - `seleccionar_longitud()`,
  - `elegir_palabra(idioma, longitud, jugador)`.
- Calcula `intentos_disponibles` como:
  - `None` si `longitud` es `None`,
  - `longitud + 1` en caso normal.
- Devuelve la tupla:

```python
(idioma, longitud, palabra, intentos_disponibles)
```

Si algún valor es `None`, será **`jugar_partida`** quien decida terminar la partida.

---

## 4. Módulo `juego.py`

### 4.1. Responsabilidad

- Encapsular la lógica del juego en sí:
  - comparación de palabras,
  - asignación de colores,
  - normalización,
  - puntajes,
  - impresión del historial.
- Manejar una sesión completa de partida para un jugador.
- Actualizar sus estadísticas.

### 4.2. `obtener_colores() -> dict`

Devuelve un diccionario con códigos ANSI para colorear la consola:

- Fondo verde (acierto),
- fondo amarillo (letra en otra posición),
- fondo gris (letra ausente),
- código de reset.

### 4.3. `normalizar(palabra) -> str`

- Convierte la palabra a minúsculas.
- Reemplaza vocales acentuadas y `ç` por su forma simple.
- Permite que la comparación ignore acentos, aunque el usuario los use.

### 4.4. `evaluar_intento(intento, palabra) -> (fondo, acierto)`

Proceso:

1. Normaliza ambas palabras.
2. Inicializa un vector de colores `fondo` en “gris”.
3. Primera pasada:
   - para cada posición donde la letra coincide exactamente, marca “verde”,
   - lleva una cuenta de cuántas veces aparece cada letra no-verde en la palabra objetivo.
4. Segunda pasada:
   - para las posiciones no verdes:
     - si hay ocurrencias restantes de esa letra en la cuenta → marca “amarillo” y descuenta una.
5. Devuelve:
   - `fondo`: lista de colores (uno por posición),
   - `acierto`: `True` si la palabra coincide completamente.

### 4.5. `colorear_intento(intento, palabra) -> (resultado, acierto)`

- Llama a `evaluar_intento` para obtener:
  - la lista de colores `fondo` (uno por posición),
  - el indicador de acierto.
- Convierte el intento a mayúsculas para mostrarlo en pantalla.
- Recorre las posiciones de la palabra mediante índices y, para cada posición:
  - toma el color correspondiente de `fondo[i]`,
  - toma la letra correspondiente de `intento[i]`,
  - arma una cadena con los códigos ANSI.
- Utiliza una *list comprehension* basada en índices para construir la lista de letras coloreadas.
- Une todas las letras coloreadas en una sola cadena, lista para imprimir.
- Devuelve:
  - `resultado`: la cadena coloreada,
  - `acierto`: el booleano que indica si se acertó la palabra.

### 4.6. `imprimir_historial(historial)`

- Imprime cada intento coloreado guardado en la lista `historial`.

### 4.7. `calcular_puntaje(acierto, nro_intento, intentos_disponibles) -> int`

Reglas:

- Si no hay acierto → 0 puntos.
- Si acierta en el primer intento → 150 puntos.
- Si acierta después:
  - se parte de 100,
  - se descuenta una cantidad fija por cada intento usado,
  - nunca baja de 0.

### 4.8. `jugar_partida(jugador) -> (seguir, puntos)`

Flujo detallado:

1. Llama a `preparar_partida(jugador)` y recibe:
   - `idioma, longitud, palabra, intentos_disponibles`.
2. Si alguno es `None`:
   - muestra mensaje de error,
   - devuelve `(None, None)` para indicar fallo.
3. Informa:
   - longitud de la palabra,
   - cantidad de intentos,
   - significado de los colores.
4. Entra en un bucle de intentos:
   - antes del último intento muestra “¡ÚLTIMO INTENTO!”.
   - usa regex para validar la palabra ingresada:
     - longitud correcta,
     - solo letras (incluye acentos y ñ).
   - colorea la palabra,
   - agrega el intento al historial y lo imprime,
   - si acierta, calcula el puntaje.
5. Al terminar:
   - si acierta → muestra puntos,
   - si no acierta → puntos = 0.
6. Registra la palabra jugada en `ARCHIVO_PARTIDAS` con `guardar_jugadores_palabras`.
7. Pregunta si desea jugar otra vez:
   - acepta variantes de `sí` / `no` usando regex.
8. Devuelve:
   - `seguir` (`True` / `False` o `None` en caso de error),
   - `puntos`.

### 4.9. `actualizar_estadisticas(jugador, puntos)`

- Carga estadísticas con `cargar_jugadores_estadisticas`.
- Si el jugador no existe, inicializa sus valores.
- Incrementa juegos y puntos.
- Recalcula el promedio como división entera (`//`).
- Guarda el resultado en `ARCHIVO_ESTADISTICAS`.

---

## 5. Módulo `estadisticas.py`

### 5.1. Responsabilidad

- Mostrar estadísticas de juego al usuario:
  - generales,
  - ranking,
  - por jugador.

### 5.2. `estadisticas()`

- Muestra un banner y un submenú con opciones:
  - `1` → estadísticas generales,
  - `2` → ranking TOP 5,
  - `3` → buscar un jugador,
  - ENTER → volver al menú principal.
- Usa un diccionario de opciones para llamar a la función correspondiente.
- Emplea un `while True` que solo finaliza cuando el usuario presiona ENTER.

### 5.3. `estadisticas_general()`

- Carga las estadísticas.
- Si no hay registros, informa.
- Si hay, recorre el diccionario e imprime:
  - jugador,
  - juegos,
  - puntos,
  - promedio.

### 5.4. `estadisticas_ranking()`

- Carga estadísticas.
- Si no hay datos, informa.
- Ordena los jugadores por:
  - promedio,
  - puntos,
  usando `sorted` + `lambda`.
- Muestra los primeros 5 con formato de ranking.
- Espera ENTER para volver.

### 5.5. `estadisticas_jugador()`

- Carga estadísticas.
- Si no hay datos, informa.
- Pide un nombre de jugador usando `definir_jugador`.
- Si encuentra estadísticas para ese jugador, las imprime.
- Si no, informa que no hay registros.

---

## 6. Módulo `wordle.py`

### 6.1. Responsabilidad

Es el **punto de entrada** del programa:

- Verifica el entorno de datos.
- Muestra el menú principal.
- Orquesta:
  - definición de jugador,
  - inicio de sesión,
  - ciclo de partidas,
  - actualización de estadísticas,
  - salida limpia del juego.

### 6.2. `menu_principal() -> bool`

Muestra:

- banner con el título del juego,
- menú con opciones:
  - ENTER → comenzar a jugar,
  - `1` → ver instrucciones,
  - `5` → ver estadísticas de jugadores,
  - `9` → salir.

En un `while not listo_para_jugar`:

- ENTER → `return True`,
- `1` → imprime instrucciones y vuelve al menú,
- `5` → llama a `estadisticas()` y vuelve al menú,
- `9` → `return False`,
- cualquier otra cosa → mensaje “Opción no válida” y vuelve a mostrar el menú.

### 6.3. `main()`

Flujo:

1. Llama a `verificar_archivos()`:
   - si devuelve `False`, termina.
2. Entra en un `while activo`:
   - llama a `menu_principal()`:
     - si devuelve `False`, imprime “Hasta la próxima!” y termina.
   - obtiene el `jugador` con `definir_jugador()`.
   - llama a `iniciar_sesion(jugador)`:
     - si devuelve `False`, vuelve al menú principal.
   - Entra en un `while seguir`:
     - llama a `jugar_partida(jugador)` → `(seguir, puntos)`.
     - si `(seguir, puntos) == (None, None)`:
       - termina el programa.
     - si `not seguir`:
       - registra estadísticas con `actualizar_estadisticas`,
       - sale del bucle de partidas y vuelve al menú principal.
     - si `seguir` es `True`:
       - registra estadísticas,
       - arranca otra partida para el mismo jugador.

Al final de archivo, se ejecuta `main()` directamente.

---

## 7. Tests unitarios

El proyecto incluye pruebas unitarias para verificar el comportamiento de las funciones más importantes de la lógica del juego:

- **Archivo**: `test_juego.py`
  - Prueba `normalizar(palabra)` con:
    - casos simples de mayúsculas/minúsculas,
    - palabras con acentos y diéresis.
  - Prueba `evaluar_intento(intento, palabra)` en distintos escenarios:
    - adivinar la palabra exacta (todo verde),
    - fallar por completo (todo gris),
    - usar las mismas letras en distinto orden (todo amarillo),
    - controlar el comportamiento con letras repetidas.
  - Prueba `calcular_puntaje(acierto, nro_intento, intentos_disponibles)`:
    - puntaje perfecto (acierto en el primer intento),
    - puntaje intermedio (acierto en un intento intermedio),
    - derrota (sin acierto da siempre 0 puntos).
