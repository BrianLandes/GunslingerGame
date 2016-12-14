# Brian Landes
# October 29, 2016

# this class handles the generation of the enemies

from Bear import Bear
from Enemy import Enemy
import FloatingText
import random, math
from Utilities import *

MIN_SPAWN_RATE = 1/6 # 1 every 5 seconds
MAX_SPAWN_RATE = 20/1 # 5 per second
SPAWN_ACCELERATION = 0.0001
# SPAWN_RATE = 0.2 # every 2 seconds
# SPAWN_DIR_CHANGE = math.pi / 200
SPAWN_ANGLE_VARIANCE = math.pi * 0.125 # upto 90 degrees in either direction
SPAWN_DISTANCE = 1300

MIN_STATE_TIME = 3 # seconds
MAX_STATE_TIME = 6 # seconds
MIN_SPIN_SPEED = 0.0005
MAX_SPIN_SPEED = 0.01
WARM_UP_TIME = 6 # give the player X seconds into the start of the game before we start spawning enemies

BEAR_SPAWN_TIME = 16
BEAR_SPAWN_DISTANCE = 1000

#### State constants
WARM_UP = 0
SPIN_CW = 1
SPIN_CCW = 2
WAIT = 3

class EnemyGenerator(object):
    def __init__(self,game):
        self.game = game # a reference to the GunslingerGame class

        self.first_game_pop_up = False
        self.first_game_pop_up_bear = False

        self.spawn_timer = 0.0
        self.spawn_rate = MIN_SPAWN_RATE
        self.spawning_direction = random.random() * 2.0 * math.pi # a random direction 0 - 360
        self.state = WARM_UP
        self.state_timer = 0.0
        self.total_state_time = WARM_UP_TIME
        self.spin_speed = 0.0
        self.bonus = 0.0
        self.spawned_bear = False
        self.bear_timer = BEAR_SPAWN_TIME

    def Reset(self):
        self.spawn_timer = 0.0
        self.spawn_rate = MIN_SPAWN_RATE
        self.spawning_direction = random.random() * 2.0 * math.pi # a random direction 0 - 360
        self.state = WARM_UP
        self.state_timer = 0.0
        self.total_state_time = WARM_UP_TIME
        self.spin_speed = 0.0
        self.bonus = 0.0
        self.spawned_bear = False
        self.bear_timer = BEAR_SPAWN_TIME
        self.rebear = 0

    def Update(self):
        self.state_timer += self.game.delta_time

        if not self.spawned_bear:
            self.bear_timer -= self.game.delta_time
            if self.bear_timer < 0.0:
                # for i in range(self.game.level):
                for i in range(1):
                    self.spawned_bear = True
                    bear = Bear(self.game)
                    variance = random.random() * 2.0 * SPAWN_ANGLE_VARIANCE - SPAWN_ANGLE_VARIANCE
                    direction = GetAngle(self.game.player.vel_x,self.game.player.vel_y)
                    theta = direction + variance
                    dis = BEAR_SPAWN_DISTANCE
                    bear.x = self.game.player.x + math.cos(theta) * dis
                    bear.y = self.game.player.y + math.sin(theta) * dis

                    self.game.AddObject( bear)

                    self.game.bear = bear

                    if not self.first_game_pop_up_bear:
                        floating_text = FloatingText.New(self.game, (127,55,51), "Don't let the Beast",
                                        self.game.width*0.7, self.game.height*0.3,
                                                 line2 = "CATCH YOU",  target_object=bear,life=6
                                                         ,target_offset=-200)
                        self.game.AddObject(floating_text)

                        self.first_game_pop_up_bear = True
                
        
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

        # have the very first enemy have some pop up text
        if not self.first_game_pop_up:
            floating_text = FloatingText.New(self.game, (255,255,255), "Use the mouse to aim",
                                self.game.width*0.6, self.game.height*0.2,
                                         line2 = "and shoot creeps",  target_object=newEnemy)
            self.game.AddObject(floating_text)
            self.first_game_pop_up = True