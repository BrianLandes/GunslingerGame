
# Brian Landes
# Final Project
import FloatingText
import math
from Utilities import GetAngle
import Bullet
# contains the stats and methods for the weapon

# weapon constants
GATLING_GUN = 0 # bullets fire in pattern intervals with spread
SHOTGUN = 1 # bullets fire in waves with spread
MACHINE_GUN = 2 # bullets fire in pattern intervals with no spread
SNIPER = 3 # bullets fire in waves with no spread

SPAWN_DISTANCE = 10
VERTICAL_OFFSET = -20

class Weapon(object):
    def __init__(self,game):
        self.game = game # a reference to the GunslingerGame class
        self.type = GATLING_GUN
        self.firing = False
        self.fire_timer = 0.0

        self.level = 0
        self.bullet_rate = 0
        self.spread = 0  # an angle in degrees
        self.fire_rate = 0
        self.next_upgrade = 10
        self.UpgradeWeapon()

        ## volatile variables
        self.last_barrel = 0

    def Reset(self):
        self.type = GATLING_GUN
        self.firing = False


        self.level = 0
        self.UpgradeWeapon()
        self.fire_timer = 1/self.fire_rate
        self.next_upgrade = 10

    def UpgradeWeapon(self):
        self.level += 1
        self.SetStatsForGatling()

        if self.level >1:

            floating_text = FloatingText.New(self.game, (255,247,84), "Upgrade!",
                                        self.game.width*0.3, self.game.height*0.2,life=3,
                                    target_object = self.game.player, target_offset = -180)
            self.game.AddObject(floating_text)

    def SetStatsForShotgun(self):
        self.bullet_rate = int( self.level/2 ) + 1
        self.spread = self.level*2  # an angle in degrees
        self.fire_rate = 0.2 - self.level * 0.01

        self.next_upgrade = self.level * 200

    def SetStatsForGatling(self):
        # self.bullet_rate = int( self.level/2 ) + 1
        if 0 <= self.level <= 5:
            self.spread = 0
        elif self.level <= 30:
            self.spread = 15
        else:
            self.spread = 25

        if 0 <= self.level <= 1:
            self.fire_rate = 1.8
        elif self.level <= 15:
            self.fire_rate = 3.5 + ((self.level-2)*0.6)
            # max 11
        elif self.level <= 30:
            self.fire_rate = 8.0 + ((self.level-16)*0.7)
            # max 18
        else:
            self.fire_rate = 18.0 + ((self.level-31)*0.8)

        self.next_upgrade += (self.level-1) * 20

    def Update(self):
        if not self.game.player.dead:
            if self.type == GATLING_GUN:
                self.GatlingGun()
            elif self.type == SHOTGUN:
                self.Shotgun()

    def GatlingGun(self):
        if self.firing:
            self.fire_timer += self.game.delta_time

            delta = 1.0/self.fire_rate

            fired = False
            count = 0
            while self.fire_timer > delta:
                self.fire_timer -= delta

                # # the angle between each of the bullets as they are evenly spread
                # if self.bullet_rate > 1:
                #     spread_dif = math.radians(self.spread) / (self.bullet_rate - 1)
                # else:
                #     # if there's only one bullet then spread doesn't really matter
                #     spread_dif = 0

                # get the angle from the player to the mouse
                theta = GetAngle(self.game.mouse_x - self.game.player.x - self.game.world_x,
                    self.game.mouse_y - self.game.player.y - self.game.world_y - VERTICAL_OFFSET)
                # given the spread, start at the one side
                angle = theta

                if self.last_barrel == 1 or self.last_barrel==3:
                    angle -= math.radians(self.spread) * 0.5
                elif self.last_barrel == 2:
                    angle += math.radians(self.spread) * 0.5

                newBullet = self.SpawnBullet()
                # omega = angle + spread_dif*i
                omega = angle
                newBullet.x += math.cos(omega) * SPAWN_DISTANCE
                newBullet.y += math.sin(omega) * SPAWN_DISTANCE + VERTICAL_OFFSET
                # shoot the bullet in that direction, including the player's speed in the bullet's velocity
                newBullet.vel_x = math.cos(omega) * Bullet.BULLET_MOVE_SPEED
                newBullet.vel_y = math.sin(omega) * Bullet.BULLET_MOVE_SPEED
                newBullet.RotateBasedOnVelocity()

                self.last_barrel += 1
                if self.last_barrel >= 4:
                    self.last_barrel = 0

                fired = True
                count += 1

            if fired:
                # play the gunshot
                self.game.audio.PlayGunshot()

        elif self.fire_timer< 1/self.fire_rate:
            self.fire_timer += self.game.delta_time

    def Shotgun(self):
        if self.fire_timer < self.fire_rate:
            self.fire_timer += self.game.delta_time
        if self.firing:
            if self.fire_timer > self.fire_rate:
                self.fire_timer -= self.fire_rate

                # the angle between each of the bullets as they are evenly spread
                if self.bullet_rate > 1:
                    spread_dif = math.radians(self.spread) / (self.bullet_rate - 1)
                else:
                    # if there's only one bullet then spread doesn't really matter
                    spread_dif = 0

                # get the angle from the player to the mouse
                theta = GetAngle(self.game.mouse_x - self.game.player.x - self.game.world_x,
                    self.game.mouse_y - self.game.player.y - self.game.world_y - VERTICAL_OFFSET)
                # given the spread, start at the one side
                angle = theta - math.radians(self.spread) * 0.5
                for i in range(self.bullet_rate):
                    newBullet = self.SpawnBullet()
                    omega = angle + spread_dif*i
                    newBullet.x += math.cos(omega) * SPAWN_DISTANCE
                    newBullet.y += math.sin(omega) * SPAWN_DISTANCE + VERTICAL_OFFSET
                    # shoot the bullet in that direction, including the player's speed in the bullet's velocity
                    newBullet.vel_x = math.cos(omega) * Bullet.BULLET_MOVE_SPEED
                    newBullet.vel_y = math.sin(omega) * Bullet.BULLET_MOVE_SPEED
                    newBullet.RotateBasedOnVelocity()
                    # newBullet.vel_x += self.game.player.vel_x
                    # newBullet.vel_y += self.game.player.vel_y

                # play the gunshot
                self.game.audio.PlayGunshot()

    def SpawnBullet(self):
        newBullet = Bullet.Bullet(self.game)

        # create a new bullet on top of the player
        newBullet.x = self.game.player.x
        newBullet.y = self.game.player.y

        self.game.AddObject(newBullet)
        return newBullet