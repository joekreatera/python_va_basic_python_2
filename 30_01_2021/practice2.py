# el juego s trata de desarmar bombas
# si la bomba es de tipo AB101 entonces los cables que hay que cortar son el rojo y el azul
# si la bomba es de tipo IU12 el cable rojo se debe cortar y el azul se debe mantener
# si la bomba es de tipo MAA089 el verde se debe conectar a la terminal negra y el cable rojo a la amarilla
# si la bomba es de tipo T78 solo hay que quitar la bateria
# KABOOM-> perder , UFFF -> ganar

"""
Bombas: AB101,IU12,MAA089,T78
Cables: rojo, azul, verde
Terminales: negra, amarilla
Bateria: 1

Entrada: bomba, cables (C/D), terminal (conectar o dejar, conectar que cable)
Decisiones
Cable: Cortar, dejar o transferir a terminal
Bateria: retirar o dejar
"""
CUT = 1
LEAVE = 2
ROUTE = 3
RED = 1
BLUE = 2
GREEN = 3
BLACK = 1
YELLOW = 2
BATTERY_QUIT = 1
BATTERY_LEAVE = 2
def getUserInput(question, colorToAssign,tB,tY):
    c = int(input(question))
    if( c == ROUTE):
        term = int(input('Terminal de reconexion (1)NEGRA, (2)AMARILLA:'))
        if( term == BLACK):
            return c,colorToAssign,tY
        if( term == YELLOW):
            return c,tB,colorToAssign
    return c,tB,tY
bomb = input("Matricula de la bomba:")
termB = 0
termY = 0
red, termB, termY = getUserInput('Accion cable rojo: (1)cortar (2)dejar (3)reconectar:',RED, termB, termY)
blue, termB, termY = getUserInput('Accion cable azul: (1)cortar (2)dejar (3)reconectar:', BLUE, termB, termY)
green, termB, termY = getUserInput('Accion cable verde: (1)cortar (2)dejar (3)reconectar:', GREEN, termB, termY)
battery = int(input('(1) Quitar la bateria (2) Dejar la bateria:'))
# evaluar exito o fracaso
if( bomb == 'AB101' and red == CUT and blue == CUT):
    print("UFFF")
elif( bomb == 'IU12' and red == CUT and blue == LEAVE):
    print("UFFF")
elif( bomb == 'MAA089' and green == ROUTE and termB  == GREEN and red == ROUTE and termY == RED):
    print("UFFF")
elif( bomb == 'T78' and battery == BATTERY_QUIT):
    print("UFFF")
else:
    print("KABOOM")





"""
red = int(input('Accion cable rojo: (1)cortar (2)dejar (3)reconectar'))
if( red == ROUTE):
    term = int(input('Terminal de reconexion (1)NEGRA, (2)AMARILLA'))
    if( term == BLACK):
        termB = RED # rojo
    if( term == YELLOW):
        termY = RED # rojo

blue = int(input('Accion cable azul: (1)cortar (2)dejar (3)reconectar'))
if( blue == ROUTE):
    term = int(input('Terminal de reconexion (1)NEGRA, (2)AMARILLA'))
    if( term == BLACK):
        termB = BLUE # azul
    if( term == YELLOW):
        termY = BLUE # azul

green = int(input('Accion cable verde: (1)cortar (2)dejar (3)reconectar'))
if( green == ROUTE):
    term = int(input('Terminal de reconexion (1)NEGRA, (2)AMARILLA'))
    if( term == BLACK):
        termB = GREEN # verde
    if( term == YELLOW):
        termY = GREEN # verde
"""
