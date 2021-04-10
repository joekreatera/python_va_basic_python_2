from InputManager import InputManager


class Player:
    def __init__(self, pandaNode):
        self.gameObject = pandaNode
        self.px = 0
        self.pz = 0
        self.gameObject.setColor( 1, 1 , 1 , 1)
    
    def update(self, world, dt):
        print( InputManager.get_input(InputManager.space) )
        
        up = (InputManager.get_input( InputManager.arrowUp ) )
        down = (InputManager.get_input( InputManager.arrowDown ) )
        left = (InputManager.get_input( InputManager.arrowLeft ) )
        right = (InputManager.get_input( InputManager.arrowRight ) )
    
        vel = 1
        if(up):
            self.pz = self.pz + vel
        
        if(down):
            self.pz = self.pz - vel
    
        if(right):
            self.px = self.px + vel
        
        if(left):
            self.px = self.px - vel
             
        self.gameObject.setZ( world, self.pz )
        self.gameObject.setX( world, self.px )