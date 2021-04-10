from enum import Enum
from panda3d.core import Vec3
from random import random
class ENEMY_TYPE(Enum):
    KAMIKAZE = 0
    CHASER = 1

class ENEMY_STATE(Enum):
    IDLE = 0
    CHASE = 1
    ATTACK = 2

class DynamicEnemy:
    def __init__(self, original, world, origin ,  cTrav, collisionHandler, type=ENEMY_TYPE.KAMIKAZE , target=None , vel=None, radius = 10000):
        self.gameObject = original.copyTo(world)
        cTrav.addCollider( self.gameObject.find("**collision**") , collisionHandler )
        self.type = type
        self.gameObject.setPythonTag("ObjectController", self)
        self.gameObject.setPos(world, origin)
        self.fromPos = origin
        self.gotoPos = target
        self.vel = vel
        self.state = ENEMY_STATE.IDLE
        self.radius = radius
        self.gameObject.setName("dynamicEnemy")
    
    def update(self, world, dt):
        self.gameObject.setColor(random() , random() , random() , 1)
        print("updating")
        
    def crash(self, obj):
        print(f'crashed with {obj}')