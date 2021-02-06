# 1 stands for strawberry
# 2 stands for chocolate

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

ic1 = Icecream()
print(f'q:{ic1.getBallQty()} f:{ic1.getFlavor()}')

ic2 = Icecream()
print(f'q:{ic2.getBallQty()} f:{ic2.getFlavor()}')
ic2.addBall()
ic2.setFlavor(2)
print(f'q:{ic2.getBallQty()} f:{ic2.getFlavor()}')

ic2.setFlavor(3)
