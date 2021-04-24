from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import loadPrcFileData
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from InputManager import InputManager
from Player import Player
from Path import Path
from math import sin
from DynamicEnemy import *
from Bullet import  *
from direct.particles.ParticleEffect import ParticleEffect
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import DirectionalLight, AmbientLight, PointLight, Fog
from direct.showbase import Audio3DManager

from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TextNode

loadPrcFileData("" , "audio-library-name p3fmod_audio")
loadPrcFileData("", "fmod-use-surround-sound true")

class Starfox(ShowBase):
    def __init__(self):
        self.height= 500
        super().__init__(self)
        self.scene = self.loader.loadModel("./models/world.egg")
        playerTexture = loader.loadTexture("models/starfoxShip.jpg")
        enemyTexture = loader.loadTexture("models/enemyShip.jpg")
        bulletTexture = loader.loadTexture("models/shot.png")
        self.scene.reparentTo(self.render)
        
        base.setBackgroundColor(0.1,0.1, 0.1, 1)
        
        self.player = self.scene.find("player")
        self.player.setPythonTag("ObjectController" , Player(self.player) )
        self.player.setTexture(playerTexture)
        
        self.building_enemy = self.scene.find("building_enemy")
        self.dynamic_enemy = self.scene.find("enemy1")
        self.dynamic_enemy.setTexture(enemyTexture)
        self.bullet = self.scene.find("bullet")
        self.bullet.setTexture(bulletTexture)
        
        base.cTrav = CollisionTraverser()
        self.CollisionHandlerEvent = CollisionHandlerEvent()
        base.enableParticles()
        self.CollisionHandlerEvent.addInPattern('into-%in')
        self.CollisionHandlerEvent.addOutPattern('out-%in')
        
        
        self.accept('into-collision_player', self.crash)
        self.accept('into-collision_plane', self.crash)
        self.accept('into-collision_enemy', self.crash)
        
        base.cTrav.addCollider( self.scene.find("player/collision**"), self.CollisionHandlerEvent)
        base.cTrav.addCollider( self.scene.find("basePlane/collision**"), self.CollisionHandlerEvent)
        
        self.player.find("**collision**").node().setFromCollideMask(0x3)
        self.player.find("**collision**").node().setIntoCollideMask(0x3)

        self.dynamic_enemy.find("**collision**").node().setFromCollideMask(0x5)
        self.dynamic_enemy.find("**collision**").node().setIntoCollideMask(0x5)
        
        self.building_enemy.find("**collision**").node().setFromCollideMask(0x5)
        self.building_enemy.find("**collision**").node().setIntoCollideMask(0x5)
        
        
        
        #base.cTrav.showCollisions(self.render)
        
        
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
        
        self.createStaticEnemy(self.building_enemy, 0,50,0)
        self.createStaticEnemy(self.building_enemy, -50,50,0)
        self.createStaticEnemy(self.building_enemy, -100,50,0)
        self.createStaticEnemy(self.building_enemy, -70,130,0)
        self.createStaticEnemy(self.building_enemy, -120,80,0)
        self.createStaticEnemy(self.building_enemy, -220,130,0)
        
        DynamicEnemy(self.dynamic_enemy, self.scene, Vec3(-230,140,10) ,  base.cTrav, self.CollisionHandlerEvent , type = ENEMY_TYPE.CHASER )
        #DynamicEnemy(self.dynamic_enemy, self.scene, Vec3(-240,160,10) ,  base.cTrav, self.CollisionHandlerEvent) 
        #DynamicEnemy(self.dynamic_enemy, self.scene, Vec3(-250,200,10) ,  base.cTrav, self.CollisionHandlerEvent) 
        #DynamicEnemy(self.dynamic_enemy, self.scene, Vec3(-270,160,10) ,  base.cTrav, self.CollisionHandlerEvent) 
        #DynamicEnemy(self.dynamic_enemy, self.scene, Vec3(-250,200,10) ,  base.cTrav, self.CollisionHandlerEvent) 
        
        self.building_enemy.hide()
        self.dynamic_enemy.hide();
        
        self.fog = Fog("fog")
        self.fog.setColor(0.1,0.1, 0.1)
        self.fog.setExpDensity(.3)
        self.fog.setLinearRange(50,150)
        self.fog.setLinearFallback(45,160,320)
        self.render.setFog(self.fog)
        
        self.dirLight = DirectionalLight("dir light")
        self.dirLight.color = (0.7,0.7,1,1)
        self.dirLightPath = self.render.attachNewNode(self.dirLight)
        self.dirLightPath.setHpr(45,-45,0)
        self.dirLight.setShadowCaster(True,512,512)
        render.setLight(self.dirLightPath)
        
        filters = CommonFilters(base.win, base.cam)
        filters.setBloom(size="large", mintrigger=0.2)
        
        self.render.setShaderAuto()
        
        self.initSounds()
        self.initUI()
        self.onGame = False

    def initUI(self):
        self.font = loader.loadFont('./fonts/Magenta.ttf')
        
        self.lifes = [
            OnscreenImage(image='./UI/fox-icon-png-8.png', pos = (1.1, 0, 0.8), scale = 0.05),
            OnscreenImage(image='./UI/fox-icon-png-8.png', pos = (1.2, 0, 0.8), scale = 0.05)
        ]
        
        self.lifes[0].setTransparency(True)
        self.lifes[1].setTransparency(True)
        
        self.dialogScreen = DirectDialog(
            frameSize = (-0.7,0.7, -0.7, 0.7),
            relief = DGG.FLAT
        )
        
        s = OnscreenImage(image='./UI/fox-icon-png-8.png', pos = (0, 0, -0.2), scale = 0.20, parent = self.dialogScreen)
        s.setTransparency(True)
        
        self.titleUI = DirectLabel(
            text = "Starfox Region 4",
            parent = self.dialogScreen,
            scale = 0.1,
            pos= (0,0,.2),
            text_font = self.font
        )
        
        self.btn = DirectButton( text = "Start" , command = self.startGame , pos = (0,0,0) , parent = self.dialogScreen , scale=0.07)
        
    def startGame(self):
        self.dialogScreen.hide()
        self.flyingSound.play()
        self.onGame = True
        self.btn.hide()

    def initSounds(self):
        self.audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0] , self.camera)
        
        self.flyingSound = self.audio3d.loadSfx("./sounds/great fox flying.mp3")
        self.flyingSound.setLoop(True)
        
        
        self.audio3d.attachSoundToObject(self.flyingSound, self.player)
        self.audio3d.setSoundVelocityAuto(self.flyingSound)
        self.audio3d.setListenerVelocityAuto()
        #self.audio3d.setDistanceFactor(100)
        self.audio3d.setDropOffFactor(0)
        
        self.fireSound = self.audio3d.loadSfx("./sounds/arwing double laser one shot.mp3")
        self.crashSound = self.audio3d.loadSfx("./sounds/break.mp3")

    def createStaticEnemy(self, original, px, py, pz):
        be = original.copyTo(self.scene)
        be.setPos(px,py,pz)
        base.cTrav.addCollider( be.find("**collision**") , self.CollisionHandlerEvent )
        
        """
        self.pointLight = PointLight("point light")
        self.pointLight.color = (1,1,1,1)
        self.pointLightPath = self.render.attachNewNode(self.pointLight)
        self.pointLightPath.setPos(px,py,pz)
        self.pointLight.attenuation = (1,0,0)
        #self.pointLight.setShadowCaster(True,1024,1024)
        self.render.setLight(self.pointLightPath)
        """

    def crash(self, evt):
        
        self.crashSound.play()
        objectInto = evt.getIntoNodePath().node().getParent(0).getPythonTag("ObjectController")
        objectFrom = evt.getFromNodePath().node().getParent(0).getPythonTag("ObjectController")
        
        if( objectInto != None):
            objectInto.crash(objectFrom)

        if( objectFrom != None):
            objectFrom.crash(objectInto)
            
        lifes = self.player.getPythonTag("ObjectController").getLifes()
        if(lifes <= 0):
            self.onGame = False
            self.dialogScreen.show()
            self.flyingSound.stop()
            
    def update(self, evt):        
        #self.camera.setPos(0,-100,100)
        
        lifes = self.player.getPythonTag("ObjectController").getLifes()
        
        if( lifes > 2):
            self.lifes[0].show()
            self.lifes[1].show()
        elif( lifes > 1):
            self.lifes[0].show()
            self.lifes[1].hide()
        elif( lifes > 0):
            self.lifes[0].hide()
            self.lifes[1].hide()
             
        
        self.camera.lookAt(self.player)
        self.rails.setPos(self.scene,  Path.getXOfY(self.rails_y) , self.rails_y  , 12.4)
        self.rails.setHpr( Path.getHeading(self.rails_y) , 0, 0 )
        self.dirLight.color = ( self.rails_y/600  ,0.7,1,1)
        self.camera.setHpr( Path.getHeading(self.rails_y) , 0, 0 )
        
        if( self.onGame ):
            self.rails_y = self.rails_y + globalClock.getDt()*10
            #self.player.setPos(self.rails, 0, 0, sin(self.z/10.0)*40 )
            relX, relZ, isShooting = self.player.getPythonTag("ObjectController").update(self.rails, globalClock.getDt() )
            self.camera.setPos(self.rails, relX, -30, relZ)
            if( isShooting ):
                self.fireSound.play()
                b = Bullet(self.bullet, 
                    self.scene, 
                    self.player.getPos(self.scene), 
                    base.cTrav,
                    self.CollisionHandlerEvent, 
                    self.scene.getRelativeVector(self.player, Vec3(0,1,0) ) ,
                    40,
                    0x4
                    )    
            enemies = self.scene.findAllMatches("dynamicEnemy")
            for e in enemies:
                enemy = e.getPythonTag("ObjectController")
                enemy.update(self.scene, globalClock.getDt()  , self.player , self.bullet)
            
            bullets = self.scene.findAllMatches("bulletC")
            for b in bullets:
                bullet = b.getPythonTag("ObjectController")
                bullet.update(self.scene, globalClock.getDt() ,self.player )
                
        return Task.cont
        
sf = Starfox()
sf.run()


        
        # start debug section
"""
levelUp = (InputManager.get_input( InputManager.keyX ) )
levelDown = (InputManager.get_input( InputManager.keyV ) )

if( levelUp ):
    self.height = self.height + 10
if( levelDown ):
    self.height = self.height - 10
    

self.camera.setPos(self.rails.getX(), self.rails.getY() , self.height )
self.camera.lookAt(Vec3(self.rails.getX(), self.rails.getY(),0) )
"""
# end debug section