import pygame 
import numpy as np 
from objects import general_fish
from main import CONFIG

class tuna(general_fish.fish):
    repel_radius = CONFIG.getint('tuna','repel_radius')
    attract_radius = CONFIG.getint('tuna','attract_radius')
    obstacle_radius = CONFIG.getint('tuna','obstacle_radius')
    foe_radius = CONFIG.getint('tuna','foe_radius')

    f_attract_friends = CONFIG.getfloat('tuna','f_attract_friends')

    f_repel_friends = CONFIG.getfloat('tuna','f_repel_friends')
    f_repel_obstacles = CONFIG.getfloat('tuna','f_repel_obstacles')
    f_repel_foes = CONFIG.getfloat('tuna','f_repel_foes')
    

    def __init__(self, pos, img):
        super().__init__(pos, img)


    def draw(self, WINDOW):
        '''
        Calculates orientation and blits instance to 
        WINDOW.
        '''

        # The in
        if(self.vel[0] < 0):
            blit_image = pygame.transform.flip(self.img, 0, 1)
            blit_image = pygame.transform.rotate(blit_image, np.degrees(np.arctan2(*self.vel))-90)
        else:
            blit_image = pygame.transform.rotate(self.img, np.degrees(np.arctan2(*self.vel))-90)            
        # Get a new rect with the center of the old rect.
        img_center = blit_image.get_rect(center=self.pos)
        WINDOW.blit(blit_image, img_center)

    def percieve_friends(self, dist_vecs, dist_vecs_norm, vel_vecs):
        '''
        Slices dist_vecs and dist_vecs_norms with respect to all tunas
        to get directions to all tunas
        '''
        close_mask = (dist_vecs_norm < self.repel_radius) & (dist_vecs_norm != 0)
        medium_mask =  (dist_vecs_norm < self.attract_radius) & (dist_vecs_norm != 0)

        '''
        dirs for directions (directions represented as unit vectors)
        '''
        self.friends_close_dirs = dist_vecs[close_mask] / dist_vecs_norm[close_mask].reshape((-1,1))
        self.friends_medium_dirs = dist_vecs[medium_mask] / dist_vecs_norm[medium_mask].reshape((-1,1))

        self.friends_vels = vel_vecs[medium_mask] 


    def percieve_obstacles(self, dist_vecs, dist_vecs_norm):
        '''
        Slices dist_vecs and dist_vecs_norms with respect to obstacles
        to get directions to all obstacles
        '''
        medium_mask = (dist_vecs_norm < self.obstacle_radius) & (dist_vecs_norm != 0)
        self.obstacles_dirs = dist_vecs[medium_mask] / dist_vecs_norm[medium_mask].reshape((-1,1))  


    def percieve_foes(self, dist_vecs, dist_vecs_norm):
        '''
        Slices dist_vecs and dist_vecs_norms with respect to foes
        to get directions to all foes (sharks)
        '''
        far_mask = (dist_vecs_norm < self.foe_radius) & (dist_vecs_norm != 0)
        self.foes_dirs = dist_vecs[far_mask] / dist_vecs_norm[far_mask].reshape((-1,1))


    def attraction(self):
        '''
        Cohesion rule
        '''
        if(self.friends_medium_dirs.shape[0]):
            self.recalc_vel.append(
                self.f_attract_friends*self.friends_medium_dirs.mean(axis=0)
            )


    def repulsion(self):
        '''
        Separation rule
        '''

        # Force norm from tunas within inner tuna radius 
        if(self.friends_close_dirs.shape[0]):
            self.recalc_vel.append(
                self.f_repel_friends*self.friends_close_dirs.mean(axis=0)
            )

        # Force norm from obstacle within obstacle radius
        if(self.obstacles_dirs.shape[0]):
            self.recalc_vel.append(
                self.f_repel_obstacles*self.obstacles_dirs.mean(axis=0)
            )
        
        # Force norm from sharks within foe radius
        if(self.foes_dirs.shape[0]):
            self.recalc_vel.append(
                self.f_repel_foes*self.foes_dirs.mean(axis=0)
            )


    def match_vel(self):
        '''
        Alignment rule
        '''
        if(self.friends_medium_dirs.shape[0] > 1):
            self.recalc_vel.append(
                self.friends_vels.mean(axis=0)*0.20+self.vel*0.80-self.vel
            )


    def apply_behavior(self, state, i):
        '''
        Applies all methods necessary to give a complete behavior
        
        The method takes in that boids_state object as an input. 
        The boids state object carries dist_matrix and dist_matrix_norms 
        as instance attributes. The percieve methods are then feeded with 
        the appropriate slices of the matrices. An iterator value is 
        also passed to this to slice.

        [:state.num_preys] slices info about preys
        [state.num_preys:state.obstacle_index] slices info about obstacles
        [state.obstacle_index:] slices info about predators
        '''
        self.percieve_friends(
            dist_vecs = state.dist_matrix[i] [:state.num_preys], 
            dist_vecs_norm = state.dist_matrix_norms[i] [:state.num_preys],
            vel_vecs = state.vel_vecs[:state.num_preys]
        )

        self.percieve_obstacles(
            dist_vecs = state.dist_matrix[i] [state.num_preys:state.obstacle_index], 
            dist_vecs_norm = state.dist_matrix_norms[i] [state.num_preys:state.obstacle_index]
        )

        self.percieve_foes(
            dist_vecs = state.dist_matrix[i] [state.obstacle_index:],
            dist_vecs_norm = state.dist_matrix_norms[i] [state.obstacle_index:]
        )

        self.attraction()
        self.repulsion()
        self.match_vel()
        self.wrap_x(state.w_shape)
        self.avoid_y_borders(state.w_shape)
        self.randval = state.randvals[i]
        self.motion()

if __name__ == '__main__':
    pass