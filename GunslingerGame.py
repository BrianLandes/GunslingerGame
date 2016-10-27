
# Brian Landes
# Final Project

import pygame, sys
import math
import random
import time
from GameAudio import GameAudio
from GameObject import GameObject
from Weapon import Weapon



############
# lay out some constants here
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

POINT_FONT = "fonts/LinBiolinum_RBah.ttf"
POINTS_HEIGHT = int(SCREEN_HEIGHT*0.05)
POINTS_COLOR = (0,0,0)

PLAYER_MOVE_SPEED = 5
PLAYER_RADIUS = 25


###########
# initialization
pygame.init()



class Game(object):
    def __init__(self):

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.playing = True
        self.audio = GameAudio()

        self.pointFont = pygame.font.Font(POINT_FONT, 96)

        self.gameobjects = []

        # Camera
        self.world_x = 0
        self.world_y = 0

        # Player
        self.player = GameObject(self) # gotta pass it a reference to the Game class
        self.player.radius = PLAYER_RADIUS
        self.player.x = SCREEN_WIDTH * 0.5
        self.player.y = SCREEN_HEIGHT * 0.5
        self.player.vel_x = 0
        self.player.vel_y = 0
        self.player.color = (25, 100, 250)
        self.weapon = Weapon()

        # Running measurements
        self.last_time = time.time()
        self.mouse_x = 0
        self.mouse_y = 0
        self.score = 0

if __name__ == '__main__':
    game = Game()