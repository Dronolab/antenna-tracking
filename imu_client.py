import sys
import getopt
import RTIMU
import os.path
import time
import math
import logging
import threading
import imu_setup


class ImuClient (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.roll = 0
        self.yaw = 0
        self.pitch = 0
        self.kill = False

    def run(self):

        try:
            while True:
                fusionPose = imu_setup.ReadSingleIMU()
                if fusionPose is not None:
                    self.roll = math.degrees(fusionPose[0])
                    self.pitch = math.degrees(fusionPose[1])
                    self.yaw = math.degrees(fusionPose[2])

                if self.kill:
                    logging.info("Closing IMU Thread")
                    break

        except KeyboardInterrupt:
            pass
