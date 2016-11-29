
# Brian Landes
# Final Project
# October 27, 2016

# from GameObject import GameObject
import GameObject
from Utilities import GetAngle
from Utilities import CheckObjectCollision
from Utilities import Reposition
from Utilities import RepositionBoth
from SpriteSheet import SpriteAnimator

import math,pygame,os,random

class Explosion(GameObject.GameObject):
    def __init__(self, game, width):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor
        self.radius = width *0.5
        self.sprite = SpriteAnimator('BombExploding.png', (13,1) )
        swidth, sheight = self.sprite.GetSpriteSize()
        self.sprite.Resize(width,int(width*sheight/swidth))
        self.sprite.AddFrame(7,0)
        self.sprite.AddFrame(8,0)
        self.sprite.AddFrame(9,0)
        self.sprite.AddFrame(10,0)
        self.sprite.AddFrame(11,0)
        self.sprite.AddFrame(12,0)
        self.sprite.loop = False

    def Draw(self):
        # override the original GameObject.Update method
        # our (x,y) is the center, but it blits to the top right
        x = int(self.x + self.game.world_x - self.radius)
        y = int(self.y + self.game.world_y - self.radius )
        self.sprite.UpdateAndDraw( self.game.screen, x, y )

    def Update(self):
        if self.sprite.stopped:
            self.game.DestroyObject(self)
