
# Brian Landes
# Final Project

import pygame, sys
import random

############
# lay out some constants here
NUM_SOUND_CHANNELS =32 # the max number of sound fx that can be playing at once

###########
# initialization
pygame.mixer.pre_init()
pygame.mixer.init()
pygame.mixer.set_num_channels(NUM_SOUND_CHANNELS)

### use this to hard code mute the audio
mute_audio = False

class GameAudio(object):
    def __init__(self):
        self.sound_channels = []

        # load some sounds
        self.gunshot_sfx= []
        for i in range(1,6):
            self.gunshot_sfx.append( pygame.mixer.Sound('gunshot0' + str(i) + '_sfx.wav') )
            self.gunshot_sfx[-1].set_volume(0.2)

        self.enemy_death_sfx= []
        for i in range(1,4):
            self.enemy_death_sfx.append( pygame.mixer.Sound(
                'enemy_death_0' + str(i) + '_sfx.wav') )

        # self.music_track = pygame.mixer.music.load(
        #     '155139__burning-mir__action-music-loop-with-dark-ambient-drones.wav')
        # pygame.mixer.music.play(loops = -1 )

    def PlaySound(self,sound_fx_list):
        # given a list of similar sound effects, choose a random one
        sound_fx = sound_fx_list[random.randint(0, len(sound_fx_list) - 1)]
        if mute_audio:
            return
        # we can only play a certain number of sound fx at one time
        # max is NUM_SOUND_CHANNELS
        # if we go to play another sound and all the channels are busy
        # lets just cut 1 and play our sound since its probably almost done anyways
        # and the player won't notice over a dozen other sounds
        # free up our list of any not playing channels
        temp_ls = self.sound_channels.copy()
        for channel in temp_ls:
            if channel is None or not channel.get_busy():
                # print( 'dropping channel' )
                self.sound_channels.remove(channel)

        # print( len(channels) )

        if len(self.sound_channels) >= NUM_SOUND_CHANNELS:
            # we already have NUM_SOUND_CHANNELS sounds playing so we need to stop one
            # might as well be the first one in our list
            self.sound_channels[0].stop
            self.sound_channels[0].play(sound_fx)
        else:

            self.sound_channels.append(sound_fx.play())