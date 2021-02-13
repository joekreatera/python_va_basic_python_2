from random import random
# lists
my_list = [10,20,30,40,50]

my_list.append(40)
my_list[2] = 30

print(my_list[-1])

my_list2 = my_list[:3]

print(my_list)
print(my_list2)


my_list.pop()
print(my_list)

rng = range(10,50)
print(rng)

i = 0
while i < 3:
    print(my_list[i])
    i = i+1

print('range list ')
for i in range(0,3):
    print(my_list[i])

print('for len')
for i in range(0, len(my_list) ):
    print(my_list[i])

print('for list')
for i in my_list:
    print(i)

# class Point con dos atributos: x , y inicializados con aleatorios entre -100 y 100
# genera una lista con solo los puntos que tengan x positiva
# genera una lista con solo los puntos que tengan y positiva
class Point:
    def __init__(self):
        self.x = random()*200-100
        self.y = random()*200-100

points = []
pos_x = []
pos_y = []
for i in range(0,100):
    p = Point()
    points.append( p )
    if p.x > 0 :
        pos_x.append(p)
    if p.y > 0 :
        pos_y.append(p)


print(len(pos_x))
# filtering., 3 types
pos_x = [e for e in points if e.x > 0 ]
print(len(pos_x))
pos_x = list(filter( lambda x: x.x>0 , pos_x))
print(len(pos_x))
# end filtering


def sumUp(p):
    pt = Point()
    pt.x = p.x + 100
    pt.y = p.y + 100
    return pt


def reverse(p):
    pt = Point()
    pt.x = p.x * -1
    pt.y = p.y * -1
    return pt

f = open('points.csv','x+')
fr = open('pointsR.csv','x+')

fx = open('pointsX.csv','x+')
fy = open('pointsY.csv','x+')

pointsReversed = (map(reverse, points))

for i in points:
    f.write(f'{i.x},{i.y}\n')

for i in pointsReversed:
    fr.write(f'{i.x},{i.y}\n')

for i in pos_x:
    fx.write(f'{i.x},{i.y}\n')


for i in pos_y:
    fy.write(f'{i.x},{i.y}\n')

f.close()
fx.close()
fy.close()
fr.close()
# escribe los puntos con x positiva en un archivo
# escribe los puntos con y positiva en otro archivo
