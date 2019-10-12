'''
Initializing instances with the purpose
the be used in the menu_state
'''
import pygame
from objects import interface
from main import CONFIG
from json import loads 
from objects import tuna

pygame.font.init()
WINDOW_SHAPE = loads(CONFIG.get('window','shape'))
font = CONFIG.get('general','font')
text_x_pos = WINDOW_SHAPE[0]*CONFIG.getfloat('menu_state','text_x_ratio')
font_size = int(WINDOW_SHAPE[0]*CONFIG.getfloat('menu_state', 'font_window_ratio'))
font_color = loads(CONFIG.get('menu_state','font_color'))

'''
text_list are for text objects without any 
further functionality
'''
text_list = [
    interface.text_float(
        text='Boids & Particle Physics Simulator',
        pos=(text_x_pos, WINDOW_SHAPE[1]*0.05),
        color=font_color, 
        font=font, 
        font_size=int(font_size*1.8), 
    ),
]

'''
button_changestate_list are all menu buttons that changes states. 
The states assigned to each button can bee seen at the next_state
argument for each button object
'''
button_changestate_list = [
    interface.button_change_state(
        text='Boids simulation', 
        pos=(text_x_pos, WINDOW_SHAPE[1]*0.20), 
        color=font_color, 
        color_mouseover=[180,200,255], 
        font=font, 
        font_size=font_size,
        next_state='boids'
    ),

    interface.button_change_state(
        text='Particle physics simulation (Experimental parallel proccessing)', 
        pos=(text_x_pos, WINDOW_SHAPE[1]*0.28), 
        color=font_color, 
        color_mouseover=[180,200,255], 
        font=font, 
        font_size=font_size,
        next_state='particles'
    ),

    interface.button_change_state(
        text='Information and instructions', 
        pos=(text_x_pos, WINDOW_SHAPE[1]*0.36), 
        color=font_color, 
        color_mouseover=[180,200,255], 
        font=font, 
        font_size=font_size,
        next_state='info'
    ),

    interface.decorated_button_change_state(
        text='Exit', 
        pos=(text_x_pos, WINDOW_SHAPE[1]*0.91), 
        color=[155,155,155], 
        color_mouseover=[180,200,255], 
        font=font, 
        font_size=int(font_size*1.1),
        next_state='exit'
    ),
]


all_list = text_list+button_changestate_list