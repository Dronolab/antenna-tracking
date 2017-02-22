import json
import socket
import logging
import struct
import sys
import Adafruit_PCA9685
from antenna import Antenna
from unmanned_aerial_vehicule import UnmannedAerialVehicule
import time
import os
import imu_client
from servo import Servo


class AntennaTrackingController:
    """ This class will controll all antenna calculation loop.

        It has the responsability to ensure we can fetch all neccessary data in
        order to make the system working properly
    """

    # Usually it's 60Hz but in this case we want it to go to 100Hz
    PMW_FREQUENCY = 100  # Hz

    # MAVLink packet id for GPS. See:
    # https://pixhawk.ethz.ch/mavlink/#GLOBAL_POSITION_INT
    MAVLINK_GPS_ID = 33

    def __init__(self):
        """ Constructor """

        # Setup pwm
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(self.PMW_FREQUENCY)

    def start(self):
        """ Start execution of the main loop

            This is the central point of the antenna tracking system. It put
            all together the data and trigger calculations. Then a nice
            output is given to STDOUT.
        """

        # Display some funky ascii
        self.greeting()

        # Setup UAV
        self.uav = UnmannedAerialVehicule()
        self.uav.start()

        # Init servos
        self.yaw_servo = Servo(-180, 180, 1.1, 1.9, 1.5, 100, 0, 0.8)
        self.pitch_servo = Servo(0, 90, 1.1, 1.9, 1.5, 100, 1, 0.5)

        #
        # Setup antenna tracking system
        #
        self.antenna = Antenna()

        while True:

            # Transfer UAV coordinates into the antenna
            self.antenna.uav_alt = self.uav.alt
            self.antenna.uav_lat = self.uav.lat
            self.antenna.uav_lon = self.uav.lon

            # Get IMU data
            self.antenna.update_imu()

            self.antenna.update_yaw_from_gps()
            self.antenna.update_pitch_from_gps()
            self.antenna.update_angle_offset()

            # Update yaw servo
            tick_yaw = self.yaw_servo.refresh(
                self.antenna.wyaw, self.antenna.yaw)
            self.pwm.set_pwm(self.yaw_servo.channel, 0, tick_yaw)

            # Update pitch servo
            tick_pitch = self.pitch_servo.refresh(
                self.antenna.wpitch, self.antenna.pitch)
            self.pwm.set_pwm(self.pitch_servo.channel, 0, tick_pitch)

            #
            # Print live data
            #

            time.sleep(0.2)

            os.system("clear")

            print("[UAV]")
            print("\tLatitude\t" + str(self.antenna.uav_lat))
            print("\tLongitude\t" + str(self.antenna.uav_lon))
            print("\tAltitude\t" + str(self.antenna.uav_alt))
            print("\tLatency\t\t" + str(self.uav.latency) + "ms")

            print("[Antenna]")
            print("\tLatitude\t" + str(self.antenna.lat))
            print("\tLongitude\t" + str(self.antenna.lon))
            print("\tAltitude\t" + str(self.antenna.alt) + "m")

            print("[IMU]")
            print("\tYaw\t\t" + str(self.antenna.yaw))
            print("\tWanted yaw\t" + str(self.antenna.wyaw))
            print("\tPitch\t\t" + str(self.antenna.pitch))
            print("\tWanted pitch\t" + str(self.antenna.wpitch))

            print("[Servos]")
            print("\tYaw tick\t" + str(tick_yaw))
            print("\tPitch tick\t" + str(tick_pitch))

    def stop(self):
        """ Gracefully stop antenna tracking controller """

        logging.info('Closing antenna tracking system')

        # Close threads
        self.antenna.close()
        self.uav.close()

        # Set yaw servo to neutral position (will stop the servo movement)
        tick_yaw = 614
        self.pwm.set_pwm(self.yaw_servo.channel, 0, tick_yaw)

        # Set pitch servo to neutral position (will stop the servo movement)
        tick_pitch = 614
        self.pwm.set_pwm(self.pitch_servo.channel, 0, tick_pitch)

    def greeting(self):
        """ Welcome message """

        print("""
  ___        _                           _                  _    _
 / _ \      | |                         | |                | |  (_)
/ /_\ \_ __ | |_ ___ _ __  _ __   __ _  | |_ _ __ __ _  ___| | ___ _ __   __ _
|  _  | '_ \| __/ _ \ '_ \| '_ \ / _` | | __| '__/ _` |/ __| |/ / | '_ \ / _` |
| | | | | | | ||  __/ | | | | | | (_| | | |_| | | (_| | (__|   <| | | | | (_| |
\_| |_/_| |_|\__\___|_| |_|_| |_|\__,_|  \__|_|  \__,_|\___|_|\_\_|_| |_|\__, |
                                                                          __/ |
        _.--l--._                                                        |___/
     .`    |     `.
   .` `.    |    .` `.
 .`     `   |  .`     `.     POWERED BY DRONOLAB
/ __       .|.`      __ \    Source code: github.com/dronolab/antenna_tracking
|   ''--._  V  _.--''   |    License: MIT
|        _ (") _        |
| __..--'   ^   '--..__ | _
\\         .`|`.         /-.)
 `.     .`  |  `.     .`
   `. .`    |    `. .`
     `._    |    _.`|
         `--l--` |  |
                 / . \\
                / / \\ \\
               / /   \\ \\
        """)
