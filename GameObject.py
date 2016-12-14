
# Brian Landes
# Final Project
# Game Object class

import pygame, sys, random, os
from Utilities import GetDistance
from Utilities import CheckObjectCollision
from Utilities import Reposition

#### Collision constants
PLAYER = 0
STATIC = 1
ENEMY = 2
BULLET = 3
COIN = 4
BOMB = 5
COL_FLAGS = [PLAYER,STATIC,ENEMY,BULLET,COIN,BOMB]

class GameObject(object):
    def __init__(self, game):
        self.game = game # a reference to the GunslingerGame class
        self.x = 0
        self.y = 0
        self.z = 0
        self.vel_x = 0
        self.vel_y = 0
        self.radius = 20
        self.color = ( 100, 100, 100 )
        self.dead = False
        self.expire_range = -1 # if this object becomes farther than this from the player then we can remove it
        self.collision_flags = {}

    def SetCollisionFlag(self, flag, bool_value = True):
        self.collision_flags[flag] = bool_value

    def GetCollisionFlag(self, flag ):
        #defaults to False
        return self.collision_flags.get(flag,False)

    def IsEnemy(self):
        return self.GetCollisionFlag( ENEMY )

    def IsStatic(self):
        return self.GetCollisionFlag( STATIC )

    def IsBomb(self):
        return self.GetCollisionFlag( BOMB )

    def Draw(self):
        pygame.draw.circle(self.game.screen, self.color, (
            int(self.x + self.game.world_x),
            int(self.y + self.game.world_y ) ),
            int(self.radius) )


    def DebugDraw(self):
        pygame.draw.circle(self.game.screen, self.color, (
            int(self.x + self.game.world_x),
            int(self.y + self.game.world_y ) ),
            int(self.radius) )

    def Destroy(self):
        self.dead = True
        self.game.needs_sorting = True
        try:
            self.game.game_objects.remove(self)
        except ValueError:
            print( self.__class__.__name__, 'was trying to destroy itself but failed' )



    def Update(self):
        self.x += self.vel_x
        self.y += self.vel_y

        # if this object gets far enough away from the player we can remove it and stop worrying about it
        if self.expire_range > 0 and not self.dead:  # only if the expire range is set to a positive number
            d = GetDistance(self.game.player, self)  # get the distance to the player
            if d > self.expire_range:
                # remove it from the game_objects list (if we were iterating
                # through the original list it wouldn't let us do this)
                self.Destroy()

#########
# Trees




