
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
        pass
##        # override the original GameObject.Update method
##
##        # make this enemy run towards the player
##        theta = GetAngle( self.game.player.x - self.x, self.game.player.y - self.y )
##        self.vel_x = math.cos(theta ) * ENEMY_MOVE_SPEED
##        self.vel_y = math.sin(theta) * ENEMY_MOVE_SPEED
##
##        right = self.vel_x > 0
##        if self.running_right is not right:
##            self.sprite.Flip(True, False)
##            self.running_right = right
##
##        # call the game object's update method (applies our velocity)
##        super().Update()
##
##        # check this enemy against the player
##        if CheckObjectCollision( self, self.game.player):
##            # this will actually kill the player but for now just push them away
##            Reposition( self, self.game.player )
##            # self.Destroy()
##
##        # check each enemy against each other enemy
##        for other_enemy in self.game.collision_layers[GameObject.ENEMY]:
##            if other_enemy is self:
##                continue
##            if CheckObjectCollision( self, other_enemy ):
##                Reposition(self,other_enemy)
##
##        # Check if this enemy was hit with a bullet
##        for bullet in self.game.collision_layers[GameObject.BULLET]:
##            if CheckObjectCollision( self, bullet ):
##                swap = bullet.vel_x
##                bullet.vel_x = -bullet.vel_y
##                bullet.vel_y = swap
##                Reposition(bullet,self)
##                bullet.RotateBasedOnVelocity()
##                # self.Destroy()
##                # bullet.Destroy()
##                # play the enemy death
##                # PlaySound(enemy_death_sfx)
##                break
