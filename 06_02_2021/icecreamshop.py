# 1 stands for strawberry
# 2 stands for chocolate
# 3 stands for grape
# 4 stands for vanilla

class Icecream:
    def __init__(self):
        self.__ball_qty = 1
        self.__flavor = 1
    def addBall(self):
        self.__ball_qty = self.__ball_qty + 1

    def getBallQty(self):
        return self.__ball_qty

    def getFlavor(self):
        return self.__flavor

    def setFlavor(self, f = 1):
        if( f >= 1 and f <= 2 ):
            self.__flavor = f
        else:
            print("Flavor not recognized")

class Customer:
    # debe tener un nombre Jesus, iva, Jose, Pedro, maria, Liz, Dayra, Roberta, y un sabor preferido
    # debe tener un sabor preferido entre 1 y 4
    # tiene una cantidad de dinero en su bolsillo
    # cada helado tiene un precio asociado por bola de helado de 10 pesos
    # asignale a cada cliente un helado del sabor que el prefiere e indica la ganancia de la tienda de helados
    # simulando la creacion del cliente (5) clientes, e imprimiendo el sabor que escogieron y las cantidad de helado.

ic1 = Icecream()
print(f'q:{ic1.getBallQty()} f:{ic1.getFlavor()}')

ic2 = Icecream()
print(f'q:{ic2.getBallQty()} f:{ic2.getFlavor()}')
ic2.addBall()
ic2.setFlavor(2)
print(f'q:{ic2.getBallQty()} f:{ic2.getFlavor()}')

ic2.setFlavor(3)
