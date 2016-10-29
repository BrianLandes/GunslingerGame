
# Brian Landes
# Final Project
# October 27, 2016

from GameObject import GameObject
from Utilities import GetAngle
from Utilities import CheckObjectCollision
from Utilities import Reposition
from Utilities import RepositionBoth
from SpriteSheet import SpriteAnimator

import math

ENEMY_SIZE = 40
ENEMY_MOVE_SPEED = 7

class Enemy(GameObject):
    def __init__(self, game):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor

        self.color = (225,0,0)
        self.radius = ENEMY_SIZE

        self.sprite = SpriteAnimator('enemy_spritesheet.png', (3,2) )
        self.sprite.Resize(self.radius*2,self.radius*2)
        self.sprite.AddFrame(0,0)
        self.sprite.AddFrame(1,0)
        self.sprite.AddFrame(2,0)
        self.sprite.AddFrame(0,1)
        self.sprite.AddFrame(1,1)

        self.running_right = True # to keep track of whether our sprite is/should be flipped

    def Draw(self):
        # override the original GameObject.Update method
        # our (x,y) is the center, but it blits to the top right
        x = int(self.x + self.game.world_x - self.radius)
        y = int(self.y + self.game.world_y - self.radius )
        self.sprite.UpdateAndDraw( self.game.screen, x, y )

    def Update(self):
        # override the original GameObject.Update method

        # make this enemy run towards the player
        theta = GetAngle( self.game.player.x - self.x, self.game.player.y - self.y )
        self.vel_x = math.cos(theta ) * ENEMY_MOVE_SPEED
        self.vel_y = math.sin(theta) * ENEMY_MOVE_SPEED

        right = self.vel_x > 0
        if self.running_right is not right:
            self.sprite.Flip(True, False)
            self.running_right = right

        # call the game object's update method (applies our velocity)
        super().Update()

        # check this enemy against the player
        if CheckObjectCollision( self, self.game.player):
            # this will actually kill the player but for now just push them away
            Reposition( self, self.game.player )

        # check each enemy against each other enemy
        for other_enemy in self.game.enemies_layer:
            if CheckObjectCollision( self, other_enemy ):
                Reposition(self,other_enemy)
        # add this enemy to the accumulating collision layer
        self.game.enemies_layer.append(self)