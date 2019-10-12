import pygame 
import numpy as np 
from objects import general_objects

class uw_mine(general_objects.game_object):
    def __init__(self, pos, img, radius=10):
        pos = np.array(pos)
        self.vel = np.zeros(2)
        self.__dict__.update(locals()) 
    
    def draw(self, WINDOW):
        WINDOW.blit(
            self.img, self.img.get_rect(center=self.pos)
        )

