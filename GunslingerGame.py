
# Brian Landes
# Final Project

import pygame, sys
from pygame.locals import *
import math
import random
import time
from GameAudio import GameAudio
from GameObject import GameObject
from Weapon import Weapon
from Utilities import GetDistance


############
# lay out some constants here
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

TARGET_FPS = 60

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

        self.game_objects = []

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
        self.game_objects.append(self.player)
        self.weapon = Weapon()

        # Running measurements
        self.last_time = time.time()
        self.mouse_x = 0
        self.mouse_y = 0
        self.score = 0

    def DestroyObject(self, game_object):
        game_object.dead = True
        self.game_objects.remove(game_object)

    def Play(self):
        while self.playing:
            # lets keep track of how much time has passed between the last frame and this one
            current_time = time.time()
            delta_time = current_time - self.last_time
            # if are game is running faster than our target FPS then pause for a tick
            if delta_time < 1/TARGET_FPS:
                continue

            #########
            # Handle events
            for event in pygame.event.get():
                # if the app is quit then break and close
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.quit()
                    sys.exit()

                # if the player is holding the left mouse button then fire some bullets
                if event.type == pygame.MOUSEBUTTONDOWN and event.button is 1:
                    self.weapon.firing = True
                if event.type == pygame.MOUSEBUTTONUP and event.button is 1:
                    self.weapon.firing = False

            # Check for key presses and update the player's velocity
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP] or pressed[pygame.K_w]:
                self.player.vel_y = -PLAYER_MOVE_SPEED
            elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
                self.player.vel_y = PLAYER_MOVE_SPEED
            else:
                self.player.vel_y = 0

            if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
                self.player.vel_x = -PLAYER_MOVE_SPEED
            elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                self.player.vel_x = PLAYER_MOVE_SPEED
            else:
                self.player.vel_x = 0

            ###########
            # Update game objects
            # we'll copy the game object list and iterate through the copy so that
            # we can remove dead elements from the original without getting tripped up
            object_list = self.game_objects.copy()
            for game_object in object_list:
                # we'll let each game object handle their own update
                # mostly they'll just check whether or not they're dead but sometimes they'll do collision detection
                game_object.Update()

            # since the camera follows the player just set the world origin to the player's position
            self.world_x = int(-self.player.x + SCREEN_WIDTH * 0.5)
            self.world_y = int(-self.player.y + SCREEN_HEIGHT * 0.5)

            #########
            # draw
            # clear the screen
            self.screen.fill((220, 220, 200))
            # draw the game objects
            for game_object in self.game_objects:
                game_object.Draw()

            # display what we've drawn to the screen
            pygame.display.flip()

            #########
            # finalize
            # save the current time as our last time
            self.last_time = current_time

if __name__ == '__main__':
    game = Game()
    game.Play()