# Brian Landes
# Final Project
# Spawns obstacles as the player moves through the level
import math, random
from Utilities import Distance
from Utilities import RandomVector
from GameObject import Tree

# types of obstacle generation
SCATTER = 0 # generates obstacles randomly in the path of the player
SNAKE = 1 # generates obstacles in a winding trail along the path of the player

class LevelGenerator(object):
    def __init__(self, game):
        self.game = game # a reference to the GunslingerGame class
        self.type = SNAKE

        self.spawn_rate = 100 # distance the player must move each time we spawn
        self.scatter_angle_variance = math.pi * 0.125 # up to 45 degrees in either direction
        self.scatter_spawning_distance = 1100
        self.distance_variance = 100

        self.snake_angle_variance = math.pi * 0.25
        # self.snake_min_spawn_distance = 200
        self.snake_max_spawn_distance = 1300

        self.last_spawned_obstacle = None
        self.snake_vx = 0
        self.snake_vy = 0

        # save the position of the player each time we spawn something
        # we'll use it (and the new position of the player) to determine when to spawn the next thing
        self.last_spawn_position_x = game.player.x
        self.last_spawn_position_y = game.player.y

    def Update(self):
        self.Scatter()
        self.Snake()

    def Scatter(self):
        # if self.type is SCATTER or self.last_spawned_obstacle is None:
        # get the distance the players moved since we last spawned something
        d = Distance( self.last_spawn_position_x, self.last_spawn_position_y,
                      self.game.player.x, self.game.player.y)

        if d > self.spawn_rate:
            # then we'll spawn something

            # create a random point in front of the player, outside of the screen
            vx = self.game.player.x - self.last_spawn_position_x
            vy = self.game.player.y - self.last_spawn_position_y
            rx, ry = RandomVector(vx,vy,self.scatter_angle_variance,
                                  self.scatter_spawning_distance,self.distance_variance)
            newx = self.game.player.x + rx
            newy = self.game.player.y + ry

            tree = Tree(self.game)
            tree.x = newx
            tree.y = newy
            self.game.AddObject(tree)

            if self.last_spawned_obstacle is None or \
                    Distance( self.last_spawned_obstacle.x, self.last_spawned_obstacle.y,
                      self.game.player.x, self.game.player.y) > 1400:
                self.last_spawned_obstacle = tree
                self.snake_vx = vx
                self.snake_vy = vy

            # finalize
            self.last_spawn_position_x = self.game.player.x
            self.last_spawn_position_y = self.game.player.y

    def Snake(self):
        # elif self.type is SNAKE:
        if self.last_spawned_obstacle is None:
            return
        # get the distance between the player and the last spawned object
        d = Distance( self.last_spawned_obstacle.x, self.last_spawned_obstacle.y,
                      self.game.player.x, self.game.player.y)

        # if that distance is less than our spawning distance we'll spawn another obstacle to try and stay ahead
        if d < self.snake_max_spawn_distance:
            rx, ry = RandomVector(self.snake_vx,self.snake_vy,self.snake_angle_variance,
                                  self.last_spawned_obstacle.radius*2.0, 10 )

            newx = self.last_spawned_obstacle.x + rx
            newy = self.last_spawned_obstacle.y + ry

            tries_left = 10
            while Distance( newx, newy, self.game.player.x, self.game.player.y ) < self.scatter_spawning_distance:
                # if the tree would spawn where the player can see then try to find another place
                rx, ry = RandomVector(self.snake_vx,self.snake_vy,self.snake_angle_variance,
                                  self.last_spawned_obstacle.radius*2.0, 10 )

                newx = self.last_spawned_obstacle.x + rx
                newy = self.last_spawned_obstacle.y + ry
                tries_left -= 1
                if tries_left is 0:
                    self.last_spawned_obstacle = None
                    print('Snake giving up')
                    return # not only break out of the loop but give up on making a tree

            tree = Tree(self.game)
            tree.x = newx
            tree.y = newy
            self.game.AddObject(tree)

            self.snake_vx = newx - self.last_spawned_obstacle.x
            self.snake_vy = newy - self.last_spawned_obstacle.y
            self.last_spawned_obstacle = tree


        # elif d > self.snake_max_spawn_distance:
        #     self.last_spawned_obstacle = None