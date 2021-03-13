from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import OrthographicLens
from panda3d.core import Point3
from panda3d.core import Vec4

from panda3d.core import CollisionHandlerEvent, CollisionTraverser, CollisionNode
from panda3d.core import CollisionRay
from panda3d.core import CollisionBox

from panda3d.core import loadPrcFileData

loadPrcFileData('', 'win-size 640 480')
#loadPrcFileData('', 'want-directtools #t')
#loadPrcFileData('', 'want-tk #t')
loadPrcFileData("", "textures-auto-power-2 #f")
loadPrcFileData("", "textures-power-2 none")
loadPrcFileData("", "textures-square none")


class DonkeyKong(ShowBase):
    def __init__(self):
        super().__init__(self)
        
        self.scene = self.loader.loadModel('models/DKSet')
        self.scene.reparentTo(self.render)
        
        self.arcadeTexture = self.loader.loadTexture('models/dk-arcade.png')
        self.scene.setTexture(self.arcadeTexture)
        self.scene.setTransparency(1)
        
        self.blockTexture = self.loader.loadTexture('models/block.png')
        self.taskMgr.add(self.setup , "setup")
        self.taskMgr.add(self.update , "update")
        
        
    def pressUp(self):
        print("up")
        self.input["up"] = not self.input["up"]
    def pressDown(self):
        print("down")
        self.input["down"] = not self.input["down"]
    def pressLeft(self):
        print("left")
        self.input["left"] = not self.input["left"]
    def pressRight(self):
        print("right")
        self.input["right"] = not self.input["right"]
    def pressSpace(self):
        print("space")
        self.input["space"] = not self.input["space"]
        
    
    def setup(self, task):
        lens = OrthographicLens()
        lens.setFilmSize(25,20)
        base.camNode.setLens(lens)
        
        self.player = self.scene.attachNewNode("Player")
        self.scene.find('root/mario').reparentTo(self.player)
        self.player.setPos(7,0,-4.5)
        
        #input setup
        self.accept("raw-arrow_up", self.pressUp)
        self.accept("raw-arrow_down", self.pressDown)
        self.accept("raw-arrow_left", self.pressLeft)
        self.accept("raw-arrow_right", self.pressRight)
        self.accept("raw-space" , self.pressSpace)
        
        self.accept("raw-arrow_up-up", self.pressUp)
        self.accept("raw-arrow_down-up", self.pressDown)
        self.accept("raw-arrow_left-up", self.pressLeft)
        self.accept("raw-arrow_right-up", self.pressRight)
        self.accept("raw-space-up" , self.pressSpace)
        self.input = {
        'left':False,
        'right':False,
        'up':False,
        'down':False,
        'space':False
        }
        
        # collision handling
        base.cTrav  = CollisionTraverser()
        self.collisionHandlerEvent = CollisionHandlerEvent()
        self.collisionHandlerEvent.addInPattern('into-%in')
        self.collisionHandlerEvent.addOutPattern('outof-%in') 
        
        self.floor1 = self.scene.attachNewNode('Floor1')
        hitbox = CollisionBox( Point3(0,0,0) , 9.3, 5, .5 )
        cNodePath = self.floor1.attachNewNode( CollisionNode('floor1Hitbox') )
        cNodePath.node().addSolid(hitbox)
        cNodePath.node().setIntoCollideMask(0x01)
        cNodePath.node().setFromCollideMask(0x01)
        #cNodePath.show()
        base.cTrav.addCollider(cNodePath, self.collisionHandlerEvent)
        
        self.scene.find('root/floor0').reparentTo(self.floor1)
        self.floor1.setPos(-1.8,0,-5.5)
        self.floor1.setTexture(self.blockTexture)
        
        #base.cTrav.showCollisions(self.render)
        return Task.done
        
    def update(self, task):
        self.camera.setPos(0,35,0)
        self.camera.lookAt(self.scene)
        
        if(self.input["left"]):
            p = self.player.getPos()
            p.x = p.x + 0.5
            self.player.setPos(p)
        if(self.input["right"]):
            p = self.player.getPos()
            p.x = p.x - 0.5
            self.player.setPos(p)

        return Task.cont
        
dk = DonkeyKong()
dk.run()