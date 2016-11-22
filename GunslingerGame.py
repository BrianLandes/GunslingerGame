
# Brian Landes
# Final Project

import pygame, sys
from pygame.locals import *
import math
import random
import time
from GameAudio import GameAudio
from GameObject import GameObject
import GameObject
# from GameObject import Tree
from Enemy import Enemy
from Bear import Bear
from Explosion import Explosion
from Weapon import Weapon
import Player
from Utilities import GetDistance
from LevelGenerator import LevelGenerator
from EnemyGenerator import EnemyGenerator
from CoinGenerator import CoinGenerator
from TreeList import TreeList


############
# lay out some constants here
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

TARGET_FPS = 55

POINT_FONT = "fonts/LinBiolinum_RBah.ttf"
POINTS_HEIGHT = int(SCREEN_HEIGHT*0.05)
POINTS_COLOR = (0,0,0)

###########
# initialization
pygame.init()

POINT_FONT = "fonts/LinBiolinum_RBah.ttf"
pointFont = pygame.font.Font(POINT_FONT, 96)
POINTS_HEIGHT = int(SCREEN_HEIGHT*0.05)
POINTS_COLOR = (0,0,0)

class Game(object):
    def __init__(self):

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.playing = True
        self.audio = GameAudio()

        self.pointFont = pygame.font.Font(POINT_FONT, 96)

        self.game_objects = []

        self.score = 0

        # Camera
        self.world_x = 0
        self.world_y = 0

        # Player
        self.player = Player.Player(self) # gotta pass it a reference to the Game class

        self.game_objects.append(self.player)
        self.weapon = Weapon(self)

        # Level
        self.level = LevelGenerator(self)

        for i in range(5):
            tree = GameObject.Tree(self)
            tree.x = SCREEN_WIDTH * random.random()
            tree.y = SCREEN_HEIGHT * random.random()
            self.game_objects.append(tree)

        # Enemies
        self.enemy_generator = EnemyGenerator(self)

        bear = Bear(self)
        bear.x = -100
        bear.y = -100
        self.AddObject(bear)

        # Coin Generator
        self.coin_generator = CoinGenerator(self)

        # for i in range(10):
        #     enemy = Enemy(self)
        #     enemy.x = SCREEN_WIDTH * random.random()
        #     enemy.y = SCREEN_HEIGHT * random.random()
        #     self.game_objects.append(enemy)

        # Running measurements
        self.last_time = time.time()
        self.delta_time = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.score = 0

        # layers for collision detection
        self.collision_layers = {}

    def AddObject(self,game_object):
        self.game_objects.append(game_object)

    def DestroyObject(self, game_object):
        game_object.dead = True
        self.game_objects.remove(game_object)

    def DisplayPoints(self):
        pointText = pointFont.render('$'+str(self.score), True, POINTS_COLOR, None)
        TX, TY = pointText.get_size()
        textWidth = int(POINTS_HEIGHT * (TX / TY))
        pointText = pygame.transform.scale(pointText, (textWidth, POINTS_HEIGHT))
        x = int(SCREEN_WIDTH * 0.95 - textWidth)
        y = int(SCREEN_HEIGHT * 0.97 - POINTS_HEIGHT)
        self.screen.blit(pointText, (x, y))

    def AddPoints(self, value):
        self.score += value
        if self.score >= self.weapon.next_upgrade:
            self.weapon.UpgradeWeapon()

    def ExplodeObject(self, game_object):
        # create an explosion on top of the given game_object
        explosion = Explosion(self, game_object.radius*2)
        explosion.x = game_object.x
        explosion.y = game_object.y
        self.AddObject(explosion)

    def Play(self):
        while self.playing:
            # lets keep track of how much time has passed between the last frame and this one
            current_time = time.time()
            self.delta_time = current_time - self.last_time
            # if are game is running faster than our target FPS then pause for a tick
            if self.delta_time < 1/TARGET_FPS:
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

            # store the mouse pos for easy getting
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

            # Check for key presses and update the player's velocity
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP] or pressed[pygame.K_w]:
                self.player.vel_y = -Player.PLAYER_MOVE_SPEED
            elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
                self.player.vel_y = Player.PLAYER_MOVE_SPEED
            else:
                self.player.vel_y = 0

            if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
                self.player.vel_x = -Player.PLAYER_MOVE_SPEED
            elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                self.player.vel_x = Player.PLAYER_MOVE_SPEED
            else:
                self.player.vel_x = 0

            ###########
            # Update game objects

            # update the weapon (fire bullets)
            self.weapon.Update()

            # update the level
            self.level.Update()

            # spawn more enemies sometimes
            self.enemy_generator.Update()

            self.coin_generator.Update()

            # clear the collision layers
            # (we really only need to do this if objects have been added or removed since the last time)
            for flag in GameObject.COL_FLAGS:
                self.collision_layers[flag] = []
            # iterate through all our game objects and add them to any layers they apply to
            for game_object in self.game_objects:
                # go through each (if any) collision flags there are for this item
                for key, value in game_object.collision_flags.items():
                    # the key will be the collision flag
                    # the value will be a bool for if it applies to this layer
                    if value:
                        # add it to the collision layer
                        self.collision_layers[key].append( game_object )

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

            # sort the objects
            object_sort_tree = TreeList()
            # just by putting them into the TreeList one by one we'll get them in ascending order
            for game_object in self.game_objects:
                # sorted by they're y position
                # that way when we draw them from highest on the screen to the lowest on the screen
                # the ones below (and in front) will be drawn on top
                object_sort_tree.Put(game_object.y + game_object.radius*0.5, game_object)
            # draw the game objects
            for game_object in object_sort_tree.ToList():
                game_object.Draw()

            self.DisplayPoints()

            # display what we've drawn to the screen
            pygame.display.flip()

            #########
            # finalize
            # save the current time as our last time
            self.last_time = current_time

if __name__ == '__main__':
    game = Game()
    game.Play()
