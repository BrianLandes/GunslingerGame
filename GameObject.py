
# Brian Landes
# Final Project
# Game Object class

import pygame, sys

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

    def Draw(self):
        pygame.draw.circle(self.game.screen, self.color, (
            int(self.x + self.game.world_x),
            int(self.y + self.game.world_y ) ),
            int(self.radius) )

    def UpdatePosition(self):
        self.x += self.vel_x
        self.y += self.vel_y
                    
    def Destroy(self):
        self.dead = True


treeSprite = pygame.image.load('tree_sprite.png')

class Tree(GameObject):
    def __init__(self):
        self.sprite = treeSprite

    def Draw(self):
        pass
        
