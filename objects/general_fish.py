import pygame 
import numpy as np 
from objects import general_objects

class fish(general_objects.game_object):
    '''
    Template class for fish classes.
    '''
    def __init__(self, pos, img):
        super().__init__(pos, img)
        self.vel = np.random.randn(2)*10
        
        # recalc_vel is used to temporary store 
        # "forces" from the rules. recalc_vel
        # will then be summed up and summed with 
        # the old velocity 
        self.recalc_vel = []


    def draw_radius(self, WINDOW, radius=5, border_width=3):
        '''
        Draws a circular border around instance.
        Used for debugging purposes. 
        '''
        pygame.draw.circle(
            WINDOW,
            (255,255,255),
            self.pos.astype('int'),
            radius,
            border_width
        )


    def draw_circle(self, WINDOW):
        '''
        Draws a circle at instance position.
        Used for debugging purpoeses.
        '''
        pygame.draw.circle(
            WINDOW,
            (255,255,255),
            self.pos.astype('int'),
            5
        )


    def motion(self):
        '''
        Calculates motion. Used after
        calculating the rules.
        '''
        self.vel = self.vel + sum(self.recalc_vel)
        self.speed = np.linalg.norm(self.vel) 

        if(self.speed < 4):
            self.vel = self.vel*2

        # Add some randomness to movement
        sin = np.sin(self.randval)
        cos = np.cos(self.randval)
        self.vel = [[cos,-sin],[sin,cos]]@self.vel

        self.pos = self.pos + self.vel

        # Very important to empty recalc_vel list before
        # calculating the rules.
        self.recalc_vel = []


    def stay_in_border(self, w_shape):
        '''
        Makes entities want to stay within all window borders
        '''
        if(self.pos[0] > w_shape[0]*0.90):
            self.recalc_vel.append([-1,0])
        if(self.pos[0] < w_shape[0]*0.10):
            self.recalc_vel.append([1,0])

        if(self.pos[1] > w_shape[1]*0.90):
            self.recalc_vel.append([0,-1])
        if(self.pos[1] < w_shape[1]*0.10):
            self.recalc_vel.append([0,1])
    

    def wrap_screen(self, w_shape):
        '''
        Makes entities able to "wrap the screen"
        '''
        self.pos[0] = self.pos[0] % w_shape[0]
        self.pos[1] = self.pos[1] % w_shape[1]


    def wrap_x(self, w_shape):
        '''
        Makes entities only wrap the screen in the 
        horizontal direction
        '''
        self.pos[0] = self.pos[0] % w_shape[0]


    def avoid_y_borders(self, w_shape):
        '''
        Makes entities want to stay within the 
        top and bottom screen borders
        '''
        if(self.pos[1] > w_shape[1]*0.99):
            self.recalc_vel.append(np.array([0,-10]))
        if(self.pos[1] < w_shape[1]*0.05):
            self.recalc_vel.append(np.array([0,10]))


if __name__ == '__main__':
    pass