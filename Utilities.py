
import math

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