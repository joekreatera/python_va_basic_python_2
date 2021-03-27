from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import OrthographicLens
from panda3d.core import Point3
from panda3d.core import Vec4, Vec3

from panda3d.core import CollisionHandlerEvent, CollisionTraverser, CollisionNode
from panda3d.core import CollisionSegment
from panda3d.core import CollisionBox, CollisionSphere

from panda3d.core import loadPrcFileData

from panda3d.physics import *
from direct.interval.IntervalGlobal import *

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
        self.stairsTexture = self.loader.loadTexture('models/stairs.png')
        self.taskMgr.add(self.setup , "setup")
        self.taskMgr.add(self.update , "update")
        self.jumpAvailable = False
        self.baseTime = 0;
        self.v0 = 0
        self.gravity = -.5
        self.stairsAvailable = False
        self.lastPlayerValidZ = 0
        self.hammerTime = False
        
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
    
    def hammerFrame1(self):
        self.hammerDown.show()
        self.hammerUp.hide()
        
    def hammerFrame2(self):
        self.hammerDown.hide()
        self.hammerUp.show()
    
    def setup(self, task):
        lens = OrthographicLens()
        lens.setFilmSize(25,20)
        base.camNode.setLens(lens)
        
        self.player = self.scene.attachNewNode("Player")


        # init mario gfx stuff
        self.marioGfx = self.scene.find('root/mario')
        self.marioGfx.reparentTo(self.player)
        self.marioGfx.setTwoSided(True)
        self.hammerDown = self.scene.find('root/hammerdowm')
        self.hammerDown.reparentTo(self.marioGfx)
        self.hammerDown.setPos(1,0,0)
        self.hammerUp = self.scene.find('root/hammerup')
        self.hammerUp.reparentTo(self.marioGfx)
        self.hammerUp.setPos(0,0,1)
        self.hammerDown.hide()
        self.hammerUp.hide()
        
        frame1 = Func(self.hammerFrame1)
        frame2 = Func(self.hammerFrame2)
        delay = Wait(0.1)
        self.hammerSequence = Sequence(frame1,delay, frame2, delay)
        #sequence.loop()
        #sequence.start()
        #sequence.finish()

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
        
        ray = CollisionSegment(0,0,0,0,0,-.6)
        cNodePath = self.player.attachNewNode( CollisionNode('marioRay') )
        cNodePath.node().addSolid(ray)
        cNodePath.node().setIntoCollideMask(0x3)
        cNodePath.node().setFromCollideMask(0x3)
        cNodePath.show()
        base.cTrav.addCollider(cNodePath, self.collisionHandlerEvent)
        self.player.setPos(7,0,5)
        
        self.donkeykong  = None
        self.floor1 = self.createSquareCollider(-1.8,-5.5, 9.3,.5,'floor0','floor1Hitbox', 'Floor1', self.enableJump, self.disableJump, self.blockTexture, 0x01)
        self.floor2 = self.createSquareCollider(2.08 ,-2.5, 8.0 ,.5,'floor1','floor2Hitbox', 'Floor2', self.enableJump, self.disableJump, self.blockTexture, 0x01)
        self.floor3_1 = self.createSquareCollider(3.6 , 0.5 ,3.8,.5,'floor2','floor3_1Hitbox', 'Floor3_1', self.enableJump, self.disableJump, self.blockTexture, 0x01)
        self.floor3_2 = self.createSquareCollider(-6.3 ,0.5 ,5  ,.5,'pCube4','floor3_2Hitbox', 'Floor3_2', self.enableJump, self.disableJump, self.blockTexture, 0x01)
        self.floor4 = self.createSquareCollider(1.8,3.5,8,.5,'floors','floor4Hitbox', 'Floor4', self.enableJump, self.disableJump, self.blockTexture, 0x01)
        
        self.hammer = self.createSquareCollider(6,1.5,.5,.5,'hammer','hammerHitbox', 'hammer', self.enableHammer, self.disableHammer, self.arcadeTexture, 0x02)
        
        self.topstair = self.createSquareCollider(-6.8 ,3.5,0.5,2.5,'topstair','topstairHitbox', 'TopStair' , self.enableStairs, self.disableStairs, self.stairsTexture, 0x02)
        self.middlestair = self.createSquareCollider(-0.86, 0.1,0.5,2.5,'middlestair','middlestairHitbox', 'MiddleStair' , self.enableStairs, self.disableStairs, self.stairsTexture, 0x02)
        self.bottomstair = self.createSquareCollider(-6.8 ,-2.5,0.5,2.5,'bottomstair','bottomstairHitbox', 'BottomStair' , self.enableStairs, self.disableStairs, self.stairsTexture, 0x02)
        
        self.leftWall = self.invisibleSquareCollider( -12.5, 0, 1, 10, "leftWallHitbox", "leftWall", 0x1 )
        self.rightWall = self.invisibleSquareCollider( 11.3, 0, 1, 20, "rightWallHitbox", "rightWall", 0x1 )
        
        self.barrelDestroyer = self.invisibleSquareCollider( -0.5, -10, 10.5, 1, "barrelDestroyHitBox", "barrelDestroyer", 0x1 )
        
        base.enableParticles()
        self.physicsCollisionPusher = PhysicsCollisionHandler()
        gravity = ForceNode("world-forces")
        gravityP = render.attachNewNode(gravity)
        gravityForce = LinearVectorForce(0,0,-9.81)
        gravity.addForce(gravityForce)
        base.physicsMgr.addLinearForce(gravityForce)
        self.accept("into-barrelCollider", self.barrelCrash)
        
        self.accept("raw-a", self.throwBarrel)
        
        base.cTrav.showCollisions(self.render)
        return Task.done
    
    def enableHammer(self, evt):
        self.hammerTime = True
        self.hammerSequence.loop()
        self.scene.node().removeChild( evt.getIntoNodePath().node().getParent(0) )
        
    def disableHammer(self, evt):
        pass
        
    def barrelCrash(self, evt):
        physicsBarrel = evt.getIntoNodePath().node().getParent(0).getParent(0)
        other = evt.getFromNodePath().node().getParent(0)
        
        if( other.name == "leftWall" or other.name == "rightWall"):
            forceNode = physicsBarrel.getChildren()[1]
            force = forceNode.getForce(0)
            force.setVector( force.getLocalVector().x*-1,0,0 )
            forceNode.clear()
            forceNode.addForce(force)
            
        if other.name == "barrelDestroyer":
            self.scene.node().removeChild( physicsBarrel.getParent(0) )
        
        if other.name == "Player" :
            if( self.hammerTime):
                self.scene.node().removeChild( physicsBarrel.getParent(0) )
        
    def throwBarrel(self):
        barrelNode = self.scene.attachNewNode("PhysicalBarrel")
        physicsBarrel = ActorNode("physics_barrel")
        physicsBarrel.getPhysicsObject().setMass(0.01)
        
        barrel = barrelNode.attachNewNode(physicsBarrel)
        base.physicsMgr.attachPhysicalNode(physicsBarrel)
        
        visualBarrel = barrel.attachNewNode("BarrelCopy")
        originalBarrel = self.scene.find("root/barrel")
        originalBarrel.instanceTo(visualBarrel)
        
        sphere = CollisionSphere(0,0,0,0.5)
        cNodePath = visualBarrel.attachNewNode( CollisionNode("barrelCollider") )
        cNodePath.node().addSolid(sphere)
        cNodePath.node().setFromCollideMask(0x01)
        cNodePath.node().setIntoCollideMask(0x01)
        #cNodePath.show()
        
        self.physicsCollisionPusher.addCollider(cNodePath, barrel)
        base.cTrav.addCollider(cNodePath, self.physicsCollisionPusher )
        
        barrelForceNode = ForceNode("barrelForce")
        barrel.attachNewNode(barrelForceNode)
        barrelForce = LinearVectorForce(-8,0,0,1,False)
        barrelForceNode.addForce(barrelForce)
        physicsBarrel.getPhysical(0).addLinearForce(barrelForce)
        
        
        barrelNode.setPos(self.scene, -3, 0, 7)
    
    def createSquareCollider(self,px,pz, w,h, modelName, collisionNodeName, nodeName, enableFunction, disableFunction, texture, mask ):
        obj = self.scene.attachNewNode(nodeName)
        hitbox = CollisionBox( Point3(0,0,0) , w, 5, h)
        cNodePath = obj.attachNewNode( CollisionNode(collisionNodeName) )
        cNodePath.node().addSolid(hitbox)
        cNodePath.node().setIntoCollideMask(mask)
        cNodePath.node().setFromCollideMask(mask)
        #cNodePath.show()
        base.cTrav.addCollider(cNodePath, self.collisionHandlerEvent)
        
        self.scene.find(f'root/{modelName}').reparentTo(obj)
        obj.setPos(px,0,pz)
        obj.setTexture(texture)
        
        self.accept(f'into-{collisionNodeName}' , enableFunction)
        self.accept(f'outof-{collisionNodeName}' , disableFunction)
        return obj
    
    
    def invisibleSquareCollider(self, px, pz, w, h, collisionNodeName, nodeName, mask ):
        obj = self.scene.attachNewNode(nodeName)
        hitbox = CollisionBox( Point3(0,0,0), w,5,h )
        cNodePath = obj.attachNewNode( CollisionNode(collisionNodeName) )
        cNodePath.node().addSolid(hitbox)
        cNodePath.node().setIntoCollideMask(mask)
        cNodePath.node().setFromCollideMask(mask)
        cNodePath.show()
        base.cTrav.addCollider(cNodePath, self.collisionHandlerEvent)
        obj.setPos(px,0,pz)
    
    def enableJump(self, evt):
        print( evt.getIntoNodePath().node().getParent(0).getTransform().getPos() )
        self.lastPlayerValidZ = evt.getIntoNodePath().node().getParent(0).getTransform().getPos().z +1
        self.jumpAvailable = True
        print("enable jump")

    def disableJump(self, evt):
        print( evt.getIntoNodePath().node().getParent(0) )
        self.jumpAvailable = False
        print("disable jump")
    
    def enableStairs(self, evt):
        self.stairsAvailable = True
        print("enable stairs")

    def disableStairs(self, evt):
        self.stairsAvailable = False
        print("disable stairs")
        
        
    def applyMove(self):
        mv = Vec3(0,0,0)
        p = self.player.getPos()
        
        if(self.input["left"]):
            self.marioGfx.setSx(self.player  , 1)
            mv.x = 0.1
        if(self.input["right"]):
            self.marioGfx.setSx(self.player  , -1)
            mv.x = -0.1
        
        if( self.jumpAvailable ):
            mv.z = self.v0 + self.baseTime*self.gravity
            if( not self.stairsAvailable ):
                p.z = self.lastPlayerValidZ
            if( mv.z < 0):
                self.v0 = 0
                self.baseTime = 0
                mv.z = 0
                        
        if( self.input["space"] and self.jumpAvailable):
            self.baseTime = 0
            self.v0 = .2
            mv.z = self.v0 + self.baseTime*self.gravity
        
        if( not self.jumpAvailable and not self.stairsAvailable ):
            self.baseTime = self.baseTime + globalClock.getDt()
            mv.z = self.v0 + self.baseTime*self.gravity
        
        if( self.stairsAvailable):
            self.baseTime = 0
            self.v0 = 0
            if( self.input["up"]):
                mv.z = mv.z + 0.1
            if( self.input["down"] and not self.jumpAvailable) :
                mv.z = mv.z - 0.1
        p.x = p.x + mv.x
        p.z = p.z + mv.z
        self.player.setPos(p)

    def update(self, task):
        self.camera.setPos(0,35,0)
        self.camera.lookAt(self.scene)
        
        self.applyMove()
        
        return Task.cont
        
dk = DonkeyKong()
dk.run()