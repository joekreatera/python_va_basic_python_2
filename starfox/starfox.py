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
        self.z = 0
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


    def update(self, evt):        
        #self.camera.setPos(0,-100,100)
        #self.camera.lookAt(self.player)
        self.rails.setPos(self.scene,  Path.getXOfY(self.rails_y) , self.rails_y  , 20)
        self.rails.setHpr( Path.getHeading(self.rails_y) , 0, 0 )
        self.camera.setHpr( Path.getHeading(self.rails_y) , 0, 0 )
        
        self.rails_y = self.rails_y + globalClock.getDt()*10
        #self.player.setPos(self.rails, 0, 0, sin(self.z/10.0)*40 )
        
        relX, relZ = self.player.getPythonTag("ObjectController").update(self.rails, globalClock.getDt() )
        self.camera.setPos(self.rails, relX, -50, relZ)
        
        #print( InputManager.get_input(InputManager.arrowDown) )
        
        return Task.cont
        
sf = Starfox()
sf.run()
