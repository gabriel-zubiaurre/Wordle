from juego import normalizar, evaluar_intento, calcular_puntaje

# --- GRUPO 1: Probando que el texto se limpie bien ---

def test_normalizar_basico():
    # Caso simple: mayúsculas a minúsculas
    assert normalizar("PERRO") == "perro"

def test_normalizar_dificil():
    # Caso difícil: acentos y diéresis
    assert normalizar("MÚSICA") == "musica"
    assert normalizar("Pingüino") == "pinguino"

# --- GRUPO 2: Probando la lógica del juego (Colores) ---

def test_adivinar_palabra_exacta():
    # Si la palabra es PERRO, y escribo PERRO, todo debe ser verde
    fondo, acierto = evaluar_intento("PERRO", "PERRO")
    
    assert acierto == True
    assert fondo == ["verde", "verde", "verde", "verde", "verde"]

def test_fallar_por_completo():
    # Si la palabra es PERRO y escribo CAJAS (nada coincide)
    fondo, acierto = evaluar_intento("CAJAS", "PERRO")
    
    assert acierto == False
    assert fondo == ["gris", "gris", "gris", "gris", "gris"]

def test_letras_desordenadas():
    # Palabra: COREA, Intento: ACERO (Mismas letras, distinto orden)
    # Todo debería ser amarillo
    fondo, acierto = evaluar_intento("ACERO", "COREA")
    
    assert acierto == False
    assert fondo == ["amarillo", "amarillo", "amarillo", "amarillo", "amarillo"]

# --- GRUPO 3: Probando los puntajes ---

def test_puntaje_perfecto():
    # Intento 1 de 5 posibles. Debe dar el máximo (150)
    puntos = calcular_puntaje(True, 1, 5)
    assert puntos == 150

def test_puntaje_medio():
    # Acierto en el intento 3 de 5.
    # Cálculo: 100 - (3-1) * (100/5) = 100 - 2*20 = 60 puntos
    puntos = calcular_puntaje(True, 3, 5)
    assert puntos == 60

def test_puntaje_derrota():
    # Si no acertó (False), debe tener 0 puntos sin importar el intento
    puntos = calcular_puntaje(False, 6, 6)
    assert puntos == 0