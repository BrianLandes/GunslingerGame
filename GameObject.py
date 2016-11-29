
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
        self.collision_flags.get(flag,False)

    def Draw(self):
        pygame.draw.circle(self.game.screen, self.color, (
            int(self.x + self.game.world_x),
            int(self.y + self.game.world_y ) ),
            int(self.radius) )

    def Destroy(self):
        self.dead = True
        self.game.game_objects.remove(self)

    def Update(self):
        self.x += self.vel_x
        self.y += self.vel_y

        # if this object gets far enough away from the player we can remove it and stop worrying about it
        if self.expire_range > 0:  # only if the expire range is set to a positive number
            d = GetDistance(self.game.player, self)  # get the distance to the player
            if d > self.expire_range:
                # remove it from the game_objects list (if we were iterating
                # through the original list it wouldn't let us do this)
                self.Destroy()

#########
# Trees

# constants
TREE_EXPIRE_RANGE = 5000
TREE_SIZE = 70
TREE_SIZE_VARIANCE = 30 # + or - this many units in size randomly

# trees will all reuse the same images so we only need to load it once
treeSprites = []
for folderName, subfolders, filenames in os.walk('sprites/trees/'):
    # for each file we find in this folder
    for filename in filenames:
        # sometimes Windows will make this file in your folders and we can't load that
        if filename == 'Thumbs.db':
            # so just skip it
            continue
        #load a sprite and add it to our availables sprites list
        image = pygame.image.load('sprites/trees/'+filename)
        treeSprites.append( image )



class Tree(GameObject):
    def __init__(self, game):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor

        self.expire_range = TREE_EXPIRE_RANGE
        self.radius = int( TREE_SIZE + random.random()*TREE_SIZE_VARIANCE*2.0 - TREE_SIZE_VARIANCE)
        sprite = random.choice(treeSprites)
        self.sprite = pygame.transform.scale( sprite, (self.radius*2,self.radius*2) )
        # self.sprite = treeSprite
        self.SetCollisionFlag( STATIC )

    def Draw(self):
        # override the original GameObject.Update method
        # our (x,y) is the center, but it blits to the top left
        x = int(self.x + self.game.world_x - self.radius)
        y = int(self.y + self.game.world_y - self.radius )
        self.game.screen.blit(self.sprite, ( x,y ) )

    def Update(self):
        # override the original GameObject.Update method
        # we'll still call the original
        super().Update() # updates position and checks for expiration
        # trees also need to check themselves for collision with the player and reposition the player
        if CheckObjectCollision(self,self.game.player):
            # move just the player so there is no more collision
            Reposition(self.game.player, self)
