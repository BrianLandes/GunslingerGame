
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

import math,os,pygame,random

COIN_SIZE = 30
COIN_EXPIRE_RANGE = 5000
COIN_VALUE = 10

coin_sprites = []
for folderName, subfolders, filenames in os.walk('sprites/coins/'):
    # for each file we find in this folder
    for filename in filenames:
        # sometimes Windows will make this file in your folders and we can't load that
        if filename == 'Thumbs.db':
            # so just skip it
            continue
        #load a sprite and add it to our availables sprites list
        image = pygame.image.load('sprites/coins/'+filename)
        coin_sprites.append( image )

class Coin(GameObject.GameObject):
    def __init__(self, game):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor

        self.color = (225,0,0)
        self.radius = COIN_SIZE
        self.expire_range = COIN_EXPIRE_RANGE
        self.SetCollisionFlag( GameObject.COIN )
        sprite = random.choice(coin_sprites)
        # we want to keep the original sprite's aspect ratio, but scale down to the bullet's size
        SX, SY = sprite.get_size()
        new_height = int(self.radius*2 * (SY/SX) )
        self.sprite = pygame.transform.scale( sprite, (self.radius*2,new_height) ).convert_alpha()


    def Draw(self):
        # override the original GameObject.Update method
        # our (x,y) is the center, but it blits to the top right
        x = int(self.x + self.game.world_x - self.radius)
        y = int(self.y + self.game.world_y - self.radius )
        self.game.screen.blit(self.sprite, ( x,y ) )

    def Update(self):
        # override the original GameObject.Update method
        # call the game object's update method (applies our velocity)
        super().Update()
        # check if we've touched the player
        if CheckObjectCollision(self,self.game.player):
            self.Destroy()
            # and give the player some points
            self.game.AddPoints(COIN_VALUE)
            self.game.audio.PlayCoin()


    def RotateBasedOnVelocity(self):
        # modifies the sprite of this game object -> sets rotation based on the velocity
        # assumes that this is the first and only time the rotation will be changed
        # (since the rotate transformation is destructive and we're not keeping track of what we've rotated)
        theta = math.degrees( -GetAngle(self.vel_x,self.vel_y) )
        self.sprite = pygame.transform.rotate(self.sprite, theta)