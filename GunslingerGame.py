
# Brian Landes
# Final Project

import pygame, sys
import random
import time
from GameAudio import GameAudio
from GameObject import GameObject
import GameObject
from Button import *
import FloatingText
from Weapon import Weapon
import Player
from LevelGenerator import LevelGenerator
from EnemyGenerator import EnemyGenerator
from CoinGenerator import CoinGenerator
from TreeList import TreeList
from Backdrop import Backdrop
from Particle import ParticleSystem
import os


############
# lay out some constants here
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

TARGET_FPS = 55

###########
# initialization
pygame.init()

POINT_FONT = "fonts/LinBiolinum_RBah.ttf"
pointFont = pygame.font.Font(POINT_FONT, 96)
POINTS_HEIGHT = int(SCREEN_HEIGHT*0.05)
POINTS_COLOR = (0,0,0)

CURSOR_SPRITE = 'sprites/target.png'

# control where the new window pops up on the screen
x = 10
y = 40
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

class Game(object):
    def __init__(self):

        # self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),FULLSCREEN)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),DOUBLEBUF)
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.dimensions = (SCREEN_WIDTH,SCREEN_HEIGHT)
        self.playing = True
        self.audio = GameAudio()

        self.pointFont = pygame.font.Font(POINT_FONT, 96)

        self.game_objects = []

        self.score = 0

        self.cursor_image = pygame.image.load(CURSOR_SPRITE).convert_alpha()
        self.cursor_dimensions = (50,50)
        self.cursor_image = pygame.transform.scale(self.cursor_image, self.cursor_dimensions )
        pygame.mouse.set_visible(False)

        # Camera
        self.world_x = 0
        self.world_y = 0

        # Background
        self.backdrop = Backdrop(self)

        # Particle system
        self.particle_system = ParticleSystem(self)

        # Player
        self.player = Player.Player(self,2) # gotta pass it a reference to the Game class

        self.bear = None

        self.game_objects.append(self.player)
        self.weapon = Weapon(self)

        # Level
        self.level = LevelGenerator(self)

        floating_text = FloatingText.New(self, (255,255,255), "Use WASD or Arrow keys",
                                SCREEN_WIDTH*0.6, SCREEN_HEIGHT*0.2,
                                         line2 = "to run around",life=6)
        # floating_text = FloatingText.FloatingText(self)
        floating_text.x = -20
        floating_text.y = -200
        self.AddObject(floating_text)

        for i in range(15):
            tree = GameObject.Tree(self)
            tree.x = SCREEN_WIDTH * random.random()
            tree.y = SCREEN_HEIGHT * random.random()
            self.game_objects.append(tree)

        # Enemies
        self.enemy_generator = EnemyGenerator(self)

        # Coin Generator
        self.coin_generator = CoinGenerator(self)

        self.again_button_style = ButtonStyle('sprites/blue_button00.png',
                                              (100,100,100),
                                              'sprites/blue_button01.png',
                                              (150,150,150),
                                              POINT_FONT,
                 vert_align = ALIGN_CENTER, hor_align = ALIGN_CENTER, border_perc = 0.25,
                 font_up_color = WHITE, font_down_color = BLACK, font_disabled_color = DARK_GREY)

        self.again_button = Button(self.screen, 'again',
                                   self.width * 0.7, self.height * 0.7,
                                   self.width * 0.2, self.height * 0.15
                                   , self.again_button_style)

        # Running measurements
        self.last_time = time.time()
        self.delta_time = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.score = 0

        # layers for collision detection
        self.collision_layers = {}

    def StartNewGame(self):
        self.ExplodeObject(self.bear)
        self.DestroyObject(self.bear)
        self.bear = None

        self.playing = True
        self.score = 0
        self.player = Player.Player(self,1)
        self.AddObject(self.player)
        self.player.x = -(self.world_x - SCREEN_WIDTH * 0.5)
        self.player.y = -(self.world_y - SCREEN_HEIGHT * 0.5)

        self.enemy_generator.Reset()
        self.coin_generator.Reset()
        self.weapon.Reset()

        pygame.mouse.set_visible(False)


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

        if game_object.IsEnemy():
            self.particle_system.EnemyExplode(game_object.x,game_object.y,game_object.radius)
        elif game_object.IsBomb():
            self.particle_system.BombExplode(game_object.x,game_object.y)
        else:
            self.particle_system.TreeExplode(game_object)

    def Play(self):
        while self.playing:
            # lets keep track of how much time has passed between the last frame and this one
            current_time = time.time()
            self.delta_time = current_time - self.last_time #should be in seconds
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

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                self.playing = False
                pygame.quit()
                sys.exit()

            # store the mouse pos for easy getting
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

            if self.mouse_x < 30:
                self.mouse_x = 30
            if self.mouse_x > SCREEN_WIDTH-30:
                self.mouse_x = SCREEN_WIDTH-30
            if self.mouse_y < 30:
                self.mouse_y = 30
            if self.mouse_y > SCREEN_HEIGHT-30:
                self.mouse_y = SCREEN_HEIGHT-30
            pygame.mouse.set_pos(self.mouse_x, self.mouse_y)

            # Check for key presses and update the player's velocity


            ###########
            # Update game objects

            # update the weapon (fire bullets)
            self.weapon.Update()

            # update the level
            self.level.Update()

            # spawn more enemies sometimes
            self.enemy_generator.Update()

            self.coin_generator.Update()

            # self.bomb_generator.Update()

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

            # draw the ground layer
            self.backdrop.Draw()

            # sort the objects
            object_sort_tree = TreeList()
            # just by putting them into the TreeList one by one we'll get them in ascending order
            for game_object in self.game_objects:
                # sorted by they're y position
                # that way when we draw them from highest on the screen to the lowest on the screen
                # the ones below (and in front) will be drawn on top
                object_sort_tree.Put(game_object.y + game_object.radius*0.5 + game_object.z, game_object)
            # draw the game objects
            for game_object in object_sort_tree.ToList():
                game_object.Draw()

            self.DisplayPoints()

            cx = int(self.mouse_x - self.cursor_dimensions[0]*0.5)
            cy = int(self.mouse_y - self.cursor_dimensions[1]*0.5)

            self.screen.blit(self.cursor_image,(cx,cy))

            if self.player.dead:
                self.again_button.Draw()
                if self.again_button.pressed:
                    self.StartNewGame()

            # display what we've drawn to the screen
            pygame.display.flip()



            #########
            # finalize
            # save the current time as our last time
            self.last_time = current_time

    def ShowMenu(self):
        pass

if __name__ == '__main__':
    game = Game()
    game.Play()
