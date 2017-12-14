import sys
import getopt
import RTIMU
import os.path
import time
import math
import logging

imu_init_success = True

# IMU init
k = 0
if k == 0:
    SETTINGS_FILE = "RTIMULib"

    if not os.path.exists(SETTINGS_FILE + ".ini"):
        imu_init_success = False
        print("Settings file does not exist, will be created")

    s = RTIMU.Settings(SETTINGS_FILE)
    imu = RTIMU.RTIMU(s)

    if (not imu.IMUInit()):
        imu_init_success = False

    imu.setSlerpPower(0.02)
    imu.setGyroEnable(True)
    imu.setAccelEnable(True)
    imu.setCompassEnable(True)

    poll_interval = imu.IMUGetPollInterval()

    k = 1

# Read Imu number for X time and return the average value


def ReadImu(accel, x):
    r = 0
    p = 0
    y = 0
    i = 0
    # Collect IMU Data X times and calcue an average
    while i < x:
        if imu.IMURead():
            data = imu.getIMUData()  # Read IMU data
            fusionPose = data["fusionPose"]
            #print("r: %f p: %f y: %f" %(math.degrees(fusionPose[0]), math.degrees(fusionPose[1]),math.degrees(fusionPose[2])))
            r = r + math.degrees(fusionPose[0])
            p = p + math.degrees(fusionPose[1])
            y = y + math.degrees(fusionPose[2])
            i = i + 1

    accel.roll = r / x
    accel.pitch = p / x
    accel.yaw = y / x

    return 1


# return a array of 3 angle : first : roll 2nd : pitch , 3rd : yaw
def ReadSingleIMU():
    if imu.IMURead():
        data = imu.getIMUData()  # Read IMU data
        fusionPose = data["fusionPose"]

        time.sleep(imu.IMUGetPollInterval() * 0.001)
        return fusionPose
    else:
        time.sleep(imu.IMUGetPollInterval() * 0.001)
        return None
