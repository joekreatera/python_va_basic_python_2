from math import sqrt

"""
val = input('Dame un valor:')
val = int(val)
res = val**3
print( str(res) )
"""

#
# Ejercicio: un enemigo tiene una vida
# El usuario introduce el hit
# el programa indica la vida del enemigo posterior al hit

#print( (100 - int( input('Hit force:') )) )

#print(sqrt(100))


""""
rp = 7
rt = 5
minD = rp + rt

x1 = int ( input ('X player '))
y1 = int ( input ('Y player '))
x2 = int ( input ('X treasure '))
y2 = int ( input ('Y treasure '))
d = sqrt( (x1-x2)**2 + (y1-y2)**2  )
print(f' Distance P->T is {d}' )
v = max(d,minD-1)
print(f'Value P->T (11->touched) is {v}')
"""


"""
Hay un hechicero que tiene un caldero. El caldero se llama RGB,
El usuario debe indicar al hechicero la cantidad de cada uno de los componentes del hechizo que colocara
en el caldero RGB

0-> 255 Ml {Rooibos, Greenish, Boost} > 765 ml

2 Lts pocion:> Cuanto componente se crea de cada sustancia ingresada.

Cual es el color final lineal de acuerdo a cantidades posterior al hechizo:

Formula = ColorFinal  = (QtyR)/2000 + QtyG*255/2000  + QtyB*255*255/2000

"""

"""
f = 2.615
r = int ( input ('Rooibos: '))
g = int ( input ('Greenish: '))
b = int ( input ('Boost: '))

r = r*f
g = g*f
b = b*f

print(f'final amount r:{r} g:{g} b:{b} ')
qty = r+g+b
print(f'final lts:{qty} ')
color = r/2000 +  g*255/2000 + b*255**2/2000
print(f'final linear color: {color}')
"""


"""

RPG, construyendo tu personaje, y calculando el nivel de fuerza
{espada=100, mazo=120} base:100 +20
{escudo=20, nada=200} base:20 + 180
{botas fuego=40, botas agua=20} base: 20 + 20
Cuanta fuerza tiene el personaje?

No hay If's
"""
sw = int(input('Weapon: (0)=>sword , (1)=>hammer:'))
sh = int(input('Shield: (0)=>shield , (1)=>i am not frightened:'))
fr = int(input('Boots: (0)=>water boots , (1)=>fire boots:'))

force = 100+sw*20 + 20+sh*180 + 20 + fr*20

print(f' Force got : {force}')
