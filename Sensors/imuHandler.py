
import os, sys
import time
from Utility.abstract_process import processAbstract
import RTIMU

import GeneralSettings


class imuHandler(processAbstract):
    SETTINGS_FILE = GeneralSettings.IMU_SETTINGS_FILE
    def __init__(self,antenna_data):
        processAbstract.__init__(self)
        self.antenna_data = antenna_data

    def process(self):
        print("Using settings file " + self.SETTINGS_FILE + ".ini")
        if not os.path.exists(self.SETTINGS_FILE + ".ini"):
            print("Settings file does not exist, will be created")

        s = RTIMU.Settings(self.SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(s)

        if (not self.imu.IMUInit()):
            print("IMU Init Failed")
            sys.exit(1)
        else:
            print("IMU Init Succeeded")

        # initialising fusion parameters
        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)
        self.poll_interval = self.imu.IMUGetPollInterval()

        print("Recommended Poll Interval: %dmS\n" % self.poll_interval)

        while self.kill_pill.empty():
            if self.imu.IMURead():

                pitch, roll, yaw = self.imu.getFusionData()
                self.antenna_data.setPitch(pitch)
                self.antenna_data.setRoll(roll)
                self.antenna_data.setYaw(yaw)

            time.sleep(self.poll_interval * 1.0 / 1000.0)