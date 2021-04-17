from panda3d.core import Vec3

class Bullet:
    def __init__(self, original, world, origin , cTrav, collisionHandler , fwd, velMag, colMask ):
        self.gameObject = original.copyTo(world)
        self.gameObject.setPos(origin)
        self.velocity = fwd*velMag
        
        cTrav.addCollider( self.gameObject.find("**collision**") , collisionHandler)
        self.gameObject.setPythonTag("ObjectController" , self)
        self.gameObject.find("**collision**").node().setFromCollideMask(colMask)
        self.gameObject.find("**collision**").node().setIntoCollideMask(colMask)
        
        self.gameObject.setName("bulletC")
        self.activeTime = 0
        print("bullet created!")
    
    def update(self, world, dt , player):
        #self.gameObject.find("**visual**").lookAt(player)
        #print(f" {self.velocity} ")
        self.gameObject.setPos(world, self.gameObject.getPos(world) + self.velocity*dt )
        
    def crash(self, other):
        print("crash bullet")
        if( type(other) is not Bullet ):
            self.gameObject.removeNode()