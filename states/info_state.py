import pygame 
from main import CONFIG
from states import state
from instances import info_instances as info_i
from json import loads

class info(state.state):
    def __init__(self, MANAGER, WINDOW):
        super().__init__(MANAGER, WINDOW)
        w_shape = loads(CONFIG.get('window','shape'))

        self.bg_img = pygame.image.load(CONFIG.get('window', 'background_fp')).convert_alpha()
        self.bg_img = pygame.transform.scale(self.bg_img, w_shape)

    
    def update_graphics(self):
        '''
        Blits and flips
        '''
        self.WINDOW.blit(self.bg_img, (0,0))

        for instance in info_i.text_list:
            instance.draw(self.WINDOW)
        
        info_i.back_button.draw(self.WINDOW)
         
        pygame.display.update()


    def interact_user(self):
        '''
        Method for user interactions
        '''
        info_i.back_button.interact_mouse(self.mouse_pos, self.click)
        if(info_i.back_button.state):
            self.next_state = self.MANAGER.get_state(info_i.back_button.next_state)
            self._active = False    
        

    def run(self):
        '''
        The "main" loop 
        '''
        while(self._active):
            self.clock.tick(30)
            self.update_user_input()
            self.interact_user()
            self.update_graphics()
        return self.next_state
    
    
    def reload(self):
        pass