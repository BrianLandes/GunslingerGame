
# Brian Landes
# Final Project
# October 29, 2016

# loads an image and slices it in a grid for sprites and animations

import pygame, sys
import time

class SpriteSheet(object):
    def __init__(self, filename, dimensions = None):
        self.filename = filename
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.dimensions = dimensions # a 2D tuple for columns X rows
        self.sprites = []
        if dimensions is not None:
            self.Slice(dimensions)

    def Slice(self,dimensions):
        self.sprites = []
        self.dimensions = dimensions # a 2D tuple for columns X rows
        columns = dimensions[0]
        rows = dimensions[1]
        cell_width = self.sheet.get_width() / columns
        cell_height = self.sheet.get_height() / rows
        for r in range(rows):
            for c in range(columns):

                rect = pygame.Rect(c * cell_width, r * cell_height, cell_width, cell_height)
                self.sheet.set_clip(rect)
                new_sprite = self.sheet.subsurface(self.sheet.get_clip() )
                self.sprites.append(new_sprite)

    def GetSpriteSize(self):
        width, height = self.sheet.get_size()
        return width/self.dimensions[0],height/self.dimensions[1]

    def GetSprite(self,x,y):
        # where (0,0) is the top-left sprite
        columns = self.dimensions[0]
        return self.sprites[ x + y * columns]

    def Resize(self,sprite_width,sprite_height):
        sheet_width = sprite_width * self.dimensions[0]
        sheet_height = sprite_height * self.dimensions[1]
        # reload the original image to preserve integrity
        # self.sheet = pygame.image.load(self.filename).convert_alpha()
        self.sheet = pygame.transform.scale( self.sheet, (sheet_width,sheet_height))
        self.Slice(self.dimensions)

    def Flip(self,xbool,ybool):
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.flip(self.sprites[i],xbool,ybool)

FRAME_RATE = 6 # X frames per second

class Animation(object):
    def __init__(self ):
        self.frames = []
        self.loop = True

    def AddFrame(self, sprite_x, sprite_y, frame_time = 1/FRAME_RATE, callback = None ):
        self.frames.append( (sprite_x, sprite_y, frame_time, callback) )

class SpriteAnimator(object):
    def __init__(self, filename, dimensions):
        self.sheet = SpriteSheet(filename,dimensions)

        self.animations = []
        self.animation_index = 0
        self.frame_index = 0
        self.frame_timer = 0.0
        self.last_time = time.time()
        self.stopped = False

    def AddAnimation(self, animation):
        self.animations.append(animation)

    def PlayAnimation(self,index):
        self.animation_index = index
        self.frame_index = 0
        self.frame_timer = 0

    def GetSpriteSize(self):
        return self.sheet.GetSpriteSize()

    def UpdateAndDraw(self, surface, x, y ):
        if self.stopped:
            return
        current_time = time.time()
        delta_time = current_time - self.last_time
        animation = self.animations[self.animation_index]
        sprite_x, sprite_y, frame_time, callback = animation.frames[self.frame_index]

        sprite = self.sheet.GetSprite(sprite_x, sprite_y)

        surface.blit(sprite, (x,y) )

        self.frame_timer += delta_time
        if self.frame_timer > frame_time:
            self.frame_timer = 0
            self.frame_index +=1
            if self.frame_index >= len(animation.frames):
                if animation.loop:
                    self.frame_index = 0
                else:
                    self.stopped = True

            if animation.frames[self.frame_index][3] is not None:
                animation.frames[self.frame_index][3]()

        self.last_time = current_time

    def Draw(self, surface, x, y ):
        if self.stopped:
            return

        animation = self.animations[self.animation_index]
        sprite_x, sprite_y, frame_time, callback = animation.frames[self.frame_index]

        sprite = self.sheet.GetSprite(sprite_x, sprite_y)

        surface.blit(sprite, (x,y) )

    def Resize(self,sprite_width,sprite_height):
        self.sheet.Resize(sprite_width,sprite_height)

    def Flip(self,xbool,ybool):
        self.sheet.Flip(xbool,ybool)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600),pygame.SRCALPHA, 32)
    spritesheet = SpriteSheet('ground_texture.png', (3,2) )
    enemys_sprite = SpriteAnimator('enemy_spritesheet.png', (3,2) )
    enemys_sprite.AddFrame(0,0)
    enemys_sprite.AddFrame(1,0)
    enemys_sprite.AddFrame(2,0)
    enemys_sprite.AddFrame(0,1)
    enemys_sprite.AddFrame(1,1 )

    enemy_x = 500

    while True:
        for event in pygame.event.get():
            # if the app is quit then break and close
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((220, 220, 200))

        for c in range(3):
            for r in range(2):
                screen.blit(spritesheet.GetSprite(c,r), ( 100*c,100*r ) )

        enemys_sprite.UpdateAndDraw( screen, int(enemy_x), 300 )
        enemy_x -= 0.01

        pygame.display.flip()
