from random import random

# 0 stands for multiple
# 1 stands for strawberry
# 2 stands for chocolate
# 3 stands for grape
# 4 stands for vanilla

ball_cost = 10

def clientArrived():
    c = Customer()
    i = None

    if(random() > 0.5):
        i = Icecream( client = c )
    else:
        i = BananaSplitIcecream( client = c )

    print(f'C:{c}')

    return i.getPrice()


class Icecream:
    def __init__(self, client = None , bq = 1, fl = 1):
        if( client != None):
            self.__ball_qty = int(client.getMoney()/ball_cost)
            self.__flavor = client.getFavoriteFlavor()
        else:
            self.__ball_qty = bq
            self.__flavor = fl
        print(f'Icrecream flavor {self.__flavor}  with ball_qty {self.__ball_qty} ')
    def addBall(self):
        self.__ball_qty = self.__ball_qty + 1

    def getBallQty(self):
        return self.__ball_qty

    def getFlavor(self):
        return self.__flavor

    def setFlavor(self, f = 1):
        if( f >= 0 and f <= 4 ):
            self.__flavor = f
        else:
            print("Flavor not recognized")

    def getPrice(self):
        return self.__ball_qty*ball_cost

class BananaSplitIcecream(Icecream):
    def __init__(self, client = None):
        if( client == None):
            super().__init__(bq=0, fl = 0)
            print('No icecream dude')

        if( client != None):
            if( client.getMoney() >= 3*ball_cost ):
                super().__init__(bq=3, fl = 0)
            else:
                super().__init__(bq=0, fl = 0)
                print('No icecream dude')

    def setFlavor(self, f):
        print(f'Cannot change Banana Split Icecream flavor')
    def addBall(self):
        print(f'Cannot change Banana Split Icecream balls')

class Customer:
    def __init__(self):
        self.__name =  int(random()*4.99)
        self.__money =  random()*50+10
        self.__fflavor = int(random()*3.99+1)
    def getMoney(self):
        return self.__money
    def spentMoney(self, spending = 0):
        self.__money = self.__money - spending
    def getFavoriteFlavor(self):
        return self.__fflavor

    def __str__(self):
        n = ""
        if(self.__name == 0):
            n = "Mario"
        if(self.__name == 1):
            n = "Ana"
        if(self.__name == 2):
            n = "Dany"
        if(self.__name == 3):
            n = "Jorge"
        if(self.__name == 4):
            n = "Eva"

        return f'N: {n} M:{self.__money}'
    # debe tener un nombre Jesus, iva, Jose, Pedro, maria, Liz, Dayra, Roberta, y un sabor preferido
    # debe tener un sabor preferido entre 1 y 4
    # tiene una cantidad de dinero en su bolsillo
    # cada helado tiene un precio asociado por bola de helado de 10 pesos
    # asignale a cada cliente un helado del sabor que el prefiere e indica la ganancia de la tienda de helados
    # simulando la creacion del cliente (5) clientes, e imprimiendo el sabor que escogieron y las cantidad de helado.

amt = 0
amt = amt + clientArrived()
amt = amt + clientArrived()
amt = amt + clientArrived()
amt = amt + clientArrived()
amt = amt + clientArrived()

bs= BananaSplitIcecream()

print(f'Ganacia: {amt}')
