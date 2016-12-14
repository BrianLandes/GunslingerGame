
import GameObject
import pygame
import os
import random
from Utilities import *

# constants
TREE_EXPIRE_RANGE = 5000
# TREE_SIZE = 70
# TREE_SIZE_VARIANCE = 30 # + or - this many units in size randomly

loaded = False

folder = 'sprites/trees/'
sprites = 'tree_sprite.png tree_sprite_02.png bush_01.png bush_02.png ' \
          'pine_tree.png pine_tree_1.png pine_tree_2.png'.split()

sprite_pool = []

## LEVEL 1
sprite_pool.append({'path': 'tree_sprite.png',
          'level': 1,
          'probability': 1,
          'radius': 90, 'radius_variance': 20,
          'size_mod': 1.4,
          'y_offset': -0.2,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'tree_sprite_02.png',
          'level': 1,
          'probability': 0.8,
          'radius': 70, 'radius_variance': 40,
          'size_mod': 1.4,
          'y_offset': -0.2,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'bush_01.png',
          'level': 1,
          'probability': 0.9,
          'radius': 40, 'radius_variance': 20,
          'size_mod': 1.45,
          'y_offset': 0,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'bush_02.png',
          'level': 1,
          'probability': 0.7,
          'radius': 40, 'radius_variance': 20,
          'size_mod': 1.45,
          'y_offset': 0,
          'image': None,
          'only_one': False,
          'spawned': False})

## LEVEL 2
sprite_pool.append({'path': 'tree_sprite_02.png',
          'level': 2,
          'probability': 1.0,
          'radius': 90, 'radius_variance': 20,
          'size_mod': 1.4,
          'y_offset': -0.2,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'bush_02.png',
          'level': 2,
          'probability': 0.3,
          'radius': 40, 'radius_variance': 20,
          'size_mod': 1.45,
          'y_offset': 0,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'buried_head.png',
          'level': 2,
          'probability': 0.003,
          'radius': 60, 'radius_variance': 20,
          'size_mod': 1.6,
          'y_offset': -.1,
          'image': None,
          'only_one': False,
          'spawned': False})

## LEVEL 3
sprite_pool.append({'path': 'obsidian.png',
          'level': 3,
          'probability': 1.0,
          'radius': 50, 'radius_variance': 20,
          'size_mod': 1.4,
          'y_offset': -0.6,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'obsidian.png',
          'level': 3,
          'probability': 0.5,
          'radius': 100, 'radius_variance': 30,
          'size_mod': 1.4,
          'y_offset': -0.6,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'bush_02.png',
          'level': 3,
          'probability': 0.1,
          'radius': 40, 'radius_variance': 20,
          'size_mod': 1.45,
          'y_offset': 0,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'tree_sprite_02.png',
          'level': 3,
          'probability': 0.1,
          'radius': 70, 'radius_variance': 10,
          'size_mod': 1.4,
          'y_offset': -0.2,
          'image': None,
          'only_one': False,
          'spawned': False})

## LEVEL 4
sprite_pool.append({'path': 'obsidian.png',
          'level': 4,
          'probability': 1.0,
          'radius': 60, 'radius_variance': 20,
          'size_mod': 1.4,
          'y_offset': -0.6,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'obsidian.png',
          'level': 4,
          'probability': 0.5,
          'radius': 120, 'radius_variance': 20,
          'size_mod': 1.4,
          'y_offset': -0.6,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'purple_crystal_02.png',
          'level': 4,
          'probability': 0.3,
          'radius': 20, 'radius_variance': 5,
          'size_mod': 1.3,
          'y_offset': -1.5,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'purple_crystal_02.png',
          'level': 4,
          'probability': 0.005,
          'radius': 130, 'radius_variance': 10,
          'size_mod': 1.3,
          'y_offset': -1.5,
          'image': None,
          'only_one': False,
          'spawned': False})

# LEVEL 5

sprite_pool.append({'path': 'pine_tree.png',
          'level': 5,
          'probability': 1.0,
          'radius': 60, 'radius_variance': 20,
          'size_mod': 1.8,
          'y_offset': -1.6,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'pine_tree_1.png',
          'level': 5,
          'probability': 0.3,
          'radius': 60, 'radius_variance': 20,
          'size_mod': 1.8,
          'y_offset': -1.6,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'pine_tree_2.png',
          'level': 5,
          'probability': 0.03,
          'radius': 80, 'radius_variance': 10,
          'size_mod': 2.0,
          'y_offset': -1.6,
          'image': None,
          'only_one': False,
          'spawned': False})

# LEVEL 6
sprite_pool.append({'path': 'pink_tree_01.png',
          'level': 6,
          'probability': 1.0,
          'radius': 60, 'radius_variance': 20,
          'size_mod': 1.8,
          'y_offset': -1.6,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'pink_tree_02.png',
          'level': 6,
          'probability': 1.0,
          'radius': 60, 'radius_variance': 20,
          'size_mod': 1.8,
          'y_offset': -1.6,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'pink_tree_03.png',
          'level': 6,
          'probability': 0.1,
          'radius': 20, 'radius_variance': 5,
          'size_mod': 1.8,
          'y_offset': -1.8,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'pink_tree_04.png',
          'level': 6,
          'probability': 0.1,
          'radius': 20, 'radius_variance': 5,
          'size_mod': 1.8,
          'y_offset': -1.8,
          'image': None,
          'only_one': False,
          'spawned': False})

# LEVEL 7
sprite_pool.append({'path': 'pink_tree_01.png',
          'level': 7,
          'probability': 1.0,
          'radius': 60, 'radius_variance': 20,
          'size_mod': 1.8,
          'y_offset': -1.6,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'pink_tree_02.png',
          'level': 7,
          'probability': 1.0,
          'radius': 60, 'radius_variance': 20,
          'size_mod': 1.8,
          'y_offset': -1.6,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'pink_tree_03.png',
          'level': 7,
          'probability': 0.1,
          'radius': 20, 'radius_variance': 5,
          'size_mod': 1.8,
          'y_offset': -1.8,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'pink_tree_04.png',
          'level': 7,
          'probability': 0.1,
          'radius': 20, 'radius_variance': 5,
          'size_mod': 1.8,
          'y_offset': -1.8,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'tree_sprite_02.png',
          'level': 7,
          'probability': 1.0,
          'radius': 70, 'radius_variance': 40,
          'size_mod': 1.4,
          'y_offset': -0.2,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'bush_01.png',
          'level': 7,
          'probability': 0.05,
          'radius': 40, 'radius_variance': 20,
          'size_mod': 1.45,
          'y_offset': 0,
          'image': None,
          'only_one': False,
          'spawned': False})
sprite_pool.append({'path': 'bush_02.png',
          'level': 7,
          'probability': 0.1,
          'radius': 40, 'radius_variance': 20,
          'size_mod': 1.45,
          'y_offset': 0,
          'image': None,
          'only_one': False,
          'spawned': False})

MAX_LEVEL = 7

# sprite_pool.append({'path': 'purple_crystal_01.png',
#           'level': 1,
#           'probability': 1.0,
#           'radius': 40, 'radius_variance': 10,
#           'size_mod': 0.9,
#           'y_offset': -0.7,
#           'image': None,
#           'only_one': False,
#           'spawned': False})


def Load():
    # trees will all reuse the same images so we only need to load it once
    for sprite in sprite_pool:
        #load a sprite and add it to our availables sprites list
        image = pygame.image.load(folder+sprite['path']).convert_alpha()
        sprite['image'] = image

    global loaded
    loaded = True

def RandomTree(game):
    values = []
    probs = []
    # time = game.total_game_time
    for sprite in sprite_pool:
        # print(time,sprite['level'])
        if game.level == sprite['level'] or game.level%MAX_LEVEL==sprite['level'] or\
                (game.level%MAX_LEVEL==0 and sprite['level']==MAX_LEVEL):
            if not sprite['only_one'] or not sprite['spawned']:
                values.append(sprite)
                probs.append( sprite['probability'] )

    sprite = RandomValueFromProbabilities(values,probs)
    sprite['spawned'] = True
    return sprite

class Tree(GameObject.GameObject):
    def __init__(self, game):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor

        if not loaded:
            Load()
        self.color = (255,0,0)
        self.expire_range = TREE_EXPIRE_RANGE

        id = RandomTree(game)

        tree_sprite = RandomTree(game)

        self.radius = tree_sprite['radius'] + random.random()*tree_sprite['radius_variance']*2.0 - tree_sprite['radius_variance']

        self.y_offset = self.radius*tree_sprite['y_offset']

        sprite = tree_sprite['image']
        sprite_size_mod = tree_sprite['size_mod']
        self.sprite_width = int(self.radius*2*sprite_size_mod)
        self.sprite_height = int( self.sprite_width * sprite.get_height()/sprite.get_width() )
        self.sprite = pygame.transform.scale( sprite, (self.sprite_width,self.sprite_height) )
        if random.random() > 0.5:
            self.sprite = pygame.transform.flip(self.sprite,True,False)
        # self.sprite = treeSprite
        self.SetCollisionFlag( GameObject.STATIC )

    def Draw(self):
        # self.DebugDraw()

        # our (x,y) is the center, but it blits to the top left
        x = int(self.x + self.game.world_x - self.sprite_width*0.5)
        y = int(self.y + self.game.world_y - self.sprite_height*0.5 + self.y_offset)
        self.game.screen.blit(self.sprite, ( x,y ) )

    def Update(self):
        # override the original GameObject.Update method
        # we'll still call the original
        super().Update() # updates position and checks for expiration
        # trees also need to check themselves for collision with the player and reposition the player
        if CheckObjectCollision(self,self.game.player):
            # move just the player so there is no more collision
            Reposition(self.game.player, self)