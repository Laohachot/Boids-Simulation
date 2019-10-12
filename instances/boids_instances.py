'''
Initializing instances with the purpose
the be used in the boids_state
'''
import pygame
from objects import interface
from main import CONFIG
from json import loads 

from objects import tuna
from objects import uw_mine
from objects import shark

# pygame.init()
pygame.font.init()
WINDOW_SHAPE = loads(CONFIG.get('window','shape'))
font = CONFIG.get('general','font')
font_size = int(WINDOW_SHAPE[0]*CONFIG.getfloat('boids_state', 'font_window_ratio'))
font_color_buttons = loads(CONFIG.get('boids_state','font_color_buttons'))
font_color_levers = loads(CONFIG.get('boids_state','font_color_levers'))

'''
Define prey, obstacle and predator list here since the lever_with_fishclass
levers needs the addresses 
'''
preys = []
obstacles = []
predators = []


'''
Mass slaughter button
'''
reset = interface.decorated_button(
        text='Reset',
        pos=(WINDOW_SHAPE[0]*0.955, WINDOW_SHAPE[1]*0.88),
        color=font_color_buttons,
        color_mouseover=[180,200,255],
        font=font,
        font_size=font_size
)

'''
state_buttons is kinda the same as the butto_changestate_list
in the menu instances. Except these are <3*DeCoRaTeD*<3 
'''
state_buttons = [
        interface.decorated_button_change_state(
                text='Menu', 
                pos=(WINDOW_SHAPE[0]*0.955, WINDOW_SHAPE[1]*0.96), 
                color=font_color_buttons, 
                color_mouseover=[180,200,255], 
                font=font, 
                font_size=font_size,
                next_state='menu'
        ),

        interface.decorated_button_change_state(
                text=' Help ', 
                pos=(WINDOW_SHAPE[0]*0.955, WINDOW_SHAPE[1]*0.92), 
                color=font_color_buttons, 
                color_mouseover=[180,200,255], 
                font=font, 
                font_size=font_size,
                next_state='info'
        )
]

'''
levers are a list containing the levers that toggles to 
insert objects into the simulation.
'''
levers = [
        interface.lever_with_fishclass(
                text='Tuna', 
                pos=(WINDOW_SHAPE[0]*0.957, WINDOW_SHAPE[1]*0.02), 
                color=font_color_levers, 
                color_mouseover=[180,200,255], 
                color_active=[255,255,255],
                font=font, 
                font_size=font_size, 
                state=True,
                class_address=tuna.tuna,
                instance_list=preys
        ),

        interface.lever_with_fishclass(
                text='Mine', 
                pos=(WINDOW_SHAPE[0]*0.957, WINDOW_SHAPE[1]*0.06), 
                color=font_color_levers, 
                color_mouseover=[180,200,255], 
                color_active=[255,255,255],
                font=font, 
                font_size=font_size, 
                state=False,
                class_address=uw_mine.uw_mine,
                instance_list=obstacles
        ),

        interface.lever_with_fishclass(
                text='Shark', 
                pos=(WINDOW_SHAPE[0]*0.957, WINDOW_SHAPE[1]*0.10), 
                color=font_color_levers, 
                color_mouseover=[180,200,255], 
                color_active=[255,255,255],
                font=font, 
                font_size=font_size, 
                state=False,
                class_address=shark.shark,
                instance_list=predators
        )
]


# Entity counter in simulation
# Used both in boids and particles
counter = interface.text_float_active(
        text='Entities',
        pos=(WINDOW_SHAPE[0]*0.02, WINDOW_SHAPE[1]*0.94),
        color=loads(CONFIG.get('boids_state','counter_color')),
        font=font, 
        font_size=int(font_size)
)


all_list = levers + state_buttons + [counter, reset]

