# generar una funcion para entregar la distancia entre dos objetos en 3d
from math import sqrt

def distance(x1,y1,z1,x2,y2,z2):
    dx =x2-x1
    dy =y2-y1
    dz = z2-z1

    d = sqrt( dx**2 + dy**2 + dz**2)
    return d

def solve(a=1,b=1,c=1):
    disc = b*b - 4*a*c

    if( disc < 0):
        return False, False

    x1 = (-b + sqrt(disc))/(2*a)
    x2 = (-b - sqrt(disc))/(2*a)

    return x1,x2

def printAndSolve(a=1,b=1,c=1):
    v1,v2 = solve(a,b,c)
    print(f'v1:{v1} v2:{v2}')


r1 = distance(0,0,0,1,1,1)
printAndSolve()
printAndSolve(b=2)
printAndSolve(b=3)
printAndSolve(b=4)
printAndSolve(b=5)
printAndSolve(b=6)
printAndSolve(b=7)
print(r1)
