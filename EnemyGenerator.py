# Brian Landes
# October 29, 2016

# this class handles the generation of the enemies

from Enemy import Enemy
import random, math

MIN_SPAWN_RATE = 1/5 # 1 every 5 seconds
MAX_SPAWN_RATE = 5/1 # 5 per second
SPAWN_ACCELERATION = 0.0001
# SPAWN_RATE = 0.2 # every 2 seconds
# SPAWN_DIR_CHANGE = math.pi / 200
SPAWN_ANGLE_VARIANCE = math.pi * 0.125 # upto 90 degrees in either direction
SPAWN_DISTANCE = 600
MIN_STATE_TIME = 3 # seconds
MAX_STATE_TIME = 3 # seconds
MIN_SPIN_SPEED = 0.005
MAX_SPIN_SPEED = 0.01
WARM_UP_TIME = 1 # give the player X seconds into the start of the game before we start spawning enemies

#### State constants
WARM_UP = 0
SPIN_CW = 1
SPIN_CCW = 2
WAIT = 3

class EnemyGenerator(object):
    def __init__(self,game):
        self.game = game # a reference to the GunslingerGame class

        self.spawn_timer = 0.0
        self.spawn_rate = MIN_SPAWN_RATE
        self.spawning_direction = random.random() * 2.0 * math.pi # a random direction 0 - 360
        self.state = WARM_UP
        self.state_timer = 0.0
        self.total_state_time = WARM_UP_TIME
        self.spin_speed = 0.0
        self.bonus = 0.0

    def Update(self):
        self.state_timer
        self.state_timer += self.game.delta_time
        if self.state_timer > self.total_state_time:
            self.state = random.choice( [ SPIN_CW, SPIN_CCW, WAIT ] )
            # set a timer for some random time between the min and max
            self.total_state_time = random.random() * (MAX_STATE_TIME - MIN_STATE_TIME) + MIN_STATE_TIME
            self.state_timer = 0.0
            self.spin_speed = random.random() * (MAX_SPIN_SPEED - MIN_SPIN_SPEED) + MIN_SPIN_SPEED
            if self.state is SPIN_CCW:
                self.spin_speed = -self.spin_speed
            elif self.state is WAIT:
                self.spin_speed = 0

        elif self.state is not WARM_UP:
            self.spawn_timer += self.game.delta_time

            if self.spawn_timer > 1/self.spawn_rate:
                self.spawn_timer -= 1/self.spawn_rate
                self.SpawnEnemy()
                # sometimes spawn 2 enemies
                self.bonus += random.random()
                if self.bonus > 2.0:
                    self.SpawnEnemy()
                    self.bonus -= 2.0

            self.spawning_direction += self.spin_speed
            if self.spawn_rate < MAX_SPAWN_RATE:
                self.spawn_rate += SPAWN_ACCELERATION
                # print('time between spawns: ',1/self.spawn_rate)

    def SpawnEnemy(self):
        newEnemy = Enemy(self.game)

        variance = random.random() * 2.0 * SPAWN_ANGLE_VARIANCE - SPAWN_ANGLE_VARIANCE
        theta = self.spawning_direction + variance
        newEnemy.x = self.game.player.x + math.cos(theta) * SPAWN_DISTANCE
        newEnemy.y = self.game.player.y + math.sin(theta) * SPAWN_DISTANCE
        self.game.AddObject( newEnemy)