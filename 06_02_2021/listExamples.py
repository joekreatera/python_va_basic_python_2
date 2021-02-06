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
    x = 0
    y = 0

f = open('points','x+')

for i in ___________:
    f.write(f'{i.x},{i.y}')

f.close()


# escrbie los puntos con x positiva en un archivo
# escribe los puntos con y positiva en otro archivo
