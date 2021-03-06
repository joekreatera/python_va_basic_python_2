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

AMULET_ITEM = 0
WEAPON_ITEM = 1
HEALING_ITEM = 2

def getRandomBetween(min,max):
    return random()*(max-min)+min

def getDistance(x1,y1,x2,y2):
    return sqrt( (x2-x1)**2 + (y2-y1)**2  )

class Horde:
    # when fighting the opponent on creature will not be set as there can be many to one Battle
    def __init__(self):
        self.members = []
        self.opponent = None
        self.x = 0
        self.y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.mate = None

    def addMember(self, creature):
        self.members.append(creature)
    def getMembers(self):
        return self.members
    def setMate(self, m):
        self.mate = m
    def isFighting(self):
        return self.opponent is not  None
    def isMating(self):
        return self.mate is not  None
    def setOpponent(self, opp):
        self.opponent =  opp
    def getOpponent(self):
        return self.opponent
    def isAlive(self):
        for i in self.members:
            if i.isAlive:
                return True
        return False
    def move(self):
        cx = 0
        cy = 0

        for i in self.members:
            i.move( [self.speed_x, self.speed_y] )
            cx = cx + i.getX()
            cy = cy + i.getY()

        self.x = int(cx/len(self.members))
        self.y = int(cy/len(self.members))

    def invertSpeedX(self):
        self.speed_x = self.speed_x * -1
    def invertSpeedY(self):
        self.speed_y = self.speed_y * -1
    def newSpeed(self):
        self.speed_x = int(getRandomBetween(-4,4))
        self.speed_y = int(getRandomBetween(-4,4))
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getSpeedX(self):
        return self.speed_x
    def getSpeedY(self):
        return self.speed_y

    def takeItems(self, items):
        for i in self.members:
            for j in items:
                dist = getDistance(i.getX(), i.getY(), j.getX(), j.getY())
                if dist < 5 :
                    j.apply(i)

    def cleanMembers(self):
        alive = []
        for i in self.members:
            if i.isAlive():
                alive.append(i)
        self.members = alive
    def __str__(self):
        res = "" + f'x:{self.x} y:{self.y} sx:{self.speed_x} sy:{self.speed_y} \n'
        for i in self.members:
            res = res + f'{i}{i.life}\n'
        return res


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
    def addMagic(self, m):
        self.magic = self.magic + m
    def addStrength(self, s):
        self.strength = self.strength + s
    def recover(self, pct):
        self.life = min(self.start_life ,  self.life + int(self.start_life*pct))
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
        self.life = max(0,self.life - damage )
    def takeItems(self, items):
        for j in items:
            dist = getDistance(self.getX(), self.getY(), j.getX(), j.getY())
            if dist < 5 :
                j.apply(self)
    def isAlive(self):
        return self.life > 0
    def move(self, us =  None ):

        if(us is None):
            self.x = self.x + self.speed_x
            self.y = self.y + self.speed_y
        else:
            self.speed_x = us[0]
            self.speed_y = us[1]
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


class Item:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.taken = False

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def isTaken(self):
        return self.taken

    def apply(self, creature):
        if( self.taken ):
            return
        self.taken = True

        if type(creature) is Elf and self.type == AMULET_ITEM :
            creature.addMagic(40)
        if type(creature) is Orc and self.type == WEAPON_ITEM :
            creature.addStrength(30)
        if type(creature) is Elf and self.type == WEAPON_ITEM :
            creature.addStrength(10)
        if(self.type == HEALING_ITEM):
            creature.recover(0.5)

        print(f"\n ****** ITEM Applying item {self.type} to {creature} \n")

class World :
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

        for i in range(0,trolls):
            self.trolls.append( Troll() )

        self.items.append( Item(AMULET_ITEM, getRandomBetween(0, 100), getRandomBetween(0, 100) ) )
        self.items.append( Item(AMULET_ITEM, getRandomBetween(0, 100), getRandomBetween(0, 100) ) )
        self.items.append( Item(WEAPON_ITEM, getRandomBetween(0, 100), getRandomBetween(0, 100) ) )
        self.items.append( Item(WEAPON_ITEM, getRandomBetween(0, 100), getRandomBetween(0, 100) ) )
        self.items.append( Item(HEALING_ITEM, getRandomBetween(0, 100), getRandomBetween(0, 100) ) )
        self.items.append( Item(HEALING_ITEM, getRandomBetween(0, 100), getRandomBetween(0, 100) ) )

    def moveEntity(self , entity , days):

        if(days%5 == 0):
            entity.newSpeed()
        if( entity.getX()+entity.getSpeedX() > MAX_GRID_UNITS_X and entity.getSpeedX() > 0 ):
            entity.invertSpeedX()
        if( entity.getX()+entity.getSpeedX() < 0 and entity.getSpeedX() < 0 ):
            entity.invertSpeedX()

        if( entity.getY()+entity.getSpeedY() > MAX_GRID_UNITS_Y and entity.getSpeedY() > 0 ):
            entity.invertSpeedY()
        if( entity.getY()+entity.getSpeedY() < 0  and entity.getSpeedY() < 0):
            entity.invertSpeedY()
        entity.move()

    def fight(self, c1, c2):

        if( not c1.isFighting() and  not c2.isFighting() and c1.isAlive() and c2.isAlive() and not c1.isMating() and not c2.isMating() ):
            c1.setOpponent(c2)
            c2.setOpponent(c1)

        if c1.getOpponent() is c2:
            c1.setDamage(c2.getHit())
            c2.setDamage(c1.getHit())

            if not (c1.isAlive() and c2.isAlive()):
                c1.setOpponent(None)
                c2.setOpponent(None)

    def horde(self, c1, c2):
        print("horde!")
        if( not c1.isFighting() and  not c2.isFighting() and c1.isAlive() and c2.isAlive() and not c1.isMating() and not c2.isMating() ):
            c1.setMate(c2)
            c2.setMate(c1)

            h = Horde()
            h.addMember(c1)
            h.addMember(c2)

            return h
        return None

    def horde_fight(self, m1,m2):

        a = m1 if (len(m1) > len(m2) ) else m2
        b = m2 if (len(m1) > len(m1) ) else m1

        i = 0
        j = 0
        for i in range (0, len(a) ):
            c1 = a[i]
            c2 = b[i%len(b)]
            c1.setDamage(c2.getHit())
            c2.setDamage(c1.getHit())

        print( f'{a}{b}')

    def hordes_fight(self, h1, h2):
        a = h1
        b = h2
        if (not a.isFighting() and not a.isMating() and a.isAlive()) and  (not b.isFighting() and not b.isMating() and b.isAlive()):
            h1.setOpponent(h2)
            h2.setOpponent(h1)

        if h1.getOpponent() is h2:
            print( "fighting!!!!")
            self.horde_fight( h1.getMembers() , h2.getMembers()  )
            h1.cleanMembers()
            h2.cleanMembers()
            if( not (h1.isAlive()  and h2.isAlive() ) ):
                print("******************** dead!")
                h1.setOpponent(None)
                h2.setOpponent(None)


    def update(self):
        minDistance = 50
        self.day = self.day + 1

        # update move and horde merging
        hordes_to_remove = []
        for i in range(0, len(self.elf_hordes)):
            a = self.elf_hordes[i]
            a.takeItems(self.items)
            if( not a.isMating() and not a.isFighting() and a.isAlive()  ):
                for j in range(i+1, len(self.elf_hordes)):
                    b = self.elf_hordes[j]
                    print("do")
                    if (not a.isMating() and a.isAlive() and not a.isFighting()) and (not b.isMating and b.isAlive() and not b.isFighting()):
                        a.setMate(b)
                        b.setMate(a)
                        a.getMembers().extend(b.getMembers())
                        hordes_to_remove.append(b)

                if not self.elf_hordes[i].isMating() :
                    self.moveEntity(self.elf_hordes[i], self.day)

        i = 0
        h_len = len(hordes_to_remove)
        while i < h_len:
            self.elf_hordes.remove(  hordes_to_remove.pop(0)  )
            i = i+1

        hordes_to_remove = []
        # update move and horde merging
        for i in range(0, len(self.orc_hordes)):
            a = self.orc_hordes[i]
            a.takeItems(self.items)
            if( not a.isMating() and not a.isFighting() and a.isAlive()  ):
                for j in range(i+1, len(self.orc_hordes)):
                    b = self.orc_hordes[j]
                    print("do")
                    if (not a.isMating() and a.isAlive() and not a.isFighting()) and (not b.isMating and b.isAlive() and not b.isFighting()):
                        a.setMate(b)
                        b.setMate(a)
                        a.getMembers().extend(b.getMembers())
                        hordes_to_remove.append(b)

                if not self.orc_hordes[i].isMating() :
                    self.moveEntity(self.orc_hordes[i], self.day)


        # check fighting

        # check dead ones
        dead_elf_hordes = []
        dead_orc_hordes = []

        for i in range(0, len(self.elf_hordes)):
            a = self.elf_hordes[i]

            for j in range(0, len(self.orc_hordes)):
                b = self.orc_hordes[j]
                d = getDistance( a.getX(), a.getY(), b.getX() , b.getY())
                if d <= minDistance:
                    self.hordes_fight(a,b)

                if( b.isAlive() ):
                    for j in self.trolls:
                        d = getDistance( b.getX(), b.getY(), j.getX() , j.getY())
                        if( d <= minDistance ):
                            for m in b.getMembers():
                                m.setDamage( j.getHit() )
                                print("***************************** AAAAHRRRRRRRRRR TROLL")
                            break;
                if( not b.isAlive() ):
                    dead_orc_hordes.append(b) if b not in dead_orc_hordes else dead_orc_hordes
            # check trolls
            for j in self.trolls:
                d = getDistance( a.getX(), a.getY(), j.getX() , j.getY())
                if( d <= minDistance ):
                    for m in a.getMembers():
                        m.setDamage( j.getHit() )
                        print("***************************** AAAAHRRRRRRRRRR TROLL")
                    break;

            if( not a.isAlive() ):
                dead_elf_hordes.append(a)

            if( not a.isFighting() and not a.isMating() and a.isAlive()  ):
                for j in range(0, len(self.creatures)):
                    b = self.creatures[j]
                    d = getDistance( a.getX(), a.getY(), b.getX() , b.getY())
                    if d <= minDistance:
                        if type(b) is Elf:
                            if not b.isFighting() and not b.isMating() and b.isAlive():
                                a.addMember(b)
                                b.setMate(a)
                        if type(b) is Orc:
                            if not b.isFighting() and not b.isMating() and b.isAlive():
                                print("DEAD BY ELF HORDE")
                                b.setDamage(1000000) # die because many guys got to you

        for i in dead_elf_hordes:
            self.elf_hordes.remove(i)
        for i in dead_orc_hordes:
            self.orc_hordes.remove(i)



        for i in range(0, len(self.orc_hordes)):
            a = self.orc_hordes[i]
            if( not a.isFighting() and not a.isMating() and a.isAlive()  ):
                for j in range(0, len(self.creatures)):
                    b = self.creatures[j]
                    d = getDistance( a.getX(), a.getY(), b.getX() , b.getY())
                    if d <= minDistance:
                        if type(b) is Orc:
                            if not b.isFighting() and not b.isMating() and b.isAlive():
                                a.addMember(b)
                                b.setMate(a)
                        if type(b) is Elf:
                            if not b.isFighting() and not b.isMating() and b.isAlive():
                                print("DEAD BY ORC HORDE")
                                b.setDamage(1000000) # die because many guys got to you

        i = 0
        while i < len(self.elf_hordes) :
            a = self.elf_hordes[i]
            if( len(a.getMembers() ) == 1 ):
                self.creatures.append( a.getMembers()[0] )
                self.elf_hordes.remove(a)
            else:
                i = i+1

        i = 0
        while i < len(self.orc_hordes) :
            a = self.orc_hordes[i]
            if( len(a.getMembers() ) == 1 ):
                self.creatures.append( a.getMembers()[0] )
                self.orc_hordes.remove(a)
            else:
                i = i+1


        for i in range(0,len(self.creatures)):
            isFighting = False
            a = self.creatures[i]
            a.takeItems(self.items)
            for j in range(i+1, len(self.creatures) ) :
                b =self.creatures[j]
                d = getDistance( a.getX(), a.getY(), b.getX() , b.getY())
                if d <= minDistance:
                    if type(a) == type(b):
                        h = self.horde(a,b)
                        if h is not None:
                            if type(a) is Elf:
                                self.elf_hordes.append(h)
                            if type(a) is Orc:
                                self.orc_hordes.append(h)
                    else:
                        self.fight(a,b)

            if not isFighting:
                self.moveEntity(a, self.day)

        c = 0
        alive = []
        keep = True
        while keep and len(self.creatures) > 0  :
            # self.creatures[:c]
            # self.creatures[c+1:]
            if not self.creatures[c].isMating():
                if self.creatures[c].isAlive():
                    alive.append( self.creatures[c] )
            else:
                self.creatures[c].setMate(None)
            c = c+1
            if( c == len(self.creatures)):
                keep = False

        """
        [x]Agregar un metodo que regrese el valor de "taken"
        [x]Eliminar item de lista de items cuando este "taken"
        Aplicar los nuevos specs a la creatura
        """
        i = 0
        while i < len(self.items):
            if(self.items[i].isTaken() ):
                self.items.remove(self.items[i])
            else:
                i = i + 1
        self.creatures = alive

    def debug(self):
        creatures = ""
        for i in self.creatures:
            creatures =  creatures + f' {i}'
        print(creatures)

    def __str__(self):

        creatures = ""
        for i in self.creatures:
            creatures =  creatures + f' {i}'


        elf_horde_str = ""
        for i in self.elf_hordes:
            elf_horde_str =  elf_horde_str + f' {i}'

        orc_horde_str = ""
        for i in self.orc_hordes:
            orc_horde_str =  orc_horde_str + f' {i}'

        return f'Day:{self.day}\n\
        Creatures\n{creatures}\n\
        Elves\n{elf_horde_str}\n\
        Orcs\n{orc_horde_str}\n\
        Items\n{self.items}\n\
        Trolls\n{self.trolls}'

w = World(5,5,10)

"""
Tareas
- Crear una raza humana que no anda en hordas, solo anda por ahi
- La raza humana puede encontrarse amuletos y armas y utilizarlas para DUPLICAR sus stats
- Los humanos tienen todos un mismo comienzo de fuerza y magia del 50% del elfo mas debil
- Existen 1 dragon en el escenario, si alguien lo encuentra, y lo domina (aleatoriamente) se quedará
con el hacia donde vaya y hará un daño al otro de 1000. Si una horda se encuentra con un dragon, mataran al dragon
Si una creatura se encuentra con un dragon, si aleatoriamente (>0.5) la creatura gana, lo domina, de cualquier otra
manera, la creatura muere.

"""


for i in range(0,50):
    w.update()
    #w.debug()
    print(f'{w}')
