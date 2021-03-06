from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import loadPrcFileData
from math import sin, cos, pi
loadPrcFileData('', 'win-size 640 480')
#loadPrcFileData('', 'want-directtools #t')
#loadPrcFileData('', 'want-tk #t')


class Test(ShowBase):
    def __init__(self):
        super().__init__(self)
        self.py = 200
        self.angle = 0
        self.taskMgr.add(self.setup , "setup")
        self.taskMgr.add(self.update, "update")

    def createFace(self,x,y,z,rx,ry,rz, img):
        square = self.loader.loadModel("models/Square")
        square.setPos(x,y,z)
        square.setHpr(rz,rx,ry)
        text = self.loader.loadTexture(img)
        square.setTexture(text)
        square.reparentTo(self.render)
        square.setScale(20,20,20)

    def setup(self, task):
        print("setup")
        d = 32.5
        self.createFace(0,d,0,0,0,0,"models/skybox_pz.jpg")
        self.createFace(d,0,0,0,0,-90,"models/skybox_nx.jpg")
        self.createFace(0,-d,0,0,0,180,"models/skybox_nz.jpg")
        self.createFace(-d,0,0,0,0,90,"models/skybox_px.jpg")

        self.createFace(0,0,d,90,0,0,"models/skybox_py.jpg")
        self.createFace(0,0,-d,-90,0,0,"models/skybox_ny.jpg")



        return Task.done
    def angleToRad(self, angle):
        return angle*pi/180.0

    def update(self, task):
        print("update")
        d = 10
        self.camera.setPos(0,0,0)
        #self.camera.setPos(d*sin(  self.angleToRad(self.angle) ) ,  d*cos(  self.angleToRad(self.angle) )   ,0)
        self.angle = self.angle + 0.5
        self.camera.lookAt(d*sin(  self.angleToRad(self.angle) ),d*cos(  self.angleToRad(self.angle) ),0)
        #self.camera.setHpr()
        return Task.cont

test = Test()
test.run()
