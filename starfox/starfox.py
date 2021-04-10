from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import loadPrcFileData
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from InputManager import InputManager
from Player import Player
from Path import Path
from math import sin
class Starfox(ShowBase):
    def __init__(self):
        super().__init__(self)
        self.scene = self.loader.loadModel("./models/world.egg")
        self.scene.reparentTo(self.render)
        
        self.player = self.scene.find("player")
        self.player.setPythonTag("ObjectController" , Player(self.player) )
        
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
        #self.camera.lookAt(self.player)
        self.rails.setPos(self.scene,  Path.getXOfY(self.rails_y) , self.rails_y  , 12.4)
        self.rails.setHpr( Path.getHeading(self.rails_y) , 0, 0 )
        self.camera.setHpr( Path.getHeading(self.rails_y) , 0, 0 )
        
        self.rails_y = self.rails_y + globalClock.getDt()*10
        #self.player.setPos(self.rails, 0, 0, sin(self.z/10.0)*40 )
        
        relX, relZ = self.player.getPythonTag("ObjectController").update(self.rails, globalClock.getDt() )
        self.camera.setPos(self.rails, relX, -30, relZ)
        
        #print( InputManager.get_input(InputManager.arrowDown) )
        
        return Task.cont
        
sf = Starfox()
sf.run()
