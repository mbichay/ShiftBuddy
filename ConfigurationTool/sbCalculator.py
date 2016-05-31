# Author: mbichay@github
#
# Description: This contains all of the algorithms used for doing interpolation
# on defining points describing a vehicle's torque curve and doing some analysis on
# it to determine a good shift point.

import math
import numpy as np
import matplotlib.pyplot as plt

# Wrapper function for calling the interpolation schema and then passing the interpolated data to the
# optimum shift point algorithm.
def calculateShiftPoints(gearRatios, definingPoints, interpolationType = 'linear', plot = False):

    if interpolationType == 'legrange':
        torqueCurve = legrangeInterpolation(definingPoints)
    else:
        torqueCurve = linearInterpolation(definingPoints)

    if plot:
        plt.plot(*zip(*torqueCurve))
        plt.plot(*zip(*definingPoints))
        plt.suptitle('Linear vs Legrange Interpolation based on Defining Points')
        plt.xlabel('Torque (lb-ft)')
        plt.ylabel('Engine Speed (RPM)')
        plt.show()

    return optimumShiftPointsAlgorithm(gearRatios, torqueCurve)



# The optimum shift point algorithm looks at the difference in torque between the torque at the vehicle's
# torque in a current gear and what the torque would be if the vehicle performed an up-shift.
# Optimum shift point is determined by the point in which the least amount of drop-in-torque occurs.
# If there is no point before redline, then the algorithm automatically defaults to the shift-point at redline.
def optimumShiftPointsAlgorithm(gearRatios, torqueCurve):

    shiftPoints = []

    # Final gear will always be redline (no gear left to up-shift into)
    shiftPoints.append(torqueCurve[len(torqueCurve)-1][0])

    # For each gear ratio (ignoring the final gear)
    for i in range(len(gearRatios)-2, -1, -1):
        minTorqueDrop = 9999999.0
        optimumShiftPt = torqueCurve[len(torqueCurve)-1][0]
        # for each point on the torque curve
        for x in range(len(torqueCurve)-1, -1, -1):
            # calculate the current torque output
            currentGearTQ = torqueCurve[x][1] * gearRatios[i]

            # calculate the RPM change if the car were to up-shift from this current RPM
            nextGearRPM = x * gearRatios[i+1] / gearRatios[i]

            # Calculate the torque at the next gear using the next gear's estimated RPM
            nextGearTQ = torqueCurve[int(math.floor(nextGearRPM))][1] * gearRatios[i+1]

            # Calculate the difference (torque drop)
            torqueDrop = currentGearTQ - nextGearTQ

            # keep track of the min torque drop and the optimum shift point associated.
            if (abs(torqueDrop) < minTorqueDrop):
                minTorqueDrop = abs(torqueDrop)
                optimumShiftPt = torqueCurve[x][0]

            # If there are none which are less than zero (IE: You loose torque when shiting)
            # shift a red-line
            if (torqueDrop > 0):
                break

        shiftPoints.append(optimumShiftPt)

    # Flip the array before returning, all calculations are done backwards.
    return shiftPoints[::-1]





def legrangeInterpolation(definingPoints):
    
    curve = []
    min = definingPoints[0][0]
    max= definingPoints[len(definingPoints)-1][0]

    for x in np.arange(min, max+0.05, 0.05):
        total=0
        for k in range(len(definingPoints)):
            xi, yi = definingPoints[k]
            total_mul = 1
            for j in range(len(definingPoints)):
                if k == j: continue
                xj, yj = definingPoints[j]
                total_mul *= (x - xj) / float(xi - xj)
            total+= yi * total_mul
        curve.append((x,total))

    return curve


def linearInterpolation(definingPoints):

    curve = []
    min = definingPoints[0][0]
    max= definingPoints[len(definingPoints)-1][0]
    for x in range(0, len(definingPoints)-1):
        rpmBegin = definingPoints[x][0]
        rpmEnd = definingPoints[x+1][0]
        for y in np.arange(rpmBegin, rpmEnd+0.05, 0.05):
            mu2 = (1.0 - math.cos(y*math.pi))/2.0
            drpm = rpmEnd-rpmBegin
            dtorq = definingPoints[x+1][1] - definingPoints[x][1]
            steprpm = y - definingPoints[x][0]
            torqn = definingPoints[x][1] + (steprpm * dtorq/drpm)
            curve.append((y,torqn))

    return curve






