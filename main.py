'''
The main python file. Execute this file to 
run program.
'''

import configparser
import pygame
import numpy as np 
from importlib import reload
from json import loads


CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')


from states import menu_state
from states import boids_state
from states import info_state
from states import manager
from states import particle_state


class main_class:
    def __init__(self, multiprocess=False):
        if(multiprocess):
            from multiprocessing import Pool, Manager
            POOL = Pool() 
            MP_MANAGER = Manager()
            QUEUE = MP_MANAGER.Queue() 

        pygame.init()

        if(CONFIG.getboolean('window','fullscreen')):
            WINDOW = pygame.display.set_mode(loads(CONFIG.get('window','shape')), pygame.FULLSCREEN)
        else:
            WINDOW = pygame.display.set_mode(loads(CONFIG.get('window','shape')))

        pygame.display.set_caption("Simulation")
 
        '''
        The manager class is essentially a container for class instances (with additional
        functionality, see the class definition in objects/manager.py). The manager 
        abstracts away most of the code for switching between class instances during 
        runtime. 

        In this case, the manager is utilized as a server for "states". States are the
        class instances, where the classes can be interpreted as standalone programs.  
        '''
        manager0 = manager.manager(state_kwargs={'WINDOW':WINDOW})
        
        # Add states to manager
        manager0.update(
            new_states = {
                'menu':menu_state.menu(manager0, WINDOW),
                'info':info_state.info(manager0, WINDOW),
                'boids':boids_state.boids(manager0, WINDOW),
                'particles':particle_state.particles(manager0, WINDOW, POOL, QUEUE) #Experimental parallel processing because why not
            }
        )
    
        # Initial state
        current_state = manager0.get_state('menu')
        
        # Turn local variables to instance attributes
        self.__dict__.update(locals())


    def run(self):
        while(True):
            self.current_state.activate()
            # The current state should return the next state when its deactivated
            self.current_state = self.current_state.run()

            # If exit state is returned (a None type)
            if(not self.current_state):
                break

        # Close and join parallel processes 
        if(self.multiprocess):
            self.POOL.close()
            self.POOL.join()


if __name__ == '__main__':
    simulator = main_class(multiprocess=True)
    simulator.run()




