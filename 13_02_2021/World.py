from math import sqrt
from random import random
"""
 ORC: 1000-2500
 ELF: 1500-2000

"""
ORC_START_MAX_LIFE = 2500
ORC_START_MIN_LIFE = 1000
ELF_START_MAX_LIFE = 2000
ELF_START_MIN_LIFE = 1500
MAX_GRID_UNITS_X = 100
MAX_GRID_UNITS_Y = 100


def getRandomBetween(min,max):
    return random()*(max-min)+min

def getDistance(x1,y1,x2,y2):
    return sqrt( (x2-x1)**2 + (y2-y1)**2  )

class Creature:
    def __init__(self):
        self.magic = 0
        self.life = 0
        self.start_life = 0
        self.strength = 0
        self.x = 0
        self.y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.strength_mult = 1
        self.magic_mult = 1
        self.x = int(getRandomBetween(0,MAX_GRID_UNITS_X))
        self.y = int(getRandomBetween(0,MAX_GRID_UNITS_Y))
        self.opponent = None
        self.mate = None
    def setOpponent(self,opp):
        self.opponent = opp
    def getOpponent(self):
        return self.opponent
    def setMate(self, m):
        self.mate = m
    def isFighting(self):
        return self.opponent is not  None
    def isMating(self):
        return self.mate is not  None
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getSpeedX(self):
        return self.speed_x
    def getSpeedY(self):
        return self.speed_y
    def getItem(self, item):
        return True
    def getHit(self):
        return self.strength*self.strength_mult + self.magic*self.magic_mult
    def setDamage(self, damage):
        self.life = self.life - damage
    def isAlive(self):
        return self.life > 0
    def move(self):
        self.x = self.x + self.speed_x
        self.y = self.y + self.speed_y
    def invertSpeedX(self):
        self.speed_x = self.speed_x * -1
    def invertSpeedY(self):
        self.speed_y = self.speed_y * -1
    def newSpeed(self):
        self.speed_x = int(getRandomBetween(-8,8))
        self.speed_y = int(getRandomBetween(-8,8))
    def __str__(self):
        # https://stackoverflow.com/questions/45310254/fixed-digits-after-decimal-with-f-strings
        return f'(x:{self.x} y:{self.y} l:{self.life:.2f} m:{self.magic:.2f} s:{self.strength:.2f})'

class Elf(Creature):
    def __init__(self):
        super().__init__()
        self.start_life = getRandomBetween(ELF_START_MIN_LIFE, ELF_START_MAX_LIFE)
        self.life = self.start_life
        self.strength_mult = 0.2
        self.magic_mult = 0.8
        self.magic = getRandomBetween(60,120)
        self.strength = getRandomBetween(20,50)
        self.newSpeed()

class Orc(Creature):
    def __init__(self):
        super().__init__()
        self.start_life = getRandomBetween(ORC_START_MIN_LIFE, ORC_START_MAX_LIFE)
        self.life = self.start_life
        self.strength_mult = 0.7
        self.magic_mult = 0.3
        self.magic = getRandomBetween(1,10)
        self.strength = getRandomBetween(50,140)
        self.newSpeed()

class Troll(Creature):
    def __init__(self):
        super().__init__()
        self.start_life = getRandomBetween(100000, 200000)
        self.life = self.start_life
        self.strength_mult = 5
        self.magic_mult = 5
        self.magic = getRandomBetween(1000,2000)
        self.strength = getRandomBetween(1000,2000)


class World:
    def __init__(self, elfs = 0, orcs = 0, trolls = 0):
        self.creatures = []
        self.items = []
        self.elf_hordes = []
        self.orc_hordes = []
        self.day = 0
        self.trolls = []

        for i in range(0,elfs):
            self.creatures.append( Elf() )
        for i in range(0,orcs):
            self.creatures.append( Orc() )
        """
        for i in range(0,trolls):
            self.creatures.append( Troll() )
        """

    def moveCreature(self , creature , days):

        if(days%5 == 0):
            creature.newSpeed()
        if( creature.getX()+creature.getSpeedX() > MAX_GRID_UNITS_X and creature.getSpeedX() > 0 ):
            creature.invertSpeedX()
        if( creature.getX()+creature.getSpeedX() < 0 and creature.getSpeedX() < 0 ):
            creature.invertSpeedX()

        if( creature.getY()+creature.getSpeedY() > MAX_GRID_UNITS_Y and creature.getSpeedY() > 0 ):
            creature.invertSpeedY()
        if( creature.getY()+creature.getSpeedY() < 0  and creature.getSpeedY() < 0):
            creature.invertSpeedY()
        creature.move()

    def fight(self, c1, c2):
        print("fight")

        if( not c1.isFighting() and  not c2.isFighting() and c1.isAlive() and c2.isAlive() and not c1.isMating() and not c2.isMating() ):
            print("fighting!!!")
            c1.setOpponent(c2)
            c2.setOpponent(c1)

        if c1.getOpponent() is c2:
            print("fighting!!! c2")
            c1.setDamage(c2.getHit())
            c2.setDamage(c1.getHit())

        if not (c1.isAlive() and c2.isAlive()):
            print("WIN!! g!!!")

            c1.setOpponent(None)
            c2.setOpponent(None)

    def horde(self, c1, c2):
        print("horde")
        return 0


    def update(self):
        self.day = self.day + 1
        for i in range(0,len(self.creatures)):
            isFighting = False
            a = self.creatures[i]
            for j in range(i+1, len(self.creatures) ) :
                b =self.creatures[j]
                d = getDistance( a.getX(), a.getY(), b.getX() , b.getY())
                if d <= 100:
                    if type(a) == type(b):
                        self.horde(a,b)
                    else:
                        self.fight(a,b)

            if not isFighting:
                self.moveCreature(a, self.day)

    def debug(self):
        creatures = ""
        for i in self.creatures:
            creatures =  creatures + f' {i}'
        print(creatures)

    def __str__(self):

        creatures = ""
        for i in self.creatures:
            creatures =  creatures + f' {i}'

        return f'Day:{self.day}\n\
        Creatures\n{creatures}\n\
        Elves\n{self.elf_hordes}\n\
        Orcs\n{self.orc_hordes}\n\
        Items\n{self.items}\n\
        Trolls\n{self.trolls}'

w = World(1,1,1)



for i in range(0,16):
    w.update()
    #w.debug()
    print(f'{w}')
