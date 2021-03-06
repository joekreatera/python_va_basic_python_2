from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Point3
from panda3d.core import Vec4


class App1(ShowBase):
    def __init__(self):
        super().__init__(self)

        posDif = 1.63
        self.addSquare(-posDif,0,0,0,-90,0,"models/skybox_px.jpg")
        self.addSquare(0,posDif,0,0,180,0,"models/skybox_nz.jpg")
        self.addSquare(posDif,0,0,0,90,0,"models/skybox_nx.jpg")
        self.addSquare(0,-posDif,0,0,0,0,"models/skybox_pz.jpg")
        self.addSquare(0,0,-posDif,90,0,0,"models/skybox_ny.jpg")
        self.addSquare(0,0,posDif,-90,0,0,"models/skybox_py.jpg")

        self.taskMgr.add(self.setup , "setup")
        print("Initialized")

    def setup(self,task):
        self.camera.setPos(0,-30,0)
        self.camera.lookAt(0,1,0)
        return Task.done

    def addSquare(self,x,y,z,rx,ry,rz,img):
        square = self.loader.loadModel("models/Square")
        square.reparentTo(self.render)
        square.setPos(x,y,z)
        square.setHpr(ry,rx,rz)
        text1 = self.loader.loadTexture(img)
        square.setTexture(text1)

app = App1()
app.run()
