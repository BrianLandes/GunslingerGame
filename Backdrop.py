
import pygame

# handles the drawing of the ground layer / backdrop layer

image_path = 'sprites/ground/ground_backdrop.png'

class Backdrop(object):
    def __init__(self, game):
        # handle to the Gunslinger Game class
        self.game = game

        self.image = pygame.image.load(image_path).convert_alpha()
        self.iw , self.ih= self.image.get_size()
    def Draw(self):
        self.game.screen.blit(self.image, (self.game.world_x%self.iw,self.game.world_y%self.ih) )
        self.game.screen.blit(self.image, (self.game.world_x%self.iw - self.iw,self.game.world_y%self.ih) )
        self.game.screen.blit(self.image, (self.game.world_x%self.iw,self.game.world_y%self.ih - self.ih) )
        self.game.screen.blit(self.image, (self.game.world_x%self.iw - self.iw,self.game.world_y%self.ih - self.ih) )
