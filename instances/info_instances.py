'''
Initializing instances with the purpose
the be used in the info_state
'''
import pygame
from objects import interface
from main import CONFIG
from json import loads 

pygame.font.init()
WINDOW_SHAPE = loads(CONFIG.get('window','shape'))
font = CONFIG.get('general','font')
font_size = int(WINDOW_SHAPE[0]*CONFIG.getfloat('info_state', 'font_window_ratio'))
font_color = loads(CONFIG.get('info_state', 'font_color'))
text_x_pos = WINDOW_SHAPE[0]*CONFIG.getfloat('info_state', 'text_x_ratio')

'''
text objects without any further functionality
'''
text_list = [
    interface.text_float(
        text='Information and instructions',
        pos=[text_x_pos, WINDOW_SHAPE[1]*0.05],
        color=font_color, 
        font=font, 
        font_size=int(font_size*1.5), 
    ),
    interface.text_float(
        text='Boids simulation: Toggle item type by clicking text buttons on right panel.',
        pos=[text_x_pos, WINDOW_SHAPE[1]*0.15],
        color=font_color, 
        font=font, 
        font_size=font_size, 
    ),
    interface.text_float(
        text='Holding LCTRL while pressing down the mouse enables continous insertion.',
        pos=[text_x_pos, WINDOW_SHAPE[1]*0.20],
        color=font_color, 
        font=font, 
        font_size=font_size, 
    ),
    interface.text_float(
        text='Particle physics simulation: Holding down right click creates a spring force pulling everything towards the mouse.',
        pos=[text_x_pos, WINDOW_SHAPE[1]*0.30],
        color=font_color, 
        font=font, 
        font_size=font_size, 
    ),
    interface.text_float(
        text='The particle physics simulation is experimental, and has horrible performance. The particles are non-bonding particles.',
        pos=[text_x_pos, WINDOW_SHAPE[1]*0.35],
        color=font_color,
        font=font, 
        font_size=font_size, 
    ),
    interface.text_float(
        text='Settings can be altered in the config.ini file.',
        pos=[text_x_pos, WINDOW_SHAPE[1]*0.45],
        color=font_color, 
        font=font, 
        font_size=font_size, 
    ),
    interface.text_float(
        text='Press F4 to exit.',
        pos=[text_x_pos, WINDOW_SHAPE[1]*0.55],
        color=font_color, 
        font=font, 
        font_size=font_size, 
    ),
    interface.text_float(
        text='Press backspace to revert to previous state.',
        pos=[text_x_pos, WINDOW_SHAPE[1]*0.60],
        color=font_color, 
        font=font, 
        font_size=font_size, 
    ),
]

'''
Back button for returning to whatever the 
previous was
'''
back_button = interface.decorated_button_change_state(
    text='Back',
    pos=(text_x_pos, WINDOW_SHAPE[1]*0.91),
    color=[155,155,155], 
    color_mouseover=[180,200,255], 
    font=font, 
    font_size=int(font_size*1.2),
    next_state='previous'
)
