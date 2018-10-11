import os
import sys
import RTIMU
import schedule
import GeneralSettings
from Utility.abstract_process import processAbstract
import time


class imuHandler(processAbstract):
    #SETTINGS_FILE = GeneralSettings.IMU_SETTINGS_FILE

    def __init__(self, antenna_data):
        processAbstract.__init__(self)
        self.antenna_data = antenna_data
        self.ready = False
        self.first = True

    def job(self):
        """ Abstract """
        raise

    def process(self):
        print("Using settings file " + self.SETTINGS_FILE + ".ini")
            #print("Settings file does not exist, will be created")
            # if not os.path.exists(self.SETTINGS_FILE + ".ini"):

        s = RTIMU.Settings(self.SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(s)

        if (not self.imu.IMUInit()):
            print("IMU Init Failed", self.SETTINGS_FILE)
            sys.exit(1)
        else:
            print("IMU Init Succeeded")
            self.ready = True

        # initialising fusion parameters
        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)
        self.poll_interval = self.imu.IMUGetPollInterval()
        while self.kill_pill.empty():
            self.job()
            time.sleep(10 / 1000)
