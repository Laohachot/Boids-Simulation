from objects import general_fish
from main import CONFIG
import numpy as np 
import pygame

class shark(general_fish.fish):
    eat_radius = CONFIG.getint('shark','eat_radius')
    obstacle_radius = CONFIG.getint('shark','obstacle_radius')
    hunt_radius = CONFIG.getint('shark','hunt_radius')

    f_hunt = CONFIG.getfloat('shark','f_hunt')
    f_repel_obstacle = CONFIG.getfloat('shark','f_repel_obstacle')
    f_repel_border = CONFIG.getfloat('shark','f_repel_border')

    def __init__(self, pos, img):
        super().__init__(pos, img)
        

    def draw(self, WINDOW):    
        if(self.vel[0] > 0):
            new_image = pygame.transform.flip(self.img, 0, 1)
            new_image = pygame.transform.rotate(new_image, np.degrees(np.arctan2(*self.vel))+90)
        else: 
            new_image = pygame.transform.rotate(self.img, np.degrees(np.arctan2(*self.vel))+90)

        img_center = new_image.get_rect(center=self.pos)
        WINDOW.blit(new_image, img_center)


    def percieve_obstacles(self, dist_vecs, dist_vecs_norm):
        obstacle_mask = (dist_vecs_norm < self.obstacle_radius) & (dist_vecs_norm != 0)

        # dirs for directions (directions represented as normalized vectors)
        self.obstacles_dirs = dist_vecs[obstacle_mask] / dist_vecs_norm[obstacle_mask].reshape((-1,1)) 


    def percieve_preys(self, dist_vecs, dist_vecs_norm):
        self.eat_mask = (dist_vecs_norm < self.eat_radius) & (dist_vecs_norm != 0)
        far_mask = (dist_vecs_norm < self.hunt_radius) & (dist_vecs_norm != 0)
        self.prey_dirs = dist_vecs[far_mask] / dist_vecs_norm[far_mask].reshape((-1,1))

        
    def eat(self, preys):
        if(any(self.eat_mask)):
            # Flipped eat mask array to perserve 
            # order in preys matrix
            for i in np.nonzero(self.eat_mask)[0][::-1]:
                if(i < len(preys)):
                    del(preys[i])


    def hunt(self):
        if(self.prey_dirs.shape[0]):
            self.recalc_vel.append(
                self.f_hunt*self.prey_dirs.mean(axis=0)
            )
        else:
            self.vel = self.vel*0.9
    

    def avoid_obstacles(self):
        if(self.obstacles_dirs.shape[0]):
            self.recalc_vel.append(
                self.f_repel_obstacle*self.obstacles_dirs.mean(axis=0)
            )


    def stay_in_border(self, w_shape):
        if(self.pos[0] > w_shape[0]*0.90):
            self.recalc_vel.append(np.array([-self.f_repel_border,0]))
        if(self.pos[0] < w_shape[0]*0.10):
            self.recalc_vel.append(np.array([self.f_repel_border,0]))

        if(self.pos[1] > w_shape[1]*0.90):
            self.recalc_vel.append(np.array([0,-self.f_repel_border]))
        if(self.pos[1] < w_shape[1]*0.10):
            self.recalc_vel.append(np.array([0,self.f_repel_border]))


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
        self.randval = state.randvals[i]

        offset_i = i+state.obstacle_index

        self.percieve_obstacles(
            dist_vecs = state.dist_matrix[offset_i] [state.num_preys:state.obstacle_index],
            dist_vecs_norm = state.dist_matrix_norms[offset_i] [state.num_preys:state.obstacle_index]
        )

        self.percieve_preys(
            dist_vecs = state.dist_matrix[offset_i] [:state.num_preys],
            dist_vecs_norm = state.dist_matrix_norms[offset_i] [:state.num_preys]
        )
        self.hunt()
        self.eat(state.preys)
        self.avoid_obstacles()
        self.stay_in_border(state.w_shape)
        self.motion()
        
        
