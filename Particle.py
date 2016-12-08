
import GameObject
import pygame
import random
import math
from Utilities import RandomColorFromSurface
import Bomb

SPEED = 3

class ParticleSystem(object):
    def __init__(self,game):
        self.game = game
        self.pool = []

        self.enemy_colors = [(178,14,2),
                             (178,14,2),
                             (178,14,2),
                             (178,14,2),
                             (255,71,58),
                             (255,47,33),
                             (0,178,73),
                             (33,255,123),]

        self.bomb_colors = [(250,95,28),
                            (250,95,28),
                            (250,95,28),
                            (250,95,28),
                            (250,95,28),
                            (247,223,91),
                            (247,223,91),
                            (247,223,91),
                            (52,46,46),]
    
        pass

    # def CreateNew(self,x,y,size):
    #     for i in range( 10 ):
    #         particle = self.GetParticle()
    #         vel_x = random.random()*HOR_SPEED*2.0 - HOR_SPEED
    #         vel_y = random.random()*VERT_SPEED*2.0 - VERT_SPEED
    #         particle.Set(x,y,vel_x,vel_y,(225,0,0),10,0.6)
    #         self.game.AddObject(particle)

    def EnemyExplode(self,x,y,size):
        # the number of particles is based on the radius of the circle
        num_part = math.ceil(math.pi * size **2 * 0.01)
        for i in range( num_part ):
            particle = self.GetParticle()
            r = random.random() * size
            theta = random.random() * math.pi * 2.0
            part_x = x + math.cos(theta) * r
            part_y = y + math.sin(theta) * r
            vel_x = random.random()*math.cos(theta)*SPEED
            vel_y = random.random()*math.sin(theta)*SPEED
            color = random.choice( self.enemy_colors )
            size = random.randint(5,20)
            particle.Set(part_x,part_y,vel_x,vel_y,color,size,0.6)
            self.game.AddObject(particle)

    def TreeExplode(self,tree_object):
        # the number of particles is based on the radius of the circle
        num_part = math.ceil(math.pi * tree_object.radius **2 * 0.007)
        for i in range( num_part ):
            particle = self.GetParticle()
            r = random.random() * tree_object.radius
            theta = random.random() * math.pi * 2.0
            part_x = tree_object.x + math.cos(theta) * r
            part_y = tree_object.y + math.sin(theta) * r
            vel_x = random.random()*math.cos(theta)*SPEED
            vel_y = random.random()*math.sin(theta)*SPEED
            color = RandomColorFromSurface(tree_object.sprite)
            while color[3] == 0:
                color = RandomColorFromSurface(tree_object.sprite)
            size = random.randint(5,20)
            particle.Set(part_x,part_y,vel_x,vel_y,color,size,0.6)
            self.game.AddObject(particle)

    def BombExplode(self,x,y):
        # the number of particles is based on the radius of the circle
        num_part = math.ceil(math.pi * Bomb.SIZE **2 * 0.003)
        for i in range( num_part ):
            particle = self.GetParticle()
            r = random.random() * Bomb.SIZE
            theta = random.random() * math.pi * 2.0
            part_x = x + math.cos(theta) * r
            part_y = y + math.sin(theta) * r
            vel_x = random.random()*math.cos(theta)*SPEED
            vel_y = random.random()*math.sin(theta)*SPEED
            color = random.choice( self.bomb_colors )
            size = random.randint(5,20)
            particle.Set(part_x,part_y,vel_x,vel_y,color,size,0.6)
            self.game.AddObject(particle)

    def GetParticle(self):
        # try to recycle old particles
        if len(self.pool) is 0:
            # or just create a new one
            return Particle(self.game, self)
        return self.pool.pop()

class Particle(GameObject.GameObject):
    def __init__(self, game, system):
        #override/extend the original constructor
        super().__init__(game)# call the original constructor
        self.system = system
        self.color = (225,0,0)
        self.radius = self.start_radius = 10
        self.life = self.start_life = 6.0

    def Set(self,x,y,vel_x,vel_y,color,radius,life):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.start_radius = radius
        self.dead = False
        self.life = self.start_life = life

    def Draw(self):
        pygame.draw.circle(self.game.screen, self.color, (
            int(self.x + self.game.world_x),
            int(self.y + self.game.world_y ) ),
            int(self.radius) )

    def Update(self):
        # override the original GameObject.Update method
        # call the game object's update method (applies our velocity)
        super().Update()

        self.life -= self.game.delta_time

        if self.life <= 0.0:
            self.Destroy()
            return

        self.radius = self.start_radius*(self.life/self.start_life)

    def Destroy(self):
        self.dead = True
        self.game.game_objects.remove(self)
        # recycle the particle into the particle pool
        self.system.pool.append(self)
