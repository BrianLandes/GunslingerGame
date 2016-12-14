
import math,random,pygame

def GetAngle( x, y ):
    # get the angle of the vector<x,y>
    return math.atan2( y, x )

def CheckObjectCollision( objectA, objectB ):
    # checks two game objects against each other
    # returns True if they overlap
    # False otherwise
    # and False if either object is dead
    if objectA.dead or objectB.dead:
        return False
    #we assume that both objects are just circles -> circle and circle collision detection
    # two circles overlap if the distance between the center points is less than the sum of the radii
    r = objectA.radius + objectB.radius # the sum of the radii
    x = abs( objectA.x - objectB.x ) # the total distance across the x axis
    # if x is greater than the sum of the radii then we know already that they don't collide
    if x > r:
        return False
    y = abs( objectA.y - objectB.y ) # the total distance across the y axis
    # same as above, if y is greater than the sum of the radii then we know already that they don't collide
    if y > r:
        return False
    # calculate the length of the vector<x,y> which will be the distance between the two center points
    d = math.sqrt( x**2 + y**2 )
    # check for if that distance is greater than the sum of the radii
    if d > r:
        # then they are not colliding
        return False

    # then they are colliding
    return True

def GetDistance( gameObjectA, gameObjectB ):
    # returns the distance between the two center points of the game objects
    x = gameObjectA.x - gameObjectB.x
    y = gameObjectA.y - gameObjectB.y
    return math.sqrt( x**2 + y**2 )


def Lerp(value, a, b):
    # takes 3 floats where
    # value is between 0.0 and 1.0
    # and returns a float equal to a if value is 0.0
    # or b if value is 1.0
    # or a float between a and b based on value

    real_max = max(a,b)
    real_min = min(a,b)
    dif = real_max - real_min
    return real_min + dif * value

def Distance( x1,y1,x2,y2 ):
    # returns the distance between the two points
    x = x1 - x2
    y = y1 - y2
    return math.sqrt( x**2 + y**2 )

def RepositionBoth( objectA, objectB ):
    # assumes these objects are overlapping and pushes them away from each other
    # until they aren't touching anymore
    # find the vector from the first object to the second
    vx = objectB.x - objectA.x
    vy = objectB.y - objectA.y
    # we need the magnitude of that vector in order to scale it
    mv = math.sqrt( vx**2 + vy**2 )
    # scale the vector so that it is equal to half the sum of the radii
    r = objectA.radius + objectB.radius  # the sum of the radii
    ux = vx/mv * r * 0.5
    uy = vy/mv * r * 0.5
    # find the point directly in between the two objects
    midx = (objectB.x + objectA.x)/2
    midy = (objectB.y + objectA.y)/2
    # move the first object based on the mid point and the half-vector
    objectA.x = midx + ux
    objectA.y = midy + uy
    #move the second object
    objectB.x = midx - ux
    objectB.y = midy - uy

def Reposition( objectA, objectB ):
    # repositions just the first object based on the second
    theta = GetAngle( objectA.x - objectB.x, objectA.y - objectB.y)
    r = objectB.radius + objectA.radius
    objectA.x = objectB.x + math.cos(theta) * r
    objectA.y = objectB.y + math.sin(theta) * r

def RandomPointInCircle( radius ):
    theta = random.random() * 360
    magnitude = random.random() * radius
    # turn our angle and magnitude into a vector
    x = math.cos(theta) * magnitude
    y = math.sin(theta) * magnitude
    return x,y

def RandomVector( vx, vy, angle_variance, magnitude, magnitude_variance ):
    # returns a vector with a similar direction to vector <vx, vy>
    # with the direction randomized by + or - up to angle_variance (in radians)
    # and a magnitude/length of the given magnitude + or - up to magnitude_variance

    # get a random value between +angle_variance and -angle_variance
    var = random.random() * 2.0 * angle_variance - angle_variance
    # get the angle of <vx,vy> and add our randomness
    theta = GetAngle( vx, vy ) + var
    # get a random value between +magnitude_variance and -magnitude_variance
    mag_var = random.random() * 2.0 * magnitude_variance - magnitude_variance
    # get the sum of the desired magnitude and our randomness
    m = magnitude + mag_var
    # turn our angle and magnitude into a vector
    x = math.cos(theta) * m
    y = math.sin(theta) * m
    return x,y

def RandomColorFromSurface( pygame_surface ):
    width, height = pygame_surface.get_size()
    x = random.randint(0,width-1)
    y = random.randint(0,height-1)

    color = pygame_surface.get_at((x,y))
    return ( color )

def RandomValueFromProbabilities(values,probs):
    # takes two lists which are one to one
    # returns one entry from 'values' based
    # on a random float and the probabilities in probs (which DO NOT necessarily add up to 1.0)
    total_p = sum(probs)
    lottery = random.random() * total_p
    num = 0
    i = 0
    for value in values:
        num += probs[i]
        if num >= lottery:
            return value
        i += 1