from InputManager import InputManager

class Player:
    def __init__(self, pandaNode):
        self.gameObject = pandaNode
        self.px = 0
        self.pz = 0
        self.shouldShoot = False
    
    def update(self, world, dt):
        #print( InputManager.get_input(InputManager.space) )
        
        up = (InputManager.get_input( InputManager.arrowUp ) )
        down = (InputManager.get_input( InputManager.arrowDown ) )
        left = (InputManager.get_input( InputManager.arrowLeft ) )
        right = (InputManager.get_input( InputManager.arrowRight ) )
        shoot = (InputManager.get_input(InputManager.space) )
    
        vel = 20*dt
        self.pz = self.pz+vel if up else self.pz
        self.pz = self.pz-vel if down else self.pz
        self.px = self.px+vel if right else self.px
        self.px = self.px+-vel if left else self.px

        limitZ = 12
        limitX = 24
        
        self.pz = min( max(self.pz, -limitZ) , limitZ)
        self.px =  min( max(self.px, -limitX) , limitX)

        self.gameObject.setZ( world, self.pz )
        self.gameObject.setX( world, self.px )
        
        lx = limitX*2.0/3
        lz = limitZ*2.0/3
        
        relx  = max(min(lx,self.px),-lx)
        relz = max(min(lz,self.pz),-lz)
    
        returnShoot = False;
        if( shoot ):
            self.shouldShoot = True
        if( not shoot and self.shouldShoot ):
            returnShoot = True
            self.shouldShoot = False
                    
        return relx,relz, returnShoot
    
    def crash(self, obj):
        self.gameObject.setColor( 1, 1 , 1 , 1)