
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

def LoadAllFilesInFolder(path):
    results = []
    for folderName, subfolders, filenames in os.walk(path):
        # for each file we find in this folder
        for filename in filenames:
            #load a sound object and add it to our sfx list
            sound = pygame.mixer.Sound(path+filename)
            results.append( sound )

    return results

class GameAudio(object):
    def __init__(self):
        self.sound_channels = []

        # load some sounds
        # for the gunshots sfx we'll just load everything in the audio/gunshots folder
        self.gunshot_sfx= LoadAllFilesInFolder('audio/gunshots/')
        self.gunshot_volume = GUNSHOT_VOLUME
        self.last_gunshot = time.time()

        self.enemy_death_sfx= LoadAllFilesInFolder('audio/enemy_death/')

        self.tree_explosion_sfx= LoadAllFilesInFolder('audio/tree_explosion/')

        self.coin_sfx= LoadAllFilesInFolder('audio/coins/')

        self.bear_sfx = LoadAllFilesInFolder('audio/bear/')

        self.smash_sfx = LoadAllFilesInFolder('audio/smash/')

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

    def PlaySmash(self ):
        self.PlaySound(self.smash_sfx )