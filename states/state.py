'''
Contains general state class (called "state")
'''
import pygame 

class state:    
    '''
    General state class that contains methods and attributes that
    all states share. 
    '''
    def __init__(self, MANAGER, WINDOW):
        self.MANAGER = MANAGER
        self.WINDOW = WINDOW
        self._active = False
        self.next_state = False
        self.clock = pygame.time.Clock()

    
    def activate(self):
        '''Activates the state'''
        self._active = True


    def update_user_input(self):
        '''
        Method to update pygame events and user inputs to the states. 

        User input information is stored as attributes for easy
        reuse of the information throughout the whole class 
        '''
        self.click = False
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                self.next_state = self.MANAGER.get_state('exit')
                self._active = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True

            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_BACKSPACE):
                    self.next_state = self.MANAGER.get_state('previous')
                    self._active = False

                if(event.key == pygame.K_F4):
                    self.next_state = self.MANAGER.get_state('exit')
                    self._active = False
    
        self.kbinput = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse = pygame.mouse.get_pressed()


    def reload(self):
        print("Reload needs to be explicitly implemented in child class")