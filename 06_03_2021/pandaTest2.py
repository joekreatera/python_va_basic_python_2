from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Point3
from panda3d.core import Vec4
from panda3d.core import loadPrcFileData

loadPrcFileData('', 'win-size 640 480')
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

class Test(ShowBase):
    def __init__(self):
        super().__init__(self)
        base.messenger.toggleVerbose()
        self.taskMgr.add(self.setup, "setup")
        self.taskMgr.add(self.setup, "update")

    def setup(self,task):

        square = self.loader.loadModel("models/Square")
        square.setPos(0,10,0)
        square.setHpr(180,0,0)
        text1 = self.loader.loadTexture("models/logo_VGA.png")
        square.setTexture(text1)

        square.reparentTo(self.render)

        return Task.done

    def update(self,task):
        self.camera.setPos(0,200,0)
        self.camera.lookAt(0,0,0)
        return Task.cont


test = Test()
test.run()
