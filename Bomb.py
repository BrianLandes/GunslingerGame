
# Brian Landes
# Final Project
# October 27, 2016

# from GameObject import GameObject
import GameObject
from Utilities import GetAngle
from Utilities import CheckObjectCollision
from Utilities import Reposition
from Utilities import RepositionBoth
from SpriteSheet import SpriteSheet

import math,os,pygame,random

SIZE = 80
EXPIRE_RANGE = 5000

class Bomb(GameObject.GameObject):
    def __init__(self, game):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor

        self.color = (225,0,0)
        self.radius = SIZE
        self.expire_range = EXPIRE_RANGE
        self.SetCollisionFlag( GameObject.BOMB )

        sprite = pygame.image.load('sprites/bomb.png')
        # we want to keep the original sprite's aspect ratio, but scale down to the bullet's size
        SX, SY = sprite.get_size()
        new_height = int(self.radius*2 * (SY/SX) )
        self.sprite = pygame.transform.scale( sprite, (self.radius*2,new_height) ).convert_alpha()


    def Draw(self):
        # override the original GameObject.Update method
        # our (x,y) is the center, but it blits to the top right
        x = int(self.x + self.game.world_x - self.radius)
        y = int(self.y + self.game.world_y - self.radius )
        self.game.screen.blit(self.sprite, ( x,y ) )

    def Update(self):
        # override the original GameObject.Update method
        # call the game object's update method (applies our velocity)
        super().Update()
        # check collision against bullets
        for bullet in self.game.collision_layers[GameObject.BULLET]:
            if CheckObjectCollision( self, bullet ):
                self.game.ExplodeObject(self)
                self.Destroy()

