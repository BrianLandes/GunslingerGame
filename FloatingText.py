
import GameObject
import pygame
from pygame.locals import *


pygame.init()

FONT_NAME = 'fonts/LinBiolinum_RBah.ttf'
font = pygame.font.Font(FONT_NAME, 96 )

def New(game,color,line1,width,height,line2=None,line3=None,life=10,dies=True,
        target_object = None, target_offset = -110):
    ft = FloatingText(game)
    ft.color = color
    ft.line1 = line1
    ft.line2 = line2
    ft.line3 = line3
    ft.width = width
    ft.height = height
    ft.life = life
    ft.dies = dies
    ft.target_object = target_object
    ft.target_offset = target_offset
    return ft

class FloatingText(GameObject.GameObject):
    def __init__(self, game):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor

        self.color = (255,255,255)
        self.line1 = "Brian Landes"
        self.line2 = "Brian Landes"
        self.line3 = "Brian Landes"
        self.width = 100
        self.height = 100
        self.life = 10
        self.dies = True
        self.target_object = None
        self.target_offset = -110

        self.surface = None

        self.z = 9999

    def Draw(self):
        if self.game.paused:
            return
        # pygame.draw.circle(self.game.screen, self.color, (
        #     int(self.x + self.game.world_x),
        #     int(self.y + self.game.world_y ) ),
        #     int(self.radius) )

        if self.surface is None:
            self.RenderSurface()

        x = int(self.x + self.game.world_x - self.width*0.5)
        y = int(self.y + self.game.world_y - self.height*0.3 )
        if x < 0:
            x = 0
        if y <  0:
            y =  0
        if x > self.game.width - self.width:
            x = self.game.width - self.width
        if y > self.game.height - self.height:
            y = self.game.height - self.height
        self.game.screen.blit(self.surface, ( x,y ) )

    def RenderSurface(self):
        self.surface = pygame.Surface((self.width, self.height), flags=SRCALPHA, depth=32)

        # cause the lines to align along the bottom where the center of the game object is
        boxes = [
            Rect(0, self.height*0.6, self.width, self.height*0.3),
            Rect(0, self.height*0.3, self.width, self.height*0.3),
            Rect(0, 0, self.width, self.height*0.3),
        ]

        # put the lines (even if they are none) in descending order
        lines = [ self.line3, self.line2, self.line1 ]
        b = 0
        for line in lines:
            # grab each line and skip any Nones
            if line is None:
                continue
            box = boxes[b]
            b += 1
            self.DrawTextInBounds(self.surface,line, box, self.color)

    def Update(self):
        # override the original GameObject.Update method
        # call the game object's update method (applies our velocity)
        super().Update()

        if self.target_object is not None:
            self.x = self.target_object.x
            self.y = self.target_object.y + self.target_offset
            if self.target_object.dead:
                self.Destroy()


        if self.dies:
            self.life -= self.game.delta_time
            if self.life < 0.0:
                self.Destroy()



    def DrawTextInBounds( self, surface, string, rect, color):
        text = font.render(string, True, color, None)
        TX, TY = text.get_size()
        if TX/rect.width > TY/rect.height:
            # if the fit is better width-wise
            w = int( rect.width )
            textWidth = w
            textHeight = int(w * (TY / TX) )
        else:
            h = int( rect.height )
            textWidth = int(h * (TX / TY))
            textHeight = h

        # align in center/center
        x = int( rect.x + rect.width*0.5 - textWidth*0.5 )
        y = int( rect.y + rect.height*0.5 - textHeight *0.5 )
        text = pygame.transform.scale(text, (textWidth, textHeight) )
        surface.blit(text,(x, y))