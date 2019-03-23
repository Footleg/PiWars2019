#!/usr/bin/env python3

import RobotControl as rc

minSideDist = 100
maxSideDist = 200
minFrontDist = 120
maxSteeringAngle = 25
lastWallDistance = 0
targetWallDistance = 0

def updateMinSideDist(increment):
    """ Updates the value of minSideDist by the amount 'increment'.
        Limits value to between a minimum allowed value and less
        than the value of maxSideDist
    """
    global minSideDist, maxSideDist
    
    minSideDist += increment
    
    if minSideDist < 10:
        minSideDist = 10
    elif minSideDist > maxSideDist - 10:
        minSideDist = maxSideDist - 10


def updateMaxSideDist(increment):
    """ Updates the value of maxSideDist by the amount 'increment'.
        Limits value to between a maximum allowed value and greater
        than the value of minSideDist
    """
    global minSideDist, maxSideDist
    
    maxSideDist += increment
    
    if maxSideDist < minSideDist + 10:
        maxSideDist = minSideDist + 10
    elif maxSideDist > 2000:
        maxSideDist = 2000


def updateMinFrontDist(increment):
    """ Updates the value of minFrontDist by the amount 'increment'.
        Limits value to between a defined allowed range
    """
    global minFrontDist
    
    minFrontDist += increment

    if minFrontDist < 10:
        minFrontDist = 10
    elif minFrontDist > 1000:
        minFrontDist = 1000


def updateAutoCycles(increment):
    """ Updates the value of autoCycles by the amount 'increment'.
        Limits value to between a defined allowed range
    """
    global autoCycles
    


def updateMaxSteeringAngle(increment):
    """ Updates the value of maxSteeringAngle by the amount 'increment'.
        Limits value to between a defined allowed range
    """
    global maxSteeringAngle
    
    maxSteeringAngle += increment

    if maxSteeringAngle < 5:
        maxSteeringAngle = 5
    elif maxSteeringAngle > 50:
        maxSteeringAngle = 50
    

def driveAuto(leftDist, rightDist, frontDist):
    """ Update steering and motors based on sensor values """
    global minSideDist, maxSideDist, minFrontDist

    if frontDist < minFrontDist:
        #Stop if closer than min front distance from obstacle
        rc.setLeftMotorPower(0)
        rc.setRightMotorPower(0)
    elif rc.motorPowerL == 0:
        #Start motors if nothing closer than min front distance from obstacle
        #and motors are stopped
        rc.setLeftMotorPower(100)
        rc.setRightMotorPower(100)
    
    distance = 5000
    direction = 1
    
    if leftDist < maxSideDist and rightDist < maxSideDist:
        #Angle away from nearest side
        if leftDist > rightDist:
            distance = rightDist
            direction = -1
        elif leftDist < rightDist:
            distance = leftDist
    elif leftDist < maxSideDist:
        distance = leftDist
    elif rightDist < maxSideDist:
        distance = rightDist
        direction = -1
        
    if distance < minSideDist:
        distance = minSideDist
    
    if distance > maxSideDist:
        angle = 0 
    else:
        angle = direction * (maxSteeringAngle - maxSteeringAngle * (distance - minSideDist) / (maxSideDist - minSideDist))
        
    #print("Distance: {} Angle: {}".format(distance,angle) )

    rc.setSteering(angle)


def setMotorPower(frontDist):
    """ Sets motors to run if front sensor is not measuring obstacle ahead.
    """
    if frontDist < minFrontDist:
        #Stop if closer than min front distance from obstacle
        rc.setLeftMotorPower(0)
        rc.setRightMotorPower(0)
    elif rc.motorPowerL == 0:
        #Start motors if nothing closer than min front distance from obstacle
        #and motors are stopped
        rc.setLeftMotorPower(100)
        rc.setRightMotorPower(100)


def wallFollow(leftDist, rightDist, frontDist, left = False):
    """ Follow left or right wall.
        Steering attempts to keep robot the same distance from the wall as starting distance.
    """
    global lastWallDistance, targetWallDistance
    
    setMotorPower(frontDist)
    
    if left == True:
        distance = leftDist
    else:
        distance = rightDist
        
    if targetWallDistance == 0:
        #Just set target distance
        targetWallDistance = distance
        lastWallDistance = distance
    elif lastWallDistance > 0:
        #Have two readings to compare, so determine if increasing or decreasing
        trendDist = lastWallDistance - distance
        
        #Determine how close to target
        targetdiff = targetWallDistance - distance 
        
        #Set steering angle based on whether moving away or nearer to wall
        maxTrendDistance = 10
        if trendDist > maxTrendDistance:
            angle = maxSteeringAngle
        elif trendDist < -maxTrendDistance:
            angle = -maxSteeringAngle
        else:
            angle = int(maxSteeringAngle * trendDist / maxTrendDistance)
        
        #Factor in difference between target distance and measured distance
        maxSteerDistance = 200
        maxTargetFactor = 15
        if targetdiff > maxSteerDistance:
            addn = maxTargetFactor
        elif targetdiff < -maxSteerDistance:
            addn = -maxTargetFactor
        else:
            addn = int(maxTargetFactor * targetdiff / maxSteerDistance)
            
        print("Target {}; Dist {}; Trend: {}; TrdCmp: {}; TrgCmp {}".format(targetWallDistance,distance,trendDist,angle,addn))
    
        angle += addn
        
        rc.setSteering(-angle)
        
        #Remember distance to compare with next time
        lastWallDistance = distance
        
        