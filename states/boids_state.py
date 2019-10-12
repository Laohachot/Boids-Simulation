import pygame 
import numpy as np
from importlib import reload

from objects import tuna
from objects import uw_mine
from objects import shark


from instances import boids_instances as boids_i

from states import state
from main import CONFIG
from json import loads

class boids(state.state):
    def __init__(self, MANAGER, WINDOW):
        super().__init__(MANAGER, WINDOW)
        w_shape = loads(CONFIG.get('window','shape'))
        fps = CONFIG.getint('window','fps')
        
        ''' Initialize graphics '''
        # Initializing in boids_instances.py caused errors
        bg_img = pygame.image.load(CONFIG.get('window', 'background_fp')).convert_alpha()
        tuna_img = pygame.image.load('images/tuna.png').convert_alpha()
        gw_shark_img = pygame.image.load('images/great_white_shark.png').convert_alpha()
        mine_img = pygame.image.load('images/mine.png').convert_alpha()

        bg_img = pygame.transform.scale(bg_img, w_shape)
        tuna_img = pygame.transform.scale(tuna_img, (70,30))
        gw_shark_img = pygame.transform.scale(gw_shark_img, (200,150))
        mine_img = pygame.transform.scale(mine_img, (90,90))

        panel = pygame.Rect(w_shape[0]*0.95, 0, w_shape[0]*0.05, w_shape[1])
        panel_border = pygame.Rect(w_shape[0]*0.95, -10, w_shape[0]*0.10, w_shape[1]*1.1)
        ''''''''''''''''''''''''''

        img_list = [tuna_img, mine_img, gw_shark_img]

        # alter w_shape to fit simulation area 
        w_shape = (int(w_shape[0]*0.95), w_shape[1])
        simulation_area = pygame.Rect(0,0, w_shape[0], w_shape[1])

        # Get the addresses of instance lists 
        preys = boids_i.preys
        obstacles = boids_i.obstacles
        predators = boids_i.predators
        
        # Turn locals to attributes
        self.__dict__.update(locals())
        self.initialize()

    def initialize(self):
        self.update_user_input()

        self.insert_class = tuna.tuna
        self.insert_list = self.preys
        self.insert_img = self.img_list[0]


    def update_graphics(self):
        '''
        Blits and flips
        '''
        self.WINDOW.blit(self.bg_img, (0,0))

        for instance in self.obstacles:
            instance.draw(self.WINDOW)

        for instance in self.preys:
            instance.draw(self.WINDOW) 
       
        for instance in self.predators:
            instance.draw(self.WINDOW)

        pygame.draw.rect(self.WINDOW, (50,50,50), self.panel)
        pygame.draw.rect(self.WINDOW, (200,200,200), self.panel_border, 3)

        for interface_obj in boids_i.all_list:
            interface_obj.draw(self.WINDOW)

        pygame.display.update()

    
    def animations(self):
        '''
        Method that handles animations, which are
        changes in graphics that does not affect the game
        '''
        boids_i.counter.text_r = f'Entities: {len(self.all_array)}'


    def interact_user(self):
        '''
        Method for user interactions
        '''
        # self.mouse = (left button, middle.., right..)
        if(any(self.mouse)):
            # Simulation is the area where the fish swim in
            if(self.simulation_area.collidepoint(self.mouse_pos)):
                if(self.kbinput[pygame.K_LCTRL]):
                    self.insert_list.append(self.insert_class(self.mouse_pos, self.insert_img))
                elif(self.click):
                    self.insert_list.append(self.insert_class(self.mouse_pos, self.insert_img))
        
        '''
        So only one lever can be activated at a time
        '''
        for i in range(len(boids_i.levers)):
            if(boids_i.levers[i].interact_mouse(self.mouse_pos, self.click)):
                for lever in boids_i.levers:
                    lever.state = False
                boids_i.levers[i].state = True
                self.insert_class, self.insert_list = boids_i.levers[i].get_class_and_list()
                self.insert_img = self.img_list[i]
    
        '''
        self.click is the click event itself (using 
        that instead to avoid a stream of true 
        values from using self.mouse)
        '''
        for button in boids_i.state_buttons:
            button.interact_mouse(self.mouse_pos, self.click)
            if(button.state):
                self.next_state = self.MANAGER.get_state(button.next_state)
                self._active = False

        #Reset button
        boids_i.reset.interact_mouse(self.mouse_pos, self.click)
        if(boids_i.reset.state):
            self.reload()


    def logic(self):
        '''
        Method for handling logic 
        '''
        self.all_array = self.preys+self.obstacles+self.predators
        if(len(self.all_array)):

            self.num_preys = len(self.preys)
            self.num_obstacles = len(self.obstacles)
            self.num_predators = len(self.predators)

            '''
            Preys and predators are going to use the obstacle index
            to aid the slicing process of the dist_matrix. (The address
            of this state-instance will be passed to preys and predators)
            '''
            self.obstacle_index = self.num_preys+self.num_obstacles

            pos_vecs = np.array([obj.pos for obj in self.all_array])
            self.vel_vecs = np.array([obj.vel for obj in self.all_array])

            '''
            I am extremely sorry for the code below, but I am doing this
            in the name of the performance gods

            The code beneath calculates the relative positions of every
            instances to each other in one go. 

            self.dist_matrix has the shape (N, N, 2), where N are the total
            number of instances. The axis' of self.dist_matrix contains the 
            following:

            axis = 0: An euclidian difference vector matrix with respect to 
                      instance i
            
            axis = 1: The difference vectors between instance i and the rest 
            
            axis = 2: The difference vector between instance i and j (j element 
                      all instances)

            E.g.
            Let a, b, c be positional vectors ([x,y])

            Then the code takes
            [a, b, c]

            and calculates

            [[a-a,  [a-b,  [a-c, 
              b-a,   b-b,   b-c,
              c-a],  c-b],  c-c]]

            Remember that a (a-b) has a length of two. Therefore the resulting matrix 
            has shape (3,3,2)   
            '''
            self.dist_matrix = pos_vecs - pos_vecs.reshape(-1,1,2)
            
            self.dist_matrix_norms = np.linalg.norm(self.dist_matrix, axis=2)
            self.randvals = np.random.randn(len(self.all_array))/12

            for i in range(self.num_preys):
                self.preys[i].apply_behavior(self, i)
            
            for i in range(self.num_predators):
                self.predators[i].apply_behavior(self, i)
        

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
        Do a soft reload
        '''
        reload(boids_i)
        self.preys = boids_i.preys
        self.obstacles = boids_i.obstacles
        self.predators = boids_i.predators
        self.initialize()

