from multiprocessing import Queue
import os
import random
import time
import math

from Utility.MultiprocessDataType import imuData
import GeneralSettings

class ImuClient:

    def __init__(self, antennaImuData):
        self.poll_interval = 0.004 # 4 ms of poll interval
        self.imuData = antennaImuData


    def mainProcess(self, killpill):
        tmp_pitch= 0
        tmp_roll = 0
        tmp_yaw = 0

        while killpill.empty():
            tmp_pitch, tmp_roll, tmp_yaw = self.getImuAttitude(tmp_pitch,tmp_yaw)

            # print("total values %lf , %lf, %lf" % (tot_lat, tot_lon, tot_alt))

            self.imuData.setPitch(float(tmp_pitch))
            self.imuData.setYaw(float(tmp_yaw))

            print("Pitch : %lf , yaw :%lf" % (self.imuData.getPitch(), self.imuData.getYaw()))
            time.sleep(self.poll_interval)


    def getImuAttitude(self,last_pitch,last_yaw):

        # the random match the inprecision of the gps
        bias = 0.005 * random.randint(-1, 1)
        pitch = (last_pitch + bias) * (1 + random.uniform(-0.001, 0.001))

        if(pitch > math.radians(90)):
            pitch = math.radians(90)
        if (pitch < math.radians(-90)):
            pitch = math.radians(-90)
        if pitch == 0:
           pitch =  pitch + bias * 100

        yaw = (last_yaw + bias) * (1 + random.uniform(-0.001, 0.001))
        if (yaw < 0):
            yaw = 0
        if (yaw > math.radians(360)):
            yaw = math.radians(360)
        if yaw == 0:
            yaw  = yaw + bias * 100

        return pitch, 0, yaw

x = ImuClient(imuData())
x.mainProcess(Queue())
