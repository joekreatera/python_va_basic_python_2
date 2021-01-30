from random import random
r = int(random()*100)
resp = int(input('Si piensas que mi numero es mayor a 60, responde (2) , si piensas que es menor a 40, responde (0), si piensas que está entre 40 y 60 responde (1)') )
if( resp == 0 and r < 40 ):
    print("ganaste")
elif( resp == 1  and  r <= 60 and r >= 40 ):
    print("ganaste")
elif( resp == 2 and r > 60):
    print("ganaste")
else:
    print("perdiste")
print(f"Habia pensado en {r}")
