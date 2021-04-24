from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import DirectionalLight, AmbientLight, PointLight, Fog
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import loadPrcFileData
from panda3d.core import Vec3
from panda3d.core import AntialiasAttrib

#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

loadPrcFileData("", "framebuffer-multisample 1")
loadPrcFileData("", "multisamples 2")


class VisualTest(ShowBase):
    def __init__(self):
        super().__init__(self)
        self.var1 = 0
        self.scene = loader.loadModel("models/world")
        playerTexture = loader.loadTexture("models/starfoxShip.jpg")
        self.player = self.scene.find("player")
        self.player.setTexture(playerTexture)
        
        base.setBackgroundColor(0.1,0.1, 0.1, 1)
        enemyTexture = loader.loadTexture("models/enemyShip.jpg")
        self.enemy = self.scene.find("enemy1")
        self.enemy.setTexture(enemyTexture)
        
        self.basePlane = self.scene.find("basePlane")
        
        self.scene.reparentTo(self.render)
        self.player.setPos(50,50,3)
        self.enemy.setPos(50,55,0)
        
        
        self.ambient = AmbientLight("ambient")
        self.ambient.color = (0.1,0.1,0.1,1)
        self.ambientPath = self.render.attachNewNode(self.ambient)
        render.setLight(self.ambientPath)
        
        self.dirLight = DirectionalLight("dir light")
        self.dirLight.color = (1,1,1,1)
        self.dirLightPath = self.render.attachNewNode(self.dirLight)
        self.dirLightPath.setHpr(0,-90,0)
        self.dirLight.setShadowCaster(True,512,512)
        render.setLight(self.dirLightPath)
        
        self.pointLight = PointLight("point light")
        self.pointLight.color = (1,1,1,1)
        self.pointLightPath = self.render.attachNewNode(self.pointLight)
        self.pointLightPath.setPos(50,52.5,4)
        self.pointLight.attenuation = (.5,0,0)
        self.pointLight.setShadowCaster(True,1024,1024)
        self.render.setLight(self.pointLightPath)
        
        self.fog = Fog("fog")
        self.fog.setColor(0.1,0.1, 0.1)
        self.fog.setExpDensity(.3)
        self.fog.setLinearRange(150,300)
        self.fog.setLinearFallback(45,160,320)
        self.render.setFog(self.fog)
        
        self.render.setShaderAuto()
        self.render.setAntialias(AntialiasAttrib.MAuto)
        
        filters = CommonFilters(base.win, base.cam)
        filters.setBloom(size="large")
        filters.setAmbientOcclusion(strength=0.6,  falloff=0.0005 , radius=0.1 )
        filters.setCartoonInk(separation=2, color=(0,0,0,1) )
        self.taskMgr.add(self.update, "update")
        
    def update(self, evt):
        self.var1 = self.var1 + 0.1
        #self.dirLight.color = (self.var1,0,1,1)
        #self.dirLightPath.setHpr(self.var1,-self.var1,0)
        self.camera.setPos(60+self.var1,60+self.var1,20)
        #self.pointLightPath.setPos(30+self.var1 ,52.5,4)
        self.camera.lookAt(self.player)
    
        return Task.cont
        
app = VisualTest()
app.run()