
# Brian Landes
# Final Project
# October 27, 2016

# from GameObject import GameObject
import GameObject
from Utilities import GetAngle
from Utilities import GetDistance
from Utilities import Lerp
from Utilities import CheckObjectCollision
from Utilities import Reposition
from Utilities import RepositionBoth
from SpriteSheet import SpriteAnimator
import FloatingText

import math,pygame,os,random

ENEMY_SIZE = 25
ENEMY_SPRITE_SIZE = 80
MIN_MOVE_SPEED = 8
MAX_MOVE_SPEED = 20

POINT_VALUE = 1

FLIP_SPEED = 0.3

initialized = False
enemies_sprites = []
def Initialize():
    global enemies_sprites
    for folderName, subfolders, filenames in os.walk('sprites/enemies/'):
        # for each file we find in this folder
        for filename in filenames:
            # sometimes Windows will make this file in your folders and we can't load that
            if filename == 'Thumbs.db':
                # so just skip it
                continue
            #load a sprite and add it to our availables sprites list
            image = pygame.image.load('sprites/enemies/'+filename).convert_alpha()
            enemies_sprites.append( image )

    global initialized
    initialized = True

class Enemy(GameObject.GameObject):
    def __init__(self, game):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor

        if not initialized:
            Initialize()

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
        self.sprite = [ pygame.transform.scale( sprite, (self.radius*2,new_height) ).convert_alpha() ]
        self.sprite.append( pygame.transform.flip( self.sprite[0], True, False ) )
        self.flipped = True # to keep track of whether our sprite is/should be flipped
        self.flip_timer = 0.0

    def Draw(self):
        # override the original GameObject.Update method
        # our (x,y) is the center, but it blits to the top right
        x = int(self.x + self.game.world_x - self.radius)
        y = int(self.y + self.game.world_y - self.radius )
        # self.sprite.UpdateAndDraw( self.game.screen, x, y )
        sprite = self.sprite[self.flipped]
        self.game.screen.blit(sprite, ( x,y ) )

    def Update(self):
        # override the original GameObject.Update method

        # make this enemy run towards the player
        theta = GetAngle( self.game.player.x - self.x, self.game.player.y - self.y )

        distance = GetDistance(self, self.game.player)
        # cause the bear to move faster if the player is further away
        lerp_value = distance/1000
        speed = Lerp(lerp_value,MIN_MOVE_SPEED,MAX_MOVE_SPEED)

        self.vel_x = math.cos(theta ) * speed
        self.vel_y = math.sin(theta) * speed

        self.flip_timer += self.game.delta_time
        while self.flip_timer > FLIP_SPEED:
            self.flipped = not self.flipped
            self.flip_timer -= FLIP_SPEED

        # call the game object's update method (applies our velocity)
        super().Update()

        # check this enemy against the player
        if CheckObjectCollision( self, self.game.player):
            # this will actually kill the player but for now just push them away
            Reposition( self, self.game.player )
            # let's have the enemy slow the player down if they're touching
            self.game.player.movement_penalty = 0.1
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
                self.game.ExplodeObject(self)
                # play the enemy death
                self.game.audio.PlayEnemyDeath(GetDistance(self,self.game.player))
                self.game.AddPoints(POINT_VALUE)
                floating_text = FloatingText.New(self.game, (255,247,84), "+%d"%POINT_VALUE,
                                    self.game.width*0.3, self.game.height*0.2,life=1)
                floating_text.x = self.x
                floating_text.y = self.y-50
                self.game.AddObject(floating_text)

                break
