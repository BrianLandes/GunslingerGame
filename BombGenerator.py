# Brian Landes
# Final Project
# Spawns coins as the player moves through the level
import math
from Utilities import Distance
from Utilities import RandomVector
from Bomb import Bomb

class BombGenerator(object):
    def __init__(self, game):
        self.game = game # a reference to the GunslingerGame class

        self.spawn_rate = 600 # distance the player must move each time we spawn
        self.scatter_angle_variance = math.pi * 0.125 # up to 45 degrees in either direction
        self.scatter_spawning_distance = 1100
        self.distance_variance = 100

        # save the position of the player each time we spawn something
        # we'll use it (and the new position of the player) to determine when to spawn the next thing
        self.last_spawn_position_x = game.player.x
        self.last_spawn_position_y = game.player.y

    def Update(self):
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

            coin = Bomb(self.game)
            coin.x = newx
            coin.y = newy
            self.game.AddObject(coin)

            # finalize
            self.last_spawn_position_x = self.game.player.x
            self.last_spawn_position_y = self.game.player.y
