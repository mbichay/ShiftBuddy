
import math
import numpy as np
import matplotlib.pyplot as plt

"""
torque = [172.0, 228.0, 354.0, 360.0, 370.0, 326.0, 230.0, 200.0]
rpm = [1000.0, 2000.0, 3000.0, 4000.0, 5000.0, 6000.0, 7000.0, 8000.0]
gearRatios = [13.93, 8.73, 6.25, 4.63, 3.53, 2.79]
td = 27.32

opt = []
opt2 = []
rpms = []

def main():
    for n in range(len(gearRatios)-2, -1, -1):
        dtorquemin = 999;
        rpmopt = rpm[len(rpm)-1]
        for x in np.arange(rpm[len(rpm)-1], rpm[0], -0.01):
            torquegearL = gettorque(x) * gearRatios[n]
            rpmH = x * gearRatios[n+1] / gearRatios[n]
            torquegearH = gettorque(rpmH) * gearRatios[n+1]
            dtorque = torquegearL - torquegearH;
            if (abs(dtorque) < dtorquemin):
                dtorquemin = abs(dtorque)
                rpmopt = x
            if (dtorque > 0):
                break
        opt.append(rpmopt)


    tq = buildtorquecurves()
    for i in range(len(gearRatios)-2, -1, -1):
        dtorquemin = 99999999
        rpmopt = tq[len(tq)-1]
        for x in range(len(tq)-1,0, -1):
            torquegearL = tq[x] * gearRatios[i]
            rpmH = x * gearRatios[i+1] / gearRatios[i]
            torquegearH = tq[int(round(rpmH,-1))] * gearRatios[i+1]
            dtorque = torquegearL - torquegearH
            if (abs(dtorque) < dtorquemin):
                dtorquemin = abs(dtorque)
                rpmopt = rpms[x]
            if (dtorque>0):
                break
        opt2.append(rpmopt)
    plt.plot(opt,opt2)
    plt.show()


def buildtorquecurves():
    torqueCurve = []
    torqueCurve2 = []

    for rpmIdx1 in range(0, len(rpm)-1):
        rpmBegin = rpm[rpmIdx1]
        rpmEnd = rpm[rpmIdx1+1]
        for rpmIdx2 in np.arange(rpmBegin, rpmEnd, 0.01):
            mu2 = (1.0 - math.cos(rpmIdx2*math.pi)) / 2.0
            torqueCurve2.append(torque[rpmIdx1] * (1.0-mu2) + torque[rpmIdx1+1] * mu2)        

            drpm = rpmEnd - rpmBegin
            dtorq = torque[rpmIdx1+1] - torque[rpmIdx1]
            steprpm = rpmIdx2 - rpm[rpmIdx1]
            torqn = torque[rpmIdx1] + (steprpm * dtorq / drpm)
            torqueCurve.append(torqn)
            rpms.append(rpmIdx2)
   # plt.plot(torqueCurve)
   # plt.show()
    return torqueCurve


def gettorque(rpmn):
    for n in range(len(rpm)-1, 0, -1):
        if (rpmn > rpm[n]) : break

    drpm = rpm[n+1] - rpm[n]
    dtorque = torque[n+1] - torque[n]
    steprpm = rpmn - rpm[n]
    torqn = torque[n] + (steprpm * dtorque / drpm)
    return torqn
    
    """




def legrangeInterpy(definingPoints, minRPM, maxRPM):
    tqCurve = []
    for x in range(minRPM, maxRPM):
        total=0
        for k in xrange(len(definingPoints)):
            xi, yi = definingPoints[k]
            total_mul = 1
            for j in xrange(len(definingPoints)):
                if k == j: continue
                xj, yj = definingPoints[j]
                total_mul *= (x - xj) / float(xi - xj)
            total+= yi * total_mul
        tqCurve.append((x,total))
    return tqCurve



if __name__ == "__main__":
    minRPM = 1000
    maxRPM = 8000
    definingPoints = [(1000.0,172.0), (2000.0,228.0), (3000.0, 354.0), (4000.0, 360.0), (5000.0, 370.0), (6000.0, 326.0), (7000.0, 230.0), (8000.0, 200.0)]

    curve = legrangeInterpy(definingPoints, minRPM, maxRPM)
    plt.plot(*zip(*curve))
    plt.plot(*zip(*definingPoints))
    plt.show()
    print(curve)










