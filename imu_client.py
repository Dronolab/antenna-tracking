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
        self.latency = 0
        self.ready = imu_setup.imu_init_success

        if self.ready:
            logging.info("IMU started successfully")
        else:
            logging.error(
                "IMU failed to initialize. Please check imu_setup.py or the MPU-92/65 unit")

    def run(self):
        try:
            while True:
                t0 = time.time()
                fusionPose = imu_setup.ReadSingleIMU()
                t1 = time.time()
                self.latency = (t1 - t0) * 1000

                if fusionPose is not None:
                    self.roll = math.degrees(fusionPose[0])
                    self.pitch = math.degrees(fusionPose[1])
                    self.yaw = math.degrees(fusionPose[2])
                if self.kill:
                    logging.info("Closing IMU Thread")
                    break

        except KeyboardInterrupt:
            pass

    def read_imu_n_time(self, n):
        imu_setup.ReadImu(self, n)
