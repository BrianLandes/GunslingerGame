
# Brian Landes
# Final Project

import pygame, sys
import math
import random
import time
from GameObject import GameObject

mute_audio = False

class GameObject(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vel_x = 0
        self.vel_y = 0
        self.radius = 20
        self.color = ( 100, 100, 100 )
        self.dead = False

    def Draw(self):
        pygame.draw.circle(screen, self.color, (
            int(self.x + world_x),
            int(self.y + world_y ) ),
            int(self.radius) )

    def UpdatePosition(self, obstacles = None):
        self.x += self.vel_x
        self.y += self.vel_y
                    
    def Destroy(self):
        self.dead = True
        destroyables.append(self)

def GetAngle( x, y ):
    return math.atan2( y, x )

def CheckObjectCollision( objectA, objectB, use_future_position=False ):
    if objectA.dead or objectB.dead:
        return False
    r = objectA.radius + objectB.radius
    x = abs( objectA.x - objectB.x )
    if use_future_position:
        x = abs( objectA.x + objectA.vel_x - objectB.x )
    if x > r:
        return False
    y = abs( objectA.y - objectB.y )
    if use_future_position:
        y = abs( objectA.y + objectA.vel_y - objectB.y )
    if y > r:
        return False
    d = math.sqrt( x**2 + y**2 )
    if d > r:
        return False
    return True

def SpawnEnemy():
    newEnemy = GameObject()
    newEnemy.color = enemy_color
    variance = random.random() * 2.0 * spawning_angle_variance - spawning_angle_variance
    theta = enemy_spawning_direction + variance
    newEnemy.x = player.x + math.cos(theta) * spawning_distance
    newEnemy.y = player.y + math.sin(theta) * spawning_distance
    newEnemy.radius = enemy_size
    enemies.append( newEnemy)

def SpawnTree():
    newTree = GameObject()
    newTree.color = tree_color
    if player.vel_x != 0 or player.vel_y != 0:
        variance = random.random() * 2.0 * tree_spawning_angle_variance - tree_spawning_angle_variance
        theta = GetAngle(player.vel_x, player.vel_y ) + variance
    else:
        theta = random.random() * 2.0 * math.pi
    d = random.random() * 2.0 * tree_spawn_distance_variance - tree_spawn_distance_variance
    d += tree_spawning_distance
    newTree.x = player.x + math.cos(theta) * d
    newTree.y = player.y + math.sin(theta) * d
    newTree.radius = tree_size + random.random()*60 - 30
    trees.append( newTree)

def SpawnCoin():
    newCoin = GameObject()
    newCoin.color = coin_color
    if player.vel_x != 0 or player.vel_y != 0:
        variance = random.random() * 2.0 * coin_spawning_angle_variance - coin_spawning_angle_variance
        theta = GetAngle(player.vel_x, player.vel_y ) + variance
    else:
        theta = random.random() * 2.0 * math.pi
    d = random.random() * 2.0 * coin_spawn_distance_variance - coin_spawn_distance_variance
    d += coin_spawning_distance
    newCoin.x = player.x + math.cos(theta) * d
    newCoin.y = player.y + math.sin(theta) * d
    newCoin.radius = coin_size
    coins.append( newCoin)
    # we might want to do a check and make sure the coins don't spawn on top of trees

def FireWeapon():

    # the angle between each of the bullets as they are evenly spread
    if weapon_bullet_rate >1:
        spread_dif = math.radians(weapon_spread) / (weapon_bullet_rate-1)
    else:
        # if there's only one bullet then spread doesn't really matter
        spread_dif = 0

    # get the angle from the player to the mouse
    theta = GetAngle( mouse_x - player.x - world_x, mouse_y - player.y - world_y )
    # given the spread, start at the one side
    angle = theta - math.radians(weapon_spread) * 0.5
    for i in range(weapon_bullet_rate):
        newBullet = SpawnBullet()
        # shoot the bullet in that direction, including the player's speed in the bullet's velocity
        newBullet.vel_x = math.cos( angle + spread_dif * i ) * bullet_speed + player.vel_x
        newBullet.vel_y = math.sin( angle + spread_dif * i ) * bullet_speed + player.vel_y
    
    # play the gunshot
    PlaySound(gunshot_sfx)

def SpawnBullet():
    newBullet = GameObject()
    newBullet.color = bullet_color
    # create a new bullet on top of the player
    newBullet.x = player.x
    newBullet.y = player.y
    newBullet.radius = bullet_size
    
    bullets.append( newBullet )
    return newBullet
    

def FlushDestroys():
    # a better way to do this would be to keep all the game objects in one list
    # and handle the logic differently based on their types
    for d in destroyables:
        if d in enemies:
            enemies.remove(d)
        elif d in bullets:
            bullets.remove(d)
        elif d in trees:
            trees.remove(d)
        elif d in coins:
            coins.remove(d)

    destroyables.clear()

def GetDistanceToPlayer( gameObject ):
    x = gameObject.x - player.x
    y = gameObject.y - player.y
    return math.sqrt( x**2 + y**2 )

def RepositionBoth( objectA, objectB ):
    # assumes these objects are overlapping and pushes them away from each other
    # until they aren't touching anymore
    # find the vector from the first object to the second
    vx = objectB.x - objectA.x
    vy = objectB.y - objectA.y
    # we need the magnitude of that vector in order to scale it
    mv = math.sqrt(vx ** 2 + vy ** 2)
    # scale the vector so that it is equal to half the sum of the radii
    r = objectA.radius + objectB.radius  # the sum of the radii
    ux = vx / mv * r * 0.5
    uy = vy / mv * r * 0.5
    # find the point directly in between the two objects
    midx = (objectB.x + objectA.x) / 2
    midy = (objectB.y + objectA.y) / 2
    # move the first object based on the mid point and the half-vector
    objectA.x = midx + ux
    objectA.y = midy + uy
    # move the second object
    objectB.x = midx - ux
    objectB.y = midy - uy

def Reposition( objectA, objectB ):
    # repositions just the first object based on the second
    theta = GetAngle( objectA.x - objectB.x, objectA.y - objectB.y)
    r = objectB.radius + objectA.radius
    objectA.x = objectB.x + math.cos(theta) * r
    objectA.y = objectB.y + math.sin(theta) * r

channels = []

def PlaySound(sound_fx_list):
    # given a list of similar sound effects, choose a random one
    sound_fx = sound_fx_list[random.randint(0,len(sound_fx_list)-1)]
    if mute_audio:
        return
    # we can only play a certain number of sound fx at one time
    # max is NUM_SOUND_CHANNELS
    # if we go to play another sound and all the channels are busy
    # lets just cut 1 and play our sound since its probably almost done anyways
    # and the player won't notice over a dozen other sounds
    # free up our list of any not playing channels
    temp_ls = channels.copy()
    for channel in temp_ls:
        if channel is None or not channel.get_busy():
            #print( 'dropping channel' )
            channels.remove(channel)

    # print( len(channels) )

    if len(channels)>=NUM_SOUND_CHANNELS:
        # we already have NUM_SOUND_CHANNELS sounds playing so we need to stop one
        # might as well be the first one in our list
        channels[0].stop
        channels[0].play( sound_fx )
    else:

        channels.append( sound_fx.play() )

def UpgradeWeapon():
    global weapon_level, weapon_bullet_rate, weapon_spread, weapon_fire_rate
    weapon_level += 1
    weapon_bullet_rate, weapon_spread, weapon_fire_rate = GetWeaponStats(weapon_level)

def GetWeaponStats(weapon_level):
    # returns the number of bullets, the spread, and the rate of fire
    if weapon_level is 1:
        bullet_count = 1
        spread = 0 # an angle in degrees
        fire_rate = 0.1
    elif 1 < weapon_level <= 5:
        bullet_count = 2
        spread = 10 # an angle in degrees
        fire_rate = 0.11 - (weapon_level)*0.01
    elif 5 < weapon_level:
        bullet_count = 3
        spread = 12 # an angle in degrees
        fire_rate = 0.1 - (weapon_level)*0.01

    return bullet_count, spread, fire_rate

def DisplayPoints():
    pointText = pointFont.render('$'+str(score), True, POINTS_COLOR, None)
    TX, TY = pointText.get_size()
    textWidth = int(POINTS_HEIGHT * (TX / TY))
    pointText = pygame.transform.scale(pointText, (textWidth, POINTS_HEIGHT))
    x = int(SCREEN_WIDTH * 0.95 - textWidth)
    y = int(SCREEN_HEIGHT * 0.97 - POINTS_HEIGHT)
    screen.blit(pointText, (x, y))

NUM_SOUND_CHANNELS =32

pygame.mixer.pre_init()
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(NUM_SOUND_CHANNELS)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
playing = True

POINT_FONT = "fonts/LinBiolinum_RBah.ttf"
pointFont = pygame.font.Font(POINT_FONT, 96)
POINTS_HEIGHT = int(SCREEN_HEIGHT*0.05)
POINTS_COLOR = (0,0,0)

clock = pygame.time.Clock()

# GameObjects
enemies = []
bullets = []
trees = []
coins = []
destroyables = []

# Camera
world_x = 0
world_y = 0

# Player
player = GameObject()
player.radius = 20
player.x = SCREEN_WIDTH * 0.5
player.y = SCREEN_HEIGHT * 0.5
player.vel_x = 0
player.vel_y = 0
player.color = ( 25, 100, 250 )

# Settings
player_move_speed = 4

# weapon constants
##GATLING_GUN = 0 # bullets fire at random intervals with a random spread (medium spread)
##SHOTGUN = 1 # bullets fire in steady waves in a constant spread (large spread)
##MACHINE_GUN = 2 # bullets fire in short random intervals with a small spread
##
##weapon_type = GATLING_GUN
weapon_level = 0
weapon_bullet_rate = 0
weapon_spread = 0
weapon_fire_rate = 0
UpgradeWeapon() # initialize the weapon level to 1

bullet_speed = 15
bullet_size = 5
bullet_color = (10,20,10)
bullet_range = 800
firing = False

tree_size = 70
tree_range = 1000
tree_spawn_time = 0.4
tree_color = ( 0, 255, 0 )
tree_spawning_angle_variance = math.pi * 0.5 # upto 90 degrees in either direction
tree_spawning_distance = 600
tree_spawn_distance_variance = 100

spawning_angle_variance = math.pi * 0.25 # upto 90 degrees in either direction
spawning_distance = 600
enemy_color = (225,0,0)
enemy_size = 15
enemy_move_speed = 5.5
enemy_spawn_time = 0.2 # every 2 seconds
spawn_dir_change = math.pi / 6

coin_value = 10
coin_size = 20
coin_range = 1000
coin_spawn_time = 2.0
coin_color = ( 255,247,49 )
coin_spawning_angle_variance = math.pi * 0.5 # upto 90 degrees in either direction
coin_spawning_distance = 600
coin_spawn_distance_variance = 100

# Running measurements
enemy_spawning_direction = random.random() * 2.0 * math.pi # a random direction 0 - 360
enemy_spawn_timer = 0.0
tree_spawn_timer = 0.0
coin_spawn_timer = 0.0
fire_timer = 0.0
last_time = time.time()
mouse_x = 0
mouse_y = 0
score = 0

# make some random trees
for i in range( 6 ):
    newTree = GameObject()
    newTree.x = random.randint( 0, SCREEN_WIDTH)
    newTree.y = random.randint( 0, SCREEN_HEIGHT )
    newTree.radius = tree_size
    newTree.color = tree_color
    trees.append(newTree)

# load some sounds
gunshot_sfx= []
for i in range(1,6):
    gunshot_sfx.append( pygame.mixer.Sound('gunshot0' + str(i) + '_sfx.wav') )
    gunshot_sfx[-1].set_volume(0.2)

enemy_death_sfx= []
for i in range(1,4):
    enemy_death_sfx.append( pygame.mixer.Sound(
        'enemy_death_0' + str(i) + '_sfx.wav') )

# music_track = pygame.mixer.music.load(
#     '155139__burning-mir__action-music-loop-with-dark-ambient-drones.wav')
# pygame.mixer.music.play(loops = -1 )

while playing:
    # lets keep track of how much time has passed between the last frame and this one
    current_time = time.time()
    delta_time = current_time - last_time
    for event in pygame.event.get():
        # if the app is quit then break and close
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()
            sys.exit()

        # if the player pressed the mouse then fire a bullet
        if event.type == pygame.MOUSEBUTTONDOWN:
            firing = True
        if event.type == pygame.MOUSEBUTTONUP:
            firing = False

    # Fire bullets
    if fire_timer < weapon_fire_rate:
        fire_timer += delta_time
    if firing:
        if fire_timer > weapon_fire_rate:
            fire_timer -= weapon_fire_rate
            mouse_x, mouse_y = pygame.mouse.get_pos()
            FireWeapon()

    # Check for key presses and update the player's position
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] or pressed[pygame.K_w]:
        player.vel_y = -player_move_speed
    elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
        player.vel_y = player_move_speed
    else: player.vel_y = 0
        
    if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
        player.vel_x = -player_move_speed
    elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
        player.vel_x = player_move_speed
    else: player.vel_x = 0

    # if the player is moving diagonally, reduce the speed so its only as fast as moving in one direction
    if abs(player.vel_x) + abs(player.vel_y) > player_move_speed:
        # pythagoream thereom baby
        n = math.sqrt(2)/2
        player.vel_x *= n
        player.vel_y *= n

    # apply the gameobject's velocity to its own position
    player.UpdatePosition()
    # since the camera follows the player just set the world origin to the player's position
    world_x = int(-player.x + SCREEN_WIDTH * 0.5)
    world_y = int(-player.y + SCREEN_HEIGHT * 0.5)

    # Check the trees
    for tree in trees:
        if CheckObjectCollision( tree, player):
            Reposition(player,tree)

    # Check the coins
    for coin in coins:
        if CheckObjectCollision( coin, player):
            coin.Destroy()
            score += coin_value
            if score%100 is 0:
                UpgradeWeapon()

    # Spawn enemies
    enemy_spawn_timer += delta_time
    if enemy_spawn_timer > enemy_spawn_time:
        enemy_spawn_timer -= enemy_spawn_time
        SpawnEnemy()
        enemy_spawning_direction += random.random() * 2.0 * spawn_dir_change - spawn_dir_change

    # Spawn trees
    tree_spawn_timer += delta_time
    if tree_spawn_timer > tree_spawn_time:
        tree_spawn_timer -= tree_spawn_time
        SpawnTree()

    # Spawn coins
    coin_spawn_timer += delta_time
    if coin_spawn_timer > coin_spawn_time:
        coin_spawn_timer -= coin_spawn_time
        SpawnCoin()

    # Update Enemies
    for i in range( len( enemies) ):
        enemy = enemies[i]
        theta = GetAngle( player.x - enemy.x, player.y - enemy.y )
        enemy.vel_x = math.cos( theta ) * enemy_move_speed
        enemy.vel_y = math.sin( theta ) * enemy_move_speed
        enemy.UpdatePosition( enemies[i+1: ])
        # check the enemy against the player
        if CheckObjectCollision( enemy, player ):
            Reposition(enemy,player)
        # check each enemy against each other enemy
        for j in range( i+1, len( enemies ) ):
            enemyB = enemies[j]
            if CheckObjectCollision( enemy, enemyB ):
                RepositionBoth(enemy,enemyB)
        # Check if this enemy was hit with a bullet
        for bullet in bullets:
            if CheckObjectCollision( enemy, bullet ):
                enemy.Destroy()
                bullet.Destroy()
                # play the enemy death
                PlaySound(enemy_death_sfx)
                break
    

    # clear the screen
    screen.fill( (220, 220, 200 ) )

    # Update the bullets
    for bullet in bullets:
        if GetDistanceToPlayer(bullet) > bullet_range:
            bullet.Destroy()
        bullet.UpdatePosition()

    # Draw the trees
    for tree in trees:
        if GetDistanceToPlayer(tree) > tree_range:
            tree.Destroy()
        tree.Draw()

    # Draw the coins
    for coin in coins:
        if GetDistanceToPlayer(coin) > coin_range:
            coin.Destroy()
        coin.Draw()

    # Draw the player
    player.Draw()

    # Draw the bullets
    for bullet in bullets:
        bullet.Draw()

    # Draw the enemies
    for enemy in enemies:
        enemy.Draw()

    # draw the points
    DisplayPoints()

    pygame.display.flip()

    clock.tick(60)

    last_time = current_time

    FlushDestroys()
