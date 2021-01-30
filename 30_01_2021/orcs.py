from random import random

# orcos
# magia
# fuerza
# arma (mazo, boleadoras, piedra)
# color (Cafe, negro, gris, rojo)
# vida
# amuleto
# se pueden mover

# funcion de creacion de orcos
# funcion de movimiento de orcos
# function de render de posicion de orcos

# simular 3 orcos, moviendose 3 vecs

def getRandom(a,b):
    return int(random()*(b-a)+a)

def createOrc():
    m = getRandom(4,10)
    f = getRandom(20,80)
    w = getRandom(1,3.9)
    c = getRandom(1,4.9)
    l = getRandom(90,140)
    a = getRandom(0,1.9)
    x = getRandom(-10,10)
    y = getRandom(-10,10)

    return m,f,w,c,l,a,x,y

def printOrc(m,f,w,c,l,a,x,y):
    print(f'magic:{m} force:{f} weapon:{w} color:{c} life:{l} amulet:{a} x:{x} y:{y}')

def printField(o1x,o1y,o2x,o2y,o3x,o3y):
    for i in range(0,20):
        line = ""
        for j in range(0,20):
            ny = i-10
            nx = j-10
            if(o1x == nx and o1y == ny):
                line = line + "X "
            elif(o2x == nx and o2y == ny):
                line = line + "Y "
            elif(o3x == nx and o3y == ny):
                line = line + "Z "
            else:
                line = line + "  "
        print(line)

orc1_magic = 0
orc1_force = 0
orc1_weapon = 0
orc1_color = 0
orc1_life = 0
orc1_amulet = 0
orc1_x = 0
orc1_y = 0

orc2_magic = 0
orc2_force = 0
orc2_weapon = 0
orc2_color = 0
orc2_life = 0
orc2_amulet = 0
orc2_x = 0
orc2_y = 0

orc3_magic = 0
orc3_force = 0
orc3_weapon = 0
orc3_color = 0
orc3_life = 0
orc3_amulet = 0
orc3_x = 0
orc3_y = 0

orc1_magic,orc1_force,orc1_weapon,orc1_color,orc1_life,orc1_amulet,orc1_x ,orc1_y = createOrc()
orc2_magic,orc2_force,orc2_weapon,orc2_color,orc2_life,orc2_amulet,orc2_x ,orc2_y = createOrc()
orc3_magic,orc3_force,orc3_weapon,orc3_color,orc3_life,orc3_amulet,orc3_x ,orc3_y = createOrc()

printOrc(orc1_magic,orc1_force,orc1_weapon,orc1_color,orc1_life,orc1_amulet,orc1_x ,orc1_y)
printOrc(orc2_magic,orc2_force,orc2_weapon,orc2_color,orc2_life,orc2_amulet,orc2_x ,orc2_y)
printOrc(orc3_magic,orc3_force,orc3_weapon,orc3_color,orc3_life,orc3_amulet,orc3_x ,orc3_y)

for i in range(0,10):
    printField(orc1_x ,orc1_y,orc2_x ,orc2_y,orc3_x ,orc3_y)
    orc1_x= orc1_x  + 1
    orc2_y= orc2_y  + 1
    orc3_x= orc3_x  - 1
    print("------------------------------")
