import abc
import pygame 
import numpy as np 

class game_object(abc.ABC):
    '''
    Template object for simulation classes.
    '''
    def __init__(self, pos, img):
        self.pos = np.array(pos)
        self.img = img

    @abc.abstractmethod
    def draw(self):
        print("Missing draw method")

    
    def draw_circle(self, WINDOW):
        pygame.draw.circle(
            WINDOW,
            (255,255,255),
            self.pos,
            5
        )

