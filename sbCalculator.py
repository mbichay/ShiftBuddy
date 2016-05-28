
import math
import numpy as np
import matplotlib.pyplot as plt


def calculateShiftPoints(gearRatios, definingPoints):
    shiftPoints = []
    torqueCurve = legrangeInterpy(definingPoints)
    #torqueCurve = linearInterpolation(definingPoints)
    shiftPoints.append(torqueCurve[len(torqueCurve)-1][0])

    for i in range(len(gearRatios)-2, -1, -1):
        minTorqueDrop = 9999999.0
        optimumShiftPt = torqueCurve[len(torqueCurve)-1][0]
        for x in range(len(torqueCurve)-1, -1, -1):
            currentGearTQ = torqueCurve[x][1] * gearRatios[i]
            nextGearRPM = x * gearRatios[i+1] / gearRatios[i]
            nextGearTQ = torqueCurve[int(math.floor(nextGearRPM))][1] * gearRatios[i+1]
            torqueDrop = currentGearTQ - nextGearTQ

            if (abs(torqueDrop) < minTorqueDrop):
                minTorqueDrop = abs(torqueDrop)
                optimumShiftPt = torqueCurve[x][0]
            if (torqueDrop > 0):
                break
        shiftPoints.append(optimumShiftPt)
    
    return shiftPoints[::-1]



def legrangeInterpy(definingPoints):
    
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

    plt.plot(*zip(*curve))
    plt.plot(*zip(*definingPoints))
    plt.show()
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

    plt.plot(*zip(*curve))
    plt.plot(*zip(*definingPoints))
    plt.show()
    return curve


if __name__ == "__main__":

    #final1 = 4.77
    #final2 = 3.44
    #gearRatios = [2.92*final1, 1.83*final1, 1.31*final1, 0.97*final1, 1.04*final2, 0.81*final2]
    #definingPoints = [(1500.0,172.0), (2000.0,214.0), (2500.0, 305.0), (3000.0, 368.0) ,(3500.0, 385.0), (4000.0, 392.0), (4500.0, 391.0), (5000.0, 382.0), (5500.0, 361.0), (6000, 333.0), (6500, 298.0)]
    
    #r32
    final1 = 3.94
    final2 = 3.09
    gearRatios = [3.36*final1, 2.09*final1, 1.47*final1, 1.10*final1, 1.11*final2, 0.93*final2]
    definingPoints = [(2500.0, 239.0), (3000.0, 257.5) ,(3500.0, 253.0), (4000.0, 243.8), (4500.0, 248.0), (5000.0, 245.0), (5500.0, 238.0), (6000, 220.0), (6500, 200.0)]
    print(calculateShiftPoints(gearRatios, definingPoints))












