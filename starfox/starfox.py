from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import loadPrcFileData
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from InputManager import InputManager
from Player import Player
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
        self.rails.setPos(self.scene, 0,0,0)
        self.player.reparentTo(self.rails)
        self.player.setPos(self.rails,0,0,0)
        
    def update(self, evt):
        self.z = self.z + 0.1
        self.camera.setPos(0,20,100)
        self.camera.lookAt(self.rails)
        self.rails.setPos(0,self.z,0)
        
        #self.player.setPos(self.rails, 0, 0, sin(self.z/10.0)*40 )
        
        self.player.getPythonTag("ObjectController").update(self.rails, globalClock.getDt() )
        
        #print( InputManager.get_input(InputManager.arrowDown) )
        
        return Task.cont
        
sf = Starfox()
sf.run()
