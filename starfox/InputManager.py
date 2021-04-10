class InputManager:
    
    arrowUp = 'arrow_up'
    arrowDown = 'arrow_down'
    arrowLeft = 'arrow_left'
    arrowRight = 'arrow_right'
    space = 'space'
    keyA = 'a'
    keyS = 's'
    keyD = 'd'
    keyW = 'w'
    keyV = 'v'
    keyX = 'x'
    
    instance = None
    
    @staticmethod
    def initWith(app, list):
        InputManager.instance = InputManager()
        
        for i in list:
            InputManager.instance.setInput(i,False)
            app.accept(f'raw-{i}' , InputManager.createInputFunction(i,InputManager.instance,True) )
            app.accept(f'raw-{i}-up' , InputManager.createInputFunction(i,InputManager.instance,False) )
            
    @staticmethod
    def createInputFunction(evt, inputManagerInstance, down=True ):
        def receiveInput():
            inputManagerInstance.setInput(evt, down)
        return receiveInput
    
    @staticmethod
    def get_input(inp):
        return InputManager.instance.getInput(inp)
    
    @staticmethod
    def debug():
        return f'{InputManager.instance}'
    
    
    def __init__(self):
        self.input = {}

    def getInput(self, input):
        return self.input[input]
    
    def setInput(self, key, state):
        self.input[key] = state
    
    def __str__(self):
        res = ""
        for i in self.input.items():
            res = res + '\n' + (f'{i[0]}:{i[1]}')
        return res