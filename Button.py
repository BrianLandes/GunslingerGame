# Brian Landes
# October 4, 2016

import pygame
from pygame.locals import *

ALIGN_CENTER = 0
ALIGN_RIGHT = 1
ALIGN_LEFT = 2
ALIGN_TOP = 3
ALIGN_BOTTOM = 4

LIGHT_GREY      = (75, 75, 75)
GREY            = (150, 150, 150)
DARK_GREY       = (200,200,200)
BLACK           = (0, 0, 0)
WHITE           = (255, 255, 255)

class Button(object):
    # class that creates a button

    def __init__(self, surface, text, x, y, width, height, style):
        self.surface = surface
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.style = style
        self.mouse_over = False
        self.last_mouse_over = False
        self.mouse_down = False
        self.last_mouse_down = False
        self.pressed = False
        self.released = False
        self.enabled = True
        self.visible = True

        self.up_image = pygame.transform.scale(style.up_image, (int(self.width), int(self.height)))
        self.down_image = pygame.transform.scale(style.down_image, (int(self.width), int(self.height)))

    def Draw(self):
        if self.enabled:
            # get whether the mouse is being pressed (just button1)
            left_mouse_button, _, _ = pygame.mouse.get_pressed()
            # get the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # keep track of what was going on last frame
            self.last_mouse_over = self.mouse_over
            self.last_mouse_down = self.mouse_down

            # check whether the mouse is over our button
            self.mouse_over = PointAndRectColDet( (mouse_x, mouse_y), self.BoundsRect() )
            if self.mouse_over:
                pygame.mouse.set_visible(True)
            else:
                pygame.mouse.set_visible(False)
            # update whether the mouse is currently being down
            self.mouse_down = left_mouse_button

            # if our button was pressed
            # and the mouse is over our button
            # and the mouse was released
            # set 'released' to true for 1 frame
            if self.pressed and self.mouse_over and not self.mouse_down and self.last_mouse_down:
                self.released = True
            else:
                self.released = False

            # if the mouse is over our button and the mouse has been clicked since the last frame
            # put the button in a state of 'pressed' until the mouse button is released
            if self.mouse_over and self.mouse_down and not self.last_mouse_down:
                self.pressed = True
            elif not self.mouse_down:
                self.pressed = False

            font_color = self.style.font_up_color

            if self.pressed:
                self.surface.blit( self.down_image, (self.x, self.y) )
                # DrawRoundRect( self.surface, self.style.down_color,
                #         self.x, self.y, self.width, self.height, 10 )
                font_color = self.style.font_down_color
            # elif self.mouse_over:
            #     DrawRoundRect( self.surface, self.style.over_color,
            #             self.x, self.y, self.width, self.height, 10 )
            else:
                self.surface.blit( self.up_image, (self.x, self.y) )
                # DrawRoundRect( self.surface, self.style.up_color,
                #     self.x, self.y, self.width, self.height, 10 )
        else:
            # draw a disabled button
            DrawRoundRect( self.surface, self.style.disabled_color,
                    self.x, self.y, self.width, self.height, 10 )

            self.released = False
            self.pressed = False

        # draw the text, scaled to fit either width or height, which ever is smaller
        text = self.style.font.render(self.text, True, font_color, None)
        TX, TY = text.get_size()
        if TX/self.width > TY/self.height:
            # if the fit is better width-wise
            w = int( self.width - 2.0 * self.width * self.style.border_perc )
            textWidth = w
            textHeight = int(w * (TY / TX) )
        else:
            h = int( self.height - 2.0 * self.height * self.style.border_perc )
            textWidth = int(h * (TX / TY))
            textHeight = h
        text = pygame.transform.scale(text, (textWidth, textHeight) )
        if self.style.hor_align is ALIGN_CENTER:
            x = int( self.x + self.width*0.5 - textWidth*0.5 )
        elif self.style.hor_align is ALIGN_LEFT:
            x = int( self.x + self.width * self.style.border_perc )
        elif self.style.hor_align is ALIGN_RIGHT:
            x = int( self.x + self.width - self.width * self.style.border_perc - textWidth )
        if self.style.vert_align is ALIGN_CENTER:
            y = int( self.y + self.height*0.5 - textHeight *0.5 )
        elif self.style.vert_align is ALIGN_TOP:
            y = int( self.y + self.height * self.style.border_perc)
        elif self.style.vert_align is ALIGN_BOTTOM:
            y = int( self.y + self.height - self.height * self.style.border_perc - textHeight )
        self.surface.blit(text,(x, y))

    def BoundsRect(self):
        return (
                self.x,
                self.y,
                self.x + self.width,
                self.y + self.height
            )


class ButtonStyle(object):
    # class that defines how a button looks
    def __init__(self, up_image, over_color, down_image, disabled_color, font_name,
                 vert_align = ALIGN_BOTTOM, hor_align = ALIGN_RIGHT, border_perc = 0.25,
                 font_up_color = WHITE, font_down_color = BLACK, font_disabled_color = DARK_GREY ):
        self.up_image = pygame.image.load(up_image)
        self.over_color = over_color
        self.down_image = pygame.image.load(down_image)
        self.disabled_color = disabled_color
        self.font = pygame.font.Font(font_name, 96 )
        self.vert_align = vert_align
        self.hor_align = hor_align
        self.border_perc = border_perc
        self.font_up_color = font_up_color
        self.font_down_color = font_down_color
        self.font_disabled_color = font_disabled_color



def DrawRoundRect( surface, color, x, y, width, height, rounded ):
    left = int(x + rounded)
    right = int(x + width - rounded)
    top = int(y + rounded)
    bottom = int(y + height - rounded)
    
    pygame.draw.circle(surface, color, (left, top), rounded)
    pygame.draw.circle(surface, color, (right, top), rounded)
    pygame.draw.circle(surface, color, (left, bottom), rounded)
    pygame.draw.circle(surface, color, (right, bottom), rounded)

    pygame.draw.rect(surface, color, Rect((left, y), (width-rounded*2, height)))
    pygame.draw.rect(surface, color, Rect((x,top), (width,height-rounded*2)))

def PointAndRectColDet( point, rect ):
    # where point is a tuple: (x,y)
    # and rect is a tuple: (left, top, right, bottom)
    if point[0] < rect[0]:
        return False
    if point[1] < rect[1]:
        return False
    if point[0] > rect[2]:
        return False
    if point[1] > rect[3]:
        return False
    return True
