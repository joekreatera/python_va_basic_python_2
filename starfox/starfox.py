from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import loadPrcFileData
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from InputManager import InputManager
from Player import Player
from Path import Path
from math import sin
from DynamicEnemy import *
class Starfox(ShowBase):
    def __init__(self):
        self.height= 500
        super().__init__(self)
        self.scene = self.loader.loadModel("./models/world.egg")
        self.scene.reparentTo(self.render)
        
        self.player = self.scene.find("player")
        self.player.setPythonTag("ObjectController" , Player(self.player) )
        
        self.building_enemy = self.scene.find("building_enemy")
        self.dynamic_enemy = self.scene.find("enemy1")
        
        base.cTrav = CollisionTraverser()
        self.CollisionHandlerEvent = CollisionHandlerEvent()
        base.enableParticles()
        self.CollisionHandlerEvent.addInPattern('into-%in')
        self.CollisionHandlerEvent.addOutPattern('out-%in')
        
        
        self.accept('into-collision_player', self.crash)
        self.accept('into-collision_plane', self.crash)
        
        base.cTrav.addCollider( self.scene.find("player/collision**"), self.CollisionHandlerEvent)
        base.cTrav.addCollider( self.scene.find("basePlane/collision**"), self.CollisionHandlerEvent)
        base.cTrav.showCollisions(self.render)
        
        
        self.taskMgr.add(self.update, "update")
        InputManager.initWith(self , [ 
        InputManager.arrowUp,
        InputManager.arrowDown,
        InputManager.arrowLeft,
        InputManager.arrowRight,
        InputManager.space,
        InputManager.keyX,
        InputManager.keyV 
        ] )        
        
        self.rails = self.scene.attachNewNode("rails")
        self.scene.find("basePlane").setHpr(70,0,0)
        self.rails.setPos(self.scene, 0,0,0)
        self.player.reparentTo(self.rails)
        self.player.setPos(self.rails,0,0,0)
        self.rails_y = -50
        
        self.createStaticEnemy(self.building_enemy, 0,50,0)
        self.createStaticEnemy(self.building_enemy, -50,50,0)
        self.createStaticEnemy(self.building_enemy, -100,50,0)
        self.createStaticEnemy(self.building_enemy, -70,130,0)
        self.createStaticEnemy(self.building_enemy, -120,80,0)
        self.createStaticEnemy(self.building_enemy, -220,130,0)
        
        DynamicEnemy(self.dynamic_enemy, self.scene, Vec3(-230,140,10) ,  base.cTrav, self.CollisionHandlerEvent , radius = 80) 
        #DynamicEnemy(self.dynamic_enemy, self.scene, Vec3(-240,160,10) ,  base.cTrav, self.CollisionHandlerEvent) 
        #DynamicEnemy(self.dynamic_enemy, self.scene, Vec3(-250,200,10) ,  base.cTrav, self.CollisionHandlerEvent) 
        #DynamicEnemy(self.dynamic_enemy, self.scene, Vec3(-270,160,10) ,  base.cTrav, self.CollisionHandlerEvent) 
        #DynamicEnemy(self.dynamic_enemy, self.scene, Vec3(-250,200,10) ,  base.cTrav, self.CollisionHandlerEvent) 
        
        self.building_enemy.hide()
        self.dynamic_enemy.hide();

    def createStaticEnemy(self, original, px, py, pz):
        be = original.copyTo(self.scene)
        be.setPos(px,py,pz)
        base.cTrav.addCollider( be.find("**collision**") , self.CollisionHandlerEvent )
        

    def crash(self, evt):
        print(evt)
        objectInto = evt.getIntoNodePath().node().getParent(0).getPythonTag("ObjectController")
        objectFrom = evt.getFromNodePath().node().getParent(0).getPythonTag("ObjectController")
        
        if( objectInto != None):
            objectInto.crash(objectFrom)

        if( objectFrom != None):
            objectFrom.crash(objectInto)
        

    def update(self, evt):        
        #self.camera.setPos(0,-100,100)
        
        # -> self.camera.lookAt(self.player)
        self.rails.setPos(self.scene,  Path.getXOfY(self.rails_y) , self.rails_y  , 12.4)
        self.rails.setHpr( Path.getHeading(self.rails_y) , 0, 0 )
        # -> self.camera.setHpr( Path.getHeading(self.rails_y) , 0, 0 )
        
        self.rails_y = self.rails_y + globalClock.getDt()*10
        #self.player.setPos(self.rails, 0, 0, sin(self.z/10.0)*40 )
        
        relX, relZ = self.player.getPythonTag("ObjectController").update(self.rails, globalClock.getDt() )
        # -> self.camera.setPos(self.rails, relX, -30, relZ)
        
        
        # start debug section
        
        levelUp = (InputManager.get_input( InputManager.keyX ) )
        levelDown = (InputManager.get_input( InputManager.keyV ) )
        
        if( levelUp ):
            self.height = self.height + 10
        if( levelDown ):
            self.height = self.height - 10
            
        
        self.camera.setPos(self.rails.getX(), self.rails.getY() , self.height )
        self.camera.lookAt(Vec3(self.rails.getX(), self.rails.getY(),0) )
        
        # end debug section
    
        enemies = self.scene.findAllMatches("dynamicEnemy")
        for e in enemies:
            enemy = e.getPythonTag("ObjectController")
            enemy.update(self.scene, globalClock.getDt()  , self.player)
            
        return Task.cont
        
sf = Starfox()
sf.run()
