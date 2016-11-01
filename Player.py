
import GameObject
import random
import pygame
import math
from Utilities import GetAngle

PLAYER_MOVE_SPEED = 10
PLAYER_RADIUS = 25

DIAGONAL_MOD = math.sqrt(2)/2

class Player(GameObject.GameObject):
    def __init__(self, game):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor

        self.color = (225,0,0)
        self.radius = PLAYER_RADIUS
        self.SetCollisionFlag( GameObject.PLAYER )
        sprite = pygame.image.load('sprites/Cowboy.png')

        # we want to keep the original sprite's aspect ratio, but scale down to the bullet's size
        SX, SY = sprite.get_size()
        new_height = int(self.radius*2 * (SY/SX) )
        self.sprite = pygame.transform.scale( sprite, (self.radius*2,new_height) ).convert_alpha()


    def Draw(self):
        # override the original GameObject.Update method
        # our (x,y) is the center, but it blits to the top right
        x = int(self.x + self.game.world_x)
        y = int(self.y + self.game.world_y )
        theta = math.degrees( -GetAngle(self.game.mouse_x -x, self.game.mouse_y -y) -math.pi*0.5 )
        sprite = pygame.transform.rotate(self.sprite,theta)
        SX, SY = sprite.get_size()

        x = int(self.x + self.game.world_x - SX*0.5)
        y = int(self.y + self.game.world_y - SY*0.5 )
        self.game.screen.blit(sprite, ( x,y ) )

    def Update(self):
        # if the player is moving diagonally, reduce the speed so its only as fast as moving in one direction
        if abs(self.vel_x) + abs(self.vel_y) > PLAYER_MOVE_SPEED:
            self.vel_x *= DIAGONAL_MOD
            self.vel_y *= DIAGONAL_MOD





        # override the original GameObject.Update method
        # call the game object's update method (applies our velocity)
        super().Update()

    # def RotateBasedOnVelocity(self):
    #     # modifies the sprite of this game object -> sets rotation based on the velocity
    #     # assumes that this is the first and only time the rotation will be changed
    #     # (since the rotate transformation is destructive and we're not keeping track of what we've rotated)
    #     theta = math.degrees( -GetAngle(self.vel_x,self.vel_y) )
    #     self.sprite = pygame.transform.rotate(self.sprite, theta)