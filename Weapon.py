
# Brian Landes
# Final Project
import math
from Utilities import GetAngle
# contains the stats and methods for the weapon

# weapon constants
GATLING_GUN = 0 # bullets fire at random intervals with a random spread (medium spread)
SHOTGUN = 1 # bullets fire in steady waves in a constant spread (large spread)
MACHINE_GUN = 2 # bullets fire in short random intervals with a small spread

class Weapon(object):
    def __init__(self):
        self.type = GATLING_GUN
        self.firing = False
        self.fire_timer = 0.0

        self.level = 0
        self.bullet_rate = 0
        self.spread = 0  # an angle in degrees
        self.fire_rate = 0
        self.UpgradeWeapon()

    def UpgradeWeapon(self):
        self.level += 1

        self.bullet_rate = int( self.level/2 ) + 1
        self.spread = self.level*2  # an angle in degrees
        self.fire_rate = 0.2 - self.level * 0.01

    def Fire(self):

        # the angle between each of the bullets as they are evenly spread
        if self.bullet_rate > 1:
            spread_dif = math.radians(self.spread) / (self.bullet_rate - 1)
        else:
            # if there's only one bullet then spread doesn't really matter
            spread_dif = 0

        # get the angle from the player to the mouse
        theta = GetAngle(mouse_x - player.x - world_x, mouse_y - player.y - world_y)
        # given the spread, start at the one side
        angle = theta - math.radians(weapon_spread) * 0.5
        for i in range(self.bullet_rate):
            newBullet = SpawnBullet()
            # shoot the bullet in that direction, including the player's speed in the bullet's velocity
            newBullet.vel_x = math.cos(angle + spread_dif * i) * bullet_speed + player.vel_x
            newBullet.vel_y = math.sin(angle + spread_dif * i) * bullet_speed + player.vel_y

        # play the gunshot
        PlaySound(gunshot_sfx)