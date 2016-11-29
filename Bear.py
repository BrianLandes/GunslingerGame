
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
from SpriteSheet import Animation

import math,pygame,os,random

ENEMY_SIZE = 35
ENEMY_SPRITE_SIZE = 300
MIN_MOVE_SPEED = 5
MAX_MOVE_SPEED = 11

GROWL_TIME = 10.0

##enemies_sprites = []
##for folderName, subfolders, filenames in os.walk('sprites/enemies/'):
##    # for each file we find in this folder
##    for filename in filenames:
##        # sometimes Windows will make this file in your folders and we can't load that
##        if filename == 'Thumbs.db':
##            # so just skip it
##            continue
##        #load a sprite and add it to our availables sprites list
##        image = pygame.image.load('sprites/enemies/'+filename)
##        enemies_sprites.append( image )

class Bear(GameObject.GameObject):
    def __init__(self, game):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor

        self.color = (225,0,0)
        self.radius = ENEMY_SIZE
        self.SetCollisionFlag( GameObject.ENEMY )
        self.sprite = SpriteAnimator('sprites/bear2/sheet.png', (8,1) )
        swidth, sheight = self.sprite.GetSpriteSize()
        self.sprite.Resize(ENEMY_SPRITE_SIZE,int(ENEMY_SPRITE_SIZE*sheight/swidth))

        run_animation = Animation()
        run_animation.AddFrame(0,0)
        run_animation.AddFrame(1,0)
        run_animation.AddFrame(2,0)
        run_animation.AddFrame(3,0)
        self.sprite.AddAnimation(run_animation)

        smash_animation = Animation()
        smash_animation.AddFrame(4,0)
        smash_animation.AddFrame(5,0)
        smash_animation.AddFrame(6,0, callback = self.SmashCallback )
        smash_animation.AddFrame(7,0)
        self.sprite.AddAnimation(smash_animation)

        self.growl_timer = 0.0

##        sprite = random.choice(enemies_sprites)
        # we want to keep the original sprite's aspect ratio, but scale down to the bullet's size
##        SX, SY = sprite.get_size()
##        new_height = int(self.radius*2 * (SY/SX) )
##        self.sprite = pygame.transform.scale( sprite, (self.radius*2,new_height) ).convert_alpha()

        self.running_right = True # to keep track of whether our sprite is/should be flipped

    def Draw(self):
##        pygame.draw.circle(self.game.screen, self.color, (
##            int(self.x + self.game.world_x),
##            int(self.y + self.game.world_y ) ),
##            int(self.radius) )
        
        # override the original GameObject.Update method
        # our (x,y) is the center, but it blits to the top right
        x = int(self.x + self.game.world_x - ENEMY_SPRITE_SIZE*0.5)
        y = int(self.y + self.game.world_y - ENEMY_SPRITE_SIZE*0.5 )
        self.sprite.UpdateAndDraw( self.game.screen, x, y )
        # self.game.screen.blit(self.sprite, ( x,y ) )

    def SmashCallback(self):
        # this function gets called everytime a certain frame of the animation plays
        # this will be the frame where the cowboy's body hits the ground and theres a sound effect and an explosion
        print( 'smash' )

    def Update(self):
        # override the original GameObject.Update method


        if not self.game.player.dead:
            # make this enemy run towards the player
            theta = GetAngle( self.game.player.x - self.x, self.game.player.y - self.y )
            distance = GetDistance(self, self.game.player)
            # cause the bear to move faster if the player is further away
            lerp_value = distance/1000
            speed = Lerp(lerp_value,MIN_MOVE_SPEED,MAX_MOVE_SPEED)
            self.vel_x = math.cos(theta ) * speed
            self.vel_y = math.sin(theta) * speed

            right = self.vel_x > 0
            if self.running_right is not right:
                self.sprite.Flip(True, False)
                self.running_right = right

            # play a bear sound effect every so often
            self.growl_timer -= self.game.delta_time
            if self.growl_timer <= 0.0:
                self.growl_timer = GROWL_TIME + GROWL_TIME* random.random()
                self.game.audio.PlayBearNoise(distance)

        else:
            self.vel_x = 0
            self.vel_y = 0

        # call the game object's update method (applies our velocity)
        super().Update()

        # check this enemy against the player
        if CheckObjectCollision( self, self.game.player):
            # this will actually kill the player but for now just push them away
            Reposition( self, self.game.player )
            self.sprite.PlayAnimation(1)
            self.game.player.Destroy()

        # check each enemy against each other enemy
        for other_enemy in self.game.collision_layers[GameObject.ENEMY]:
            if other_enemy is self:
                continue
            if CheckObjectCollision( self, other_enemy ):
                Reposition(other_enemy,self)

        # check the bear against trees
        for tree in self.game.collision_layers[GameObject.STATIC]:
            if CheckObjectCollision( self, tree ):
                tree.Destroy()
                self.game.ExplodeObject(tree)
                self.game.audio.PlayTreeExplosion(distance)

        # Check if this enemy was hit with a bullet
        for bullet in self.game.collision_layers[GameObject.BULLET]:
            if CheckObjectCollision( self, bullet ):
                theta = GetAngle(bullet.x-self.x,bullet.y-self.y)
                speed = math.sqrt( bullet.vel_x**2 + bullet.vel_y**2 )
                bullet.vel_x = math.cos(theta) * speed
                bullet.vel_y = math.sin(theta) * speed
                Reposition(bullet,self)
                bullet.RotateBasedOnVelocity()
                # self.Destroy()
                # bullet.Destroy()
                # play the enemy death
                # PlaySound(enemy_death_sfx)
                break

