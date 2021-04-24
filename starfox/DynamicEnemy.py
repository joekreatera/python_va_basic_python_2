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
        
        self.gameObject.find("**collision**").node().setFromCollideMask(0x5)
        self.gameObject.find("**collision**").node().setIntoCollideMask(0x5)
        
        self.type = type
        self.gameObject.setPythonTag("ObjectController", self)
        self.gameObject.setPos(world, origin)
        self.fromPos = origin
        self.gotoPos = target
        self.vel = vel
        self.state = ENEMY_STATE.IDLE
        self.radius = radius
        self.gameObject.setName("dynamicEnemy")
        self.activeTime = 0
        
        self.bulletTimer = 5
        self.cTrav = cTrav
        self.collisionHandler = collisionHandler
    
    
    def updateKamikaze(self, world, dt , player):
        dir = player.getPos(world) - self.gameObject.getPos(world)
        distance = dir.length()
        
        if(self.state == ENEMY_STATE.IDLE and distance <= 80):
            print("attack")
            self.state = ENEMY_STATE.ATTACK
            player_point_forward =  player.getPos(world)  + world.getRelativeVector(player, Vec3(0,1,0) )*40
            self.vel = (player_point_forward - self.gameObject.getPos(world) )
            self.vel.normalize()
            
        if( self.state == ENEMY_STATE.ATTACK):
            #pass
            self.gameObject.setPos(world, self.gameObject.getPos(world) + self.vel*dt*60 )
            self.activeTime = self.activeTime + dt
            if( self.activeTime > 3):
                self.gameObject.removeNode()
            
    def updateChaser(self, world, dt , player , bullet):
        
        dir = player.getPos(world) - self.gameObject.getPos(world)
        distance = dir.length()
        
        if(self.state == ENEMY_STATE.IDLE and distance <= 1200):
            print("attack")
            self.state = ENEMY_STATE.CHASE
            player_point_forward =  player.getPos(world)  + world.getRelativeVector(player, Vec3(0,1,0) )*40
            self.vel = (player_point_forward - self.gameObject.getPos(world) )
            self.vel.normalize()    
        
        if( self.state == ENEMY_STATE.CHASE and distance >= 50  ):
            self.gameObject.setPos(world, self.gameObject.getPos(world) + self.vel*dt*60 )
            self.state = ENEMY_STATE.ATTACK
            self.activeTime = 0
        
        if( self.state == ENEMY_STATE.ATTACK):
            self.activeTime = self.activeTime - dt
            if( self.activeTime <= 0):
                self.activeTime = 1
                player_point_forward =  player.getPos(world)  + world.getRelativeVector(player, Vec3(0,1,0) )*40
                self.gotoPos = player_point_forward
            
            self.bulletTimer = self.bulletTimer - dt
            if(self.bulletTimer <= 0):
                self.bulletTimer = 5
                b = Bullet(bullet, 
                    world, 
                    self.gameObject.getPos(world), 
                    self.cTrav,
                    self.collisionHandler,
                    self.scene.getRelativeVector(self.gameObject, Vec3(0,1,0) ) ,
                    40,
                    0x2
                    )   

            
            pos = player.getPos(world)
            pos.setZ( self.gameObject.getPos(world).getZ() + (self.gotoPos.getZ() - self.gameObject.getPos(world).getZ())*dt*2  )
             
            self.gameObject.setPos(world, pos + world.getRelativeVector(player, Vec3(0,1,0) )*40  )
        
    def update(self, world, dt , player, bullet):
        self.gameObject.setColor(1 , 0 , 1 , 1)
        
        if( self.type == ENEMY_TYPE.KAMIKAZE ):
            self.updateKamikaze( world, dt , player )
        
        if( self.type == ENEMY_TYPE.CHASER ):
            self.updateChaser( world, dt , player, bullet )
        
        
    def crash(self, obj):
        print(f'crashed with {obj}')
        if (obj is not None):
            self.gameObject.removeNode()