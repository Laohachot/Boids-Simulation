import pygame 
import numpy as np 
from main import CONFIG
n_strong_f = CONFIG.getfloat('particles_state','nuclear_strong_force')
n_weak_f = CONFIG.getfloat('particles_state', 'nuclear_weak_force')
drag_f = CONFIG.getfloat('particles_state', 'drag_force')

'''
I wrote most of this code early on and didn't really comment. 
Now I dont really get it, so I wont bother commenting
'''

class particle:
    def __init__(self, pos):
        pos = np.array(pos)
        vel = np.zeros((2))
        acc = np.zeros((2))
        x0 = np.array([20,20])
        friends = []
        friends_dist_vecs = []
        self.__dict__.update(locals())
    

    def draw(self, WINDOW):
        pygame.draw.circle(
            WINDOW,
            (255,255,255),
            self.pos.astype('int'),
            5
        )
    

    def motion(self):
        self.vel = self.vel+self.acc-drag_f*self.vel
        self.pos = self.pos+self.vel


    def get_distances_mp(self, pos_matrix):
        self.distance_vecs = pos_matrix - self.pos 
        self.distances = np.linalg.norm(self.distance_vecs, axis=1) 


    def percieve_mp(self, pos_matrix):
        mask = self.distances > 0.01
        self.friends_dist_vecs = self.distance_vecs[mask]
        self.friends_dist = self.distances[mask]
        
        self.friends_dist[self.friends_dist < 1] = 1
        self.normalized_vecs = self.friends_dist_vecs.T/self.friends_dist
        self.normalized_vecs = self.normalized_vecs.T  

        
    def attraction(self):
        norms = n_weak_f/self.friends_dist
        self.acc = self.acc + np.sum((norms*self.friends_dist_vecs.T).T, axis=0)


    def repulsion(self):
        norms = -n_strong_f/self.friends_dist**2
        self.acc = self.acc + np.sum(
            (self.normalized_vecs.T*norms).T, 
            axis=0
        )


    def mouse_spring(self, mouse, mouse_pos):
        if(mouse):
            norms = 0.1*(mouse_pos - self.pos)
            self.acc = self.acc + norms


    def apply_all(self, pos_matrix, mouse, mouse_pos, queue):
        self.motion()
        self.get_distances_mp(pos_matrix)

        self.acc.fill(0)
        self.percieve_mp(pos_matrix)
        self.attraction()
        self.repulsion()
        self.mouse_spring(mouse, mouse_pos)
        queue.put(self)
    


if __name__ == '__main__':
    pass