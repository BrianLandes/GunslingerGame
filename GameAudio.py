
# Brian Landes
# Final Project

import pygame, sys, os
import random
import time

############
# lay out some constants here
NUM_SOUND_CHANNELS =32 # the max number of sound fx that can be playing at once

###########
# initialization
pygame.mixer.pre_init()
pygame.mixer.init()
pygame.mixer.set_num_channels(NUM_SOUND_CHANNELS)

### use this to hard code mute the audio
MUTE_AUDIO = False

MAX_DISTANCE = 800

## adjust volumes
GUNSHOT_VOLUME = 0.9
# enemy_death_volume = 0.9
# tree_explosion_volume = 0.9
# music_volume = 0.5

class GameAudio(object):
    def __init__(self):
        self.sound_channels = []

        # load some sounds
        # for the gunshots sfx we'll just load everything in the audio/gunshots folder
        self.gunshot_sfx= []
        for folderName, subfolders, filenames in os.walk('audio/gunshots'):
            # for each file we find in this folder
            for filename in filenames:
                #load a sound object and add it to our sfx list
                sound = pygame.mixer.Sound('audio/gunshots/'+filename)
                # adjust the volume
                # sound.set_volume(gunshot_volume)
                self.gunshot_sfx.append( sound )

        self.gunshot_volume = GUNSHOT_VOLUME
        self.last_gunshot = time.time()


        self.enemy_death_sfx= []
        for folderName, subfolders, filenames in os.walk('audio/enemy_death'):
            # for each file we find in this folder
            for filename in filenames:
                #load a sound object and add it to our sfx list
                sound = pygame.mixer.Sound('audio/enemy_death/'+filename)
                # adjust the volume
                # sound.set_volume(enemy_death_volume)
                self.enemy_death_sfx.append( sound )

        self.tree_explosion_sfx= []
        for folderName, subfolders, filenames in os.walk('audio/tree_explosion'):
            # for each file we find in this folder
            for filename in filenames:
                #load a sound object and add it to our sfx list
                sound = pygame.mixer.Sound('audio/tree_explosion/'+filename)
                # adjust the volume
                # sound.set_volume(tree_explosion_volume)
                self.tree_explosion_sfx.append( sound )

        self.coin_sfx= []
        for folderName, subfolders, filenames in os.walk('audio/coins'):
            # for each file we find in this folder
            for filename in filenames:
                #load a sound object and add it to our sfx list
                sound = pygame.mixer.Sound('audio/coins/'+filename)
                # adjust the volume
                # sound.set_volume(tree_explosion_volume)
                self.coin_sfx.append( sound )

        self.bear_sfx= []
        for folderName, subfolders, filenames in os.walk('audio/bear'):
            # for each file we find in this folder
            for filename in filenames:
                #load a sound object and add it to our sfx list
                sound = pygame.mixer.Sound('audio/bear/'+filename)
                # adjust the volume
                # sound.set_volume(tree_explosion_volume)
                self.bear_sfx.append( sound )

        # self.music_track = pygame.mixer.music.load(
        #     '155139__burning-mir__action-music-loop-with-dark-ambient-drones.wav')
        # pygame.mixer.music.play(loops = -1 )

    def PlaySound(self,sound_fx_list, distance = None, volume = None):
        # given a list of similar sound effects, choose a random one
        sound_fx = sound_fx_list[random.randint(0, len(sound_fx_list) - 1)]
        if MUTE_AUDIO:
            return
        # # we can only play a certain number of sound fx at one time
        # # max is NUM_SOUND_CHANNELS
        # # if we go to play another sound and all the channels are busy
        # # lets just cut 1 and play our sound since its probably almost done anyways
        # # and the player won't notice over a dozen other sounds
        # # free up our list of any not playing channels
        # temp_ls = self.sound_channels.copy()
        # for channel in temp_ls:
        #     if channel is None or not channel.get_busy():
        #         # print( 'dropping channel' )
        #         self.sound_channels.remove(channel)

        # print( len(channels) )

        if distance is not None:
            sound_fx.set_volume((MAX_DISTANCE - distance) / MAX_DISTANCE)

        if volume is not None:
            # setting volume will override the distance
            sound_fx.set_volume( volume )

        sound_fx.play()

        # if len(self.sound_channels) >= NUM_SOUND_CHANNELS:
        #     # we already have NUM_SOUND_CHANNELS sounds playing so we need to stop one
        #     # might as well be the first one in our list
        #     self.sound_channels[0].stop
        #     self.sound_channels[0].play(sound_fx)
        # else:
        #
        #     self.sound_channels.append(sound_fx.play())

    def PlayGunshot(self):
        gunshot_time = time.time()
        # how much time has passed since the last gunshot?
        difference = gunshot_time - self.last_gunshot
        # if the last one was within a small period of time

        if difference < 0.3:

            # adjust our gunshot volume (so that new ones are quieter)
            self.gunshot_volume -= 0.08
            # but don't let it get too low
            if self.gunshot_volume <= 0.3:
                self.gunshot_volume = 0.3
        else:
            self.gunshot_volume = GUNSHOT_VOLUME


        # print( self.gunshot_volume)
        self.PlaySound(self.gunshot_sfx, volume = self.gunshot_volume )

        self.last_gunshot = gunshot_time

    def PlayEnemyDeath(self, distance):
        self.PlaySound(self.enemy_death_sfx, distance)

    def PlayTreeExplosion(self, distance):
        self.PlaySound(self.tree_explosion_sfx, distance)

    def PlayBearNoise(self, distance):
        self.PlaySound(self.bear_sfx, distance)

    def PlayCoin(self ):
        self.PlaySound(self.coin_sfx )