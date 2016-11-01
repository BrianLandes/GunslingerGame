
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

ENEMY_SIZE = 25
ENEMY_SPRITE_SIZE = 80
ENEMY_MOVE_SPEED = 10.5

enemies_sprites = []
for folderName, subfolders, filenames in os.walk('sprites/enemies/'):
    # for each file we find in this folder
    for filename in filenames:
        # sometimes Windows will make this file in your folders and we can't load that
        if filename == 'Thumbs.db':
            # so just skip it
            continue
        #load a sprite and add it to our availables sprites list
        image = pygame.image.load('sprites/enemies/'+filename)
        enemies_sprites.append( image )

class Enemy(GameObject.GameObject):
    def __init__(self, game):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor

        self.color = (225,0,0)
        self.radius = ENEMY_SIZE
        self.SetCollisionFlag( GameObject.ENEMY )
        # self.sprite = SpriteAnimator('enemy_spritesheet.png', (3,2) )
        # self.sprite.Resize(ENEMY_SPRITE_SIZE,ENEMY_SPRITE_SIZE)
        # self.sprite.AddFrame(0,0)
        # self.sprite.AddFrame(1,0)
        # self.sprite.AddFrame(2,0)
        # self.sprite.AddFrame(0,1)
        # self.sprite.AddFrame(1,1)

        sprite = random.choice(enemies_sprites)
        # we want to keep the original sprite's aspect ratio, but scale down to the bullet's size
        SX, SY = sprite.get_size()
        new_height = int(self.radius*2 * (SY/SX) )
        self.sprite = pygame.transform.scale( sprite, (self.radius*2,new_height) ).convert_alpha()

        self.running_right = True # to keep track of whether our sprite is/should be flipped

    def Draw(self):
        # override the original GameObject.Update method
        # our (x,y) is the center, but it blits to the top right
        x = int(self.x + self.game.world_x - self.radius)
        y = int(self.y + self.game.world_y - self.radius )
        # self.sprite.UpdateAndDraw( self.game.screen, x, y )
        self.game.screen.blit(self.sprite, ( x,y ) )

    def Update(self):
        # override the original GameObject.Update method

        # make this enemy run towards the player
        theta = GetAngle( self.game.player.x - self.x, self.game.player.y - self.y )
        self.vel_x = math.cos(theta ) * ENEMY_MOVE_SPEED
        self.vel_y = math.sin(theta) * ENEMY_MOVE_SPEED

        # right = self.vel_x > 0
        # if self.running_right is not right:
        #     self.sprite.Flip(True, False)
        #     self.running_right = right

        # call the game object's update method (applies our velocity)
        super().Update()

        # check this enemy against the player
        if CheckObjectCollision( self, self.game.player):
            # this will actually kill the player but for now just push them away
            Reposition( self, self.game.player )
            # self.Destroy()

        # check each enemy against each other enemy
        for other_enemy in self.game.collision_layers[GameObject.ENEMY]:
            if other_enemy is self:
                continue
            if CheckObjectCollision( self, other_enemy ):
                Reposition(self,other_enemy)

        # Check if this enemy was hit with a bullet
        for bullet in self.game.collision_layers[GameObject.BULLET]:
            if CheckObjectCollision( self, bullet ):
                self.Destroy()
                bullet.Destroy()
                # play the enemy death
                # PlaySound(enemy_death_sfx)
                break