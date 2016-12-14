
# Brian Landes
# Final Project
# October 27, 2016

# from GameObject import GameObject
import GameObject
from Utilities import GetAngle
from Utilities import GetDistance
from Utilities import CheckObjectCollision
from Utilities import Reposition
from Utilities import RepositionBoth
from SpriteSheet import SpriteSheet

import math,os,pygame,random

SPRITE_SIZE = 30
SIZE = 200
EXPIRE_RANGE = 5000

class Bomb(GameObject.GameObject):
    def __init__(self, game):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor

        self.color = (225,0,0)
        self.radius = SPRITE_SIZE
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
                self.Detonate()

    def Detonate(self):
        self.game.ExplodeObject(self)
        self.Destroy()

        self.game.audio.PlayBomb()

        # check the trees
        for tree in self.game.collision_layers[GameObject.STATIC]:
            distance = GetDistance(self, tree)

            if distance - tree.radius < SIZE:
                tree.Destroy()
                self.game.ExplodeObject(tree)
                # self.game.audio.PlayTreeExplosion(distance)

        # check each enemy against each other enemy
        for other_enemy in self.game.collision_layers[GameObject.ENEMY]:
            distance = GetDistance(self, other_enemy)

            if distance - other_enemy.radius < SIZE:
                other_enemy.Destroy()
                self.game.audio.PlayEnemyDeath(GetDistance(other_enemy,self.game.player))
                self.game.ExplodeObject(other_enemy)
