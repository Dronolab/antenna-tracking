import sys
import getopt
import RTIMU
import os.path
import time
import math
import logging
import socket
import threading


class ManualOverride (threading.Thread):

    # Manual override control
    MANUAL_OVERRIDE_BUFFER_SIZE = 1024
    MANUAL_OVERRIDE_LISTENING_IP = "0.0.0.0"
    MANUAL_OVERRIDE_LISTENING_PORT = 5050

    def __init__(self):
        threading.Thread.__init__(self)

        self.manual_override_socket = None
        self.overriden = False
        self.yaw_servo_pwm = 614
        self.pitch_servo_pwm = 614
        self.kill = False
        self.latency = 0
        self.ready = False

        try:
            self.manual_override_socket = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM)
            self.manual_override_socket.bind(
                (self.MANUAL_OVERRIDE_LISTENING_IP, self.MANUAL_OVERRIDE_LISTENING_PORT))
            self.ready = True
        except IOError:
            logging.warning(
                "Cannot establish connection with external controller")

        if self.ready:
            logging.info(
                "Connection with external controller succesfull. Manual override is now possible")
        else:
            logging.error(
                "Can't establish connection. Please check if the external controller is sending data")

    def run(self):
        try:
            while True:
                t0 = time.time()

                self.data, addr = self.manual_override_socket.recvfrom(
                    self.MANUAL_OVERRIDE_BUFFER_SIZE)

                manual_override_json = json.loads(self.data)

                print(self.data)

                t1 = time.time()
                self.latency = (t1 - t0) * 1000

                self.pitch_servo_pwm = 614
                self.yaw_servo_pwm = 614

                if self.kill:
                    logging.info("Closing Manual Override")
                    break

        except KeyboardInterrupt:
            pass

    def close(self):
        """ Trigger thread closure """
        self.kill = True
