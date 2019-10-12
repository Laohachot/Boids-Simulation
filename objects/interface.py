'''
Module that contains UI objects such 
as text, buttons and levers
'''

import pygame 


'''
The interface classes below are general classes for 
UI and text. The classes are often used as parent classes for 
more specialized UI classes, for example classes with some 
aesthethic decorations. 

General classes that ends with _active means that the object
will be actively re-rendered before each blit. Tthe purpose of 
that are for animations, such as moving text, text that changes 
color and such.
'''
class text_float:
    '''
    Text with floating position, not actively rendered
    '''
    def __init__(self, text, pos, color, font, font_size):
        self.text = text
        self.pos = pos 
        self.color = color 
        self.font = font 
        self.font_size = font_size

        self.text_type = pygame.font.Font(self.font, self.font_size)
        self.text_render = self.text_type.render(self.text, True, self.color)        


    def draw(self, window):
        window.blit(
            self.text_render,
            self.pos
        )
    

    def interact_mouse(self, mouse_pos, click):
        pass


'''
Variables ending with _r are the actual variables used
in rendering
'''
class text_float_active:
    '''
    Actively rendered text with floating position
    '''
    def __init__(self, text, pos, color, font, font_size):
        self.text = text 
        self.font_size = font_size
        self.font = font 

        self.text_r = text
        self.pos_r = pos
        self.color_r = color 
        self.font_size_r = self.font_size

        self.text_type = pygame.font.Font(self.font, self.font_size)
        self.text_render = self.text_type.render(self.text_r, True, self.color_r)
 
        # Updates the object __dict__ with all the local variables in init method
        self.__dict__.update(locals())


    def draw(self, window):
        self.text_type = pygame.font.Font(self.font, self.font_size_r)
        self.text_render = self.text_type.render(self.text_r, True, self.color_r)
        window.blit(
            self.text_render,
            self.pos_r
        )


    def interact_mouse(self):
        pass


class text_center(text_float):
    '''
    Centered text, not actively rendered
    '''
    def __init__(self, text, pos, window_shape, color, font, font_size):
        super().__init__(text, pos, color, font, font_size)
        pos[0] = (window_shape[0]-self.text_render.get_width())/2
        self.__dict__.update(locals())


class text_center_active(text_center, text_float_active):
    '''
    Actively rendered centered text
    '''
    def __init__(self, text, pos, window_shape, color, font, font_size):
        super().__init__(text, pos, window_shape, color, font, font_size)


class button_float_active(text_float_active):
    '''
    Actively rendered floating position button
    '''
    def __init__(self, text, pos, color, color_mouseover, font, font_size):
        super().__init__(text, pos, color, font, font_size)
        self.__dict__.update(locals())

        self.state = False

        self.rect = pygame.Rect(
            self.pos_r[0],
            self.pos_r[1],
            self.text_render.get_width(),
            self.text_render.get_height()
        )


    def interact_mouse(self, mouse_pos, click):
        if(self.rect.collidepoint(mouse_pos)):
            self.color_r = self.color_mouseover
            if(click):
                self.state = True
        else:
            self.state = False
            self.color_r = self.color


class lever_float_active(button_float_active):
    '''
    Levers are toggle-able buttons. 
    '''
    def __init__(self, text, pos, color, color_mouseover, color_active, font, font_size, state):
        super().__init__(text, pos, color, color_mouseover, font, font_size)
        self.state = state
        self.color_active = color_active
        if(self.state):
            self.color_r = color_active


    def interact_mouse(self, mouse_pos, click):
        if(self.rect.collidepoint(mouse_pos)):
            self.color_r = self.color_mouseover
            if(click):
                self.state = not self.state
                return True
        else:
            if(self.state):
                self.color_r = self.color_active
            else:
                self.color_r = self.color
            return False


'''
The classes defined below are specialized classes that 
inherits the classes above.
'''
class decorated_button(button_float_active):
    '''
    Actively renderd button with a bounding box
    '''
    def __init__(self, text, pos, color, color_mouseover, font, font_size):
        super().__init__(text, pos, color, color_mouseover, font, font_size)

        self.decor_pos_r = [0,0]
        self.decor_pos_r[0] = self.pos_r[0] - self.text_render.get_width()*0.05
        self.decor_pos_r[1] = self.pos_r[1] - self.text_render.get_height()*0.01

        self.decor_shape = [0,0]

        self.decor_shape[0] = self.text_render.get_width()*1.14
        self.decor_shape[1] = self.text_render.get_height()

    def draw(self, window):
        self.text_type = pygame.font.Font(self.font, self.font_size_r)
        self.text_render = self.text_type.render(self.text, True, self.color_r)
        window.blit(
            self.text_render,
            self.pos_r
        )

        pygame.draw.rect(
            window,
            self.color_r,
            (self.decor_pos_r[0], self.decor_pos_r[1], self.decor_shape[0], self.decor_shape[1]),
            2
        )

# _change_state objects simply has the name of a state stored as a string
class button_change_state(button_float_active):
    '''
    A button with floating position that also contains the string name
    of a state.
    '''
    def __init__(self, text, pos, color, color_mouseover, font, font_size, next_state):
        super().__init__(text, pos, color, color_mouseover, font, font_size)
        self.next_state = next_state


class decorated_button_change_state(decorated_button):
    '''
    A button with floating position that also contains the string name
    of a state. It is decorated with a square bounding box
    '''
    def __init__(self, text, pos, color, color_mouseover, font, font_size, next_state):
        super().__init__(text, pos, color, color_mouseover, font, font_size)
        self.next_state = next_state


class lever_with_fishclass(lever_float_active):
    '''
    A lever that contains the list of the fish type, and the fish class. 
    '''
    def __init__(self, text, pos, color, color_mouseover, color_active, font, font_size, state, 
                class_address, instance_list):
        super().__init__(text, pos, color, color_mouseover, color_active, font, font_size, state)
        self.class_address = class_address
        self.instance_list = instance_list

    def get_class_and_list(self):
        return self.class_address, self.instance_list   
    



