from juego import normalizar, evaluar_intento, calcular_puntaje


def test_normalizar_basico():
    assert normalizar("PERRO") == "perro"

def test_normalizar_dificil():
    assert normalizar("MÚSICA") == "musica"
    assert normalizar("Pingüino") == "pinguino"

def test_adivinar_palabra_exacta():
    fondo, acierto = evaluar_intento("PERRO", "PERRO")
    
    assert acierto == True
    assert fondo == ["verde", "verde", "verde", "verde", "verde"]

def test_fallar_por_completo():
    fondo, acierto = evaluar_intento("CAJAS", "PERRO")
    
    assert acierto == False
    assert fondo == ["gris", "gris", "gris", "gris", "gris"]

def test_letras_desordenadas():
    fondo, acierto = evaluar_intento("ACERO", "COREA")
    
    assert acierto == False
    assert fondo == ["amarillo", "amarillo", "amarillo", "amarillo", "amarillo"]


def test_puntaje_perfecto():
    puntos = calcular_puntaje(True, 1, 5)
    assert puntos == 150

def test_puntaje_medio():
    puntos = calcular_puntaje(True, 3, 5)
    assert puntos == 60

def test_puntaje_derrota():
    puntos = calcular_puntaje(False, 6, 6)
    assert puntos == 0