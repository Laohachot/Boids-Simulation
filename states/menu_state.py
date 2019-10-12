'''
State that is the menu screen
'''

import pygame
from states import state
from main import CONFIG
from instances import menu_instances as menu_i
from json import loads
from objects import tuna


class menu(state.state):
    '''State for menu'''
    def __init__(self, MANAGER, WINDOW):
        super().__init__(MANAGER, WINDOW)
        w_shape = loads(CONFIG.get('window','shape'))
        self.fps = CONFIG.getint('window','fps')

        # bg for background
        self.menu_bg = pygame.image.load(CONFIG.get('window', 'background_fp')).convert_alpha()
        self.menu_bg = pygame.transform.scale(self.menu_bg, w_shape)


    def update_graphics(self):
        '''
        Blits and flips
        '''
        self.WINDOW.blit(
            self.menu_bg,
            (0,0)
        )

        for instance in menu_i.all_list:
            instance.draw(self.WINDOW)
        
        pygame.display.update()
        

    def interact_user(self):
        for instance in menu_i.all_list:
            instance.interact_mouse(self.mouse_pos, self.click)
        
    
    def logic(self):        
        for button in menu_i.button_changestate_list:
            if(button.state):
                self.next_state = self.MANAGER.get_state(button.next_state)
                self._active = False
                try:
                    # Will raise error for MANAGER.get_state('exit'), since it will try
                    # to reload a None type 
                    self.MANAGER.reload_state(button.next_state)
                except Exception:
                    continue

    def run(self):
        while(self._active):
            self.clock.tick(self.fps)
            self.update_user_input()
            self.interact_user()
            self.logic()
            self.update_graphics()

        return self.next_state
