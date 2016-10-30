
# Brian Landes
# Final Project

# Handles the floor/background layer of the game
# Uses 4 window sized surfaces to draw the ground

import pygame,os,random
import GunslingerGame

# sprites for the ground
ground_sprites = []
for folderName, subfolders, filenames in os.walk('sprites/ground/'):
    # for each file we find in this folder
    for filename in filenames:
        # sometimes Windows will make this file in your pictures folders and we can't load that
        if filename == 'Thumbs.db':
            # so just skip it
            continue
        #load a sprite and add it to our available sprites list
        print('sprites/ground/',filename )
        image = pygame.image.load('sprites/ground/'+filename)
        ground_sprites.append( image )

SCREEN_BUFFER_SIZE = 100 # we'll make our surfaces a little bigger han the window so we have a buffer zone

SURFACE_WIDTH = GunslingerGame.SCREEN_WIDTH + SCREEN_BUFFER_SIZE
SURFACE_HEIGHT = GunslingerGame.SCREEN_HEIGHT + SCREEN_BUFFER_SIZE

class ScrollSurface(object):
    def __init__(self, x, y):
        self.surface = pygame.Surface(SURFACE_WIDTH,SURFACE_HEIGHT)

        self.surface.blit(random.choice(ground_sprites),(0,0))

        self.x = x
        self.y = y

    def GetBounds(self):
        # returns the (left,top,right,bottom) values for this ScrollSurface
        return (
            self.x, self.y,
            self.x + self.surface.get_width(), self.y + self.surface.get_height()
        )

class FloorLayer(object):
    def __init__(self, game):
        self.game = game # a reference to the GunslingerGame class

        self.center_x = 0
        self.center_y = 0

        # we'll be pulling a little slight of hand with these surfaces
        self.surfaces = []
        for i in range(4):
            # first lets throw them down as 2x2
            x = i%2 *SURFACE_WIDTH
            y = i//2 *SURFACE_HEIGHT
            self.surfaces.append( ScrollSurface( x ,y ) )