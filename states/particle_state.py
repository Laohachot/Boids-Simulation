'''
State that is the particle simulation
This state uses button instances from the boids
simulator (exit an help button).
'''

import pygame 
import numpy as np

from objects import particle
from instances import boids_instances as boids_i

from states import state
from main import CONFIG
from itertools import product

class particles(state.state):
    '''State for particle simulation'''
    def __init__(self, MANAGER, WINDOW, POOL, QUEUE):
        super().__init__(MANAGER, WINDOW)
        fps = CONFIG.getint('window','fps')
        particles_list = []

        self.__dict__.update(locals())

    def update_graphics(self):
        '''
        Blits and flips
        '''

        self.WINDOW.fill((0,0,0))
        for instance in self.particles_list:
            instance.draw(self.WINDOW) 

        for button in boids_i.state_buttons:
            button.draw(self.WINDOW)

        boids_i.counter.draw(self.WINDOW)
        boids_i.reset.draw(self.WINDOW)

        pygame.display.update()


    def animations(self):
        '''
        Method that handles animations, which are
        changes in graphics that does not affect the game
        '''
        boids_i.counter.text_r = f'Particles: {len(self.particles_list)}'


    def interact_user(self):
        '''
        Method for user interactions
        '''
        for button in boids_i.state_buttons:
            button.interact_mouse(self.mouse_pos, self.click)
            # button.state is whether the button has been clicked 
            # or not
            if(button.state):
                self.next_state = self.MANAGER.get_state(button.next_state)
                self._active = False


        if(self.mouse[0]):
            self.particles_list.append(
                particle.particle(self.mouse_pos)
            )
        
        boids_i.reset.interact_mouse(self.mouse_pos, self.click)
        if(boids_i.reset.state):
            self.reload()
    

    def logic(self):
        '''
        Method for handling logic:
        particle physics in this case. 
        '''
        pos_matrix = np.array([obj.pos for obj in self.particles_list])

        '''Maps task and sets for arguments across multiple processes'''
        self.POOL.starmap(particle.particle.apply_all, product(
                self.particles_list, [pos_matrix], [self.mouse[2]], [self.mouse_pos], [self.QUEUE]
            )
        )
        
        '''
        Results are stored in the self.QUEUE by the processes.
        They are retrieved to the main program by popping the queue 
        til empty. 
        '''
        self.particles_list = []
        while not self.QUEUE.empty():
            self.particles_list.append(self.QUEUE.get())


    def run(self):
        '''
        The "main" loop 
        '''
        while(self._active):
            self.clock.tick(self.fps)
            self.update_user_input()
            self.interact_user()
            self.logic()
            self.update_graphics()
            self.animations()
        return self.next_state
    

    def reload(self):
        '''
        Soft reload by removing reference 
        from old list of particle instances
        '''
        self.particles_list = []