from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import loadPrcFileData
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from InputManager import InputManager

class Starfox(ShowBase):
    def __init__(self):
        super().__init__(self)
        self.scene = self.loader.loadModel("./models/world.egg")
        self.scene.reparentTo(self.render)
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
    def update(self, evt):
        self.z = self.z + 1
        self.camera.setPos(0,20,self.z)
        self.camera.lookAt(self.scene)
        
        print( InputManager.debug() )
        #print( InputManager.get_input(InputManager.arrowDown) )
        
        return Task.cont
        
sf = Starfox()
sf.run()
