
# Brian Landes
# Final Project
import math
from Utilities import GetAngle
import Bullet
# contains the stats and methods for the weapon

# weapon constants
GATLING_GUN = 0 # bullets fire at random intervals with a random spread (medium spread)
SHOTGUN = 1 # bullets fire in steady waves in a constant spread (large spread)
MACHINE_GUN = 2 # bullets fire in short random intervals with a small spread

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
        self.UpgradeWeapon()

        self.next_upgrade = 100

    def UpgradeWeapon(self):
        self.level += 1

        self.bullet_rate = int( self.level/2 ) + 1
        self.spread = self.level*2  # an angle in degrees
        self.fire_rate = 0.2 - self.level * 0.01

        self.next_upgrade = self.level * 200

    def Update(self):
        if not self.game.player.dead:
            # Fire bullets
            if self.fire_timer < self.fire_rate:
                self.fire_timer += self.game.delta_time
            if self.firing:
                if self.fire_timer > self.fire_rate:
                    self.fire_timer -= self.fire_rate
                    self.Fire()

    def Fire(self):

        # the angle between each of the bullets as they are evenly spread
        if self.bullet_rate > 1:
            spread_dif = math.radians(self.spread) / (self.bullet_rate - 1)
        else:
            # if there's only one bullet then spread doesn't really matter
            spread_dif = 0

        # get the angle from the player to the mouse
        theta = GetAngle(self.game.mouse_x - self.game.player.x - self.game.world_x,
                         self.game.mouse_y - self.game.player.y - self.game.world_y)
        # given the spread, start at the one side
        angle = theta - math.radians(self.spread) * 0.5
        for i in range(self.bullet_rate):
            newBullet = self.SpawnBullet()
            # shoot the bullet in that direction, including the player's speed in the bullet's velocity
            newBullet.vel_x = math.cos(angle + spread_dif * i) * Bullet.BULLET_MOVE_SPEED
            newBullet.vel_y = math.sin(angle + spread_dif * i) * Bullet.BULLET_MOVE_SPEED
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