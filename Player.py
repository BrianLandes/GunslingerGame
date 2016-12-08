
import GameObject
import random
import pygame
import pyganim
import math
from Utilities import GetAngle

PLAYER_MOVE_SPEED = 8
PLAYER_RADIUS = 25

DIAGONAL_MOD = math.sqrt(2)/2

PI_EIGHTS = math.pi * (1/8)

SPRITE_WIDTH = 70
SPRITE_H_W_RATIO = 3/2

class Player(GameObject.GameObject):
    def __init__(self, game, gender):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor

        self.color = (225,0,0)
        self.radius = PLAYER_RADIUS
        self.SetCollisionFlag( GameObject.PLAYER )
        # sprite = pygame.image.load('sprites/Cowboy.png')
        #
        # # we want to keep the original sprite's aspect ratio, but scale down to the bullet's size
        # SX, SY = sprite.get_size()
        # new_height = int(self.radius*2 * (SY/SX) )
        # self.sprite = pygame.transform.scale( sprite, (self.radius*2,new_height) ).convert_alpha()

        self.gender = gender

        self.movement_penalty = 1.0

        self.LoadSprites(gender)

    def ScaleSprite(self,path):
        sprite = pygame.image.load(path)
        width = SPRITE_WIDTH
        return pygame.transform.scale(sprite,(width,int(width*SPRITE_H_W_RATIO)))

    def LoadSprites(self,choice):
        if choice == 1:

            self.front_standing = self.ScaleSprite('sprites/player/cowboy_3.00.png')
            self.back_standing = self.ScaleSprite('sprites/player/cowboy_6.00.png')
            self.left_standing = self.ScaleSprite('sprites/player/cowboy_4.00.png')
            self.right_standing = self.ScaleSprite('sprites/player/cowboy_1.00.png')
            self.upleft_standing = self.ScaleSprite('sprites/player/cowboy_5.00.png')
            self.upright_standing = self.ScaleSprite('sprites/player/cowboy_2.00.png')
            self.downleft_standing = pygame.image.load('sprites/player/cowboy_8.00.png')
            self.downright_standing = pygame.image.load('sprites/player/cowboy_7.00.png')

            animTypes = '6 3 1 4 2 5 7 8'.split()
            self.animObjs = {}

            for animType in animTypes:
                imagesAndDurations = [('sprites/player/cowboy_%s.%s.png' % (animType, str(num).rjust(2, '0')), 0.1) for num in range(4)]
                self.animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)
            ##cowboy walk animation

        elif choice == 2:
            self.front_standing = self.ScaleSprite('sprites/player/cowgirl_3.00.png')
            self.back_standing = self.ScaleSprite('sprites/player/cowgirl_6.00.png')
            self.left_standing = self.ScaleSprite('sprites/player/cowgirl_4.00.png')
            self.right_standing = self.ScaleSprite('sprites/player/cowgirl_1.00.png')
            self.upleft_standing = self.ScaleSprite('sprites/player/cowgirl_8.00.png')
            self.upright_standing = self.ScaleSprite('sprites/player/cowgirl_7.00.png')
            self.downleft_standing = self.ScaleSprite('sprites/player/cowgirl_5.00.png')
            self.downright_standing = self.ScaleSprite('sprites/player/cowgirl_2.00.png')

            animTypes = '6 3 1 4 2 5 7 8'.split()
            self.animObjs = {}

            for animType in animTypes:
                    imagesAndDurations = [('sprites/player/cowgirl_%s.%s.png' % (animType, str(num).rjust(2, '0')), 0.1) for num in range(4)]
                    self.animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)
            ##cowgirl walk animation

        self.moveConductor = pyganim.PygConductor(self.animObjs)
        self.moveConductor.scale((SPRITE_WIDTH,int(SPRITE_WIDTH*SPRITE_H_W_RATIO)))

    def Draw(self):
        # override the original GameObject.Update method
        # our (x,y) is the center, but it blits to the top right
        x = int(self.x + self.game.world_x - SPRITE_WIDTH*0.5)
        y = int(self.y + self.game.world_y - SPRITE_WIDTH*SPRITE_H_W_RATIO*0.75 )
        moving = (self.vel_x**2 + self.vel_y**2) > 0.0001
        # theta = math.degrees( -GetAngle(self.game.mouse_x -x, self.game.mouse_y -y) -math.pi*0.5 )
        theta = GetAngle(self.game.mouse_x -x, self.game.mouse_y -y)

        if moving:
            # draw the correct walking/running sprite from the animation object
            self.moveConductor.play() # calling play() while the animation objects are already playing is okay; in that case play() is a no-op
                # walking
            if -5*PI_EIGHTS < theta < -3*PI_EIGHTS: # UP
                self.animObjs['3'].blit(self.game.screen, (x, y))
            elif -7*PI_EIGHTS < theta < -5*PI_EIGHTS: # UP LEFT
                self.animObjs['2'].blit(self.game.screen, (x, y))
            elif theta < -7*PI_EIGHTS or theta > 7*PI_EIGHTS: # LEFT
                self.animObjs['1'].blit(self.game.screen, (x, y))
            elif theta > 5*PI_EIGHTS: # DOWN LEFT
                self.animObjs['7'].blit(self.game.screen, (x, y))
            elif theta > 3*PI_EIGHTS: # DOWN
                self.animObjs['6'].blit(self.game.screen, (x, y))
            elif theta > 1*PI_EIGHTS: #DOWN RIGHT
                self.animObjs['8'].blit(self.game.screen, (x, y))
            elif theta > -1*PI_EIGHTS: # RIGHT
                self.animObjs['4'].blit(self.game.screen, (x, y))
            else: # UP RIGHT
                self.animObjs['5'].blit(self.game.screen, (x, y))
        else:

            # standing still
            self.moveConductor.stop() # calling stop() while the animation objects are already stopped is okay; in that case stop() is a no-op
            if -5*PI_EIGHTS < theta < -3*PI_EIGHTS:
                self.game.screen.blit(self.front_standing, (x, y))
            elif -7*PI_EIGHTS < theta < -5*PI_EIGHTS:
                self.game.screen.blit(self.downright_standing, (x, y))
            elif theta < -7*PI_EIGHTS or theta > 7*PI_EIGHTS:
                self.game.screen.blit(self.right_standing, (x, y))
            elif theta > 5*PI_EIGHTS:
                self.game.screen.blit(self.upright_standing, (x, y))
            elif theta > 3*PI_EIGHTS:
                self.game.screen.blit(self.back_standing, (x, y))
            elif theta > 1*PI_EIGHTS:
                self.game.screen.blit(self.upleft_standing, (x, y))
            elif theta > -1*PI_EIGHTS:
                self.game.screen.blit(self.left_standing, (x, y))
            else:
                self.game.screen.blit(self.downleft_standing, (x, y))


    def Update(self):

        movespeed = PLAYER_MOVE_SPEED * self.movement_penalty

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.vel_y = -movespeed
        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.vel_y = movespeed
        else:
            self.vel_y = 0

        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.vel_x = -movespeed
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.vel_x = movespeed
        else:
            self.vel_x = 0

        # if the player is moving diagonally, reduce the speed so its only as fast as moving in one direction
        if abs(self.vel_x) + abs(self.vel_y) > PLAYER_MOVE_SPEED:
            self.vel_x *= DIAGONAL_MOD
            self.vel_y *= DIAGONAL_MOD





        # override the original GameObject.Update method
        # call the game object's update method (applies our velocity)
        super().Update()

        self.movement_penalty = 1.0

    # def RotateBasedOnVelocity(self):
    #     # modifies the sprite of this game object -> sets rotation based on the velocity
    #     # assumes that this is the first and only time the rotation will be changed
    #     # (since the rotate transformation is destructive and we're not keeping track of what we've rotated)
    #     theta = math.degrees( -GetAngle(self.vel_x,self.vel_y) )
    #     self.sprite = pygame.transform.rotate(self.sprite, theta)