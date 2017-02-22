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

    # Constants
    LISTENING_IP = "0.0.0.0"
    LISTENING_PORT = 5008
    PMW_FREQUENCY = 100
    SATELLITE_DISH_DEFAULT_LATITUDE = 45.4939087
    SATELLITE_DISH_DEFAULT_LONGITUDE = -73.5630330
    SATELLITE_DISH_DEFAULT_ALTITUDE = 14.0

    MAVLINK_GPS_ID = 33

    def __init__(self):
        self.greeting()
        # Setting up the pwm
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(self.PMW_FREQUENCY)

        # Entry point of Antenna GPS position
        # gps_ = gpsreader('antgps.txt')

        # Entry point of UAV GPS position
        # uavtxt = gpsreader('uavgps.txt')

    def start(self):
        # Setup UAV
        self.uav = UnmannedAerialVehicule(
            AntennaTrackingController.LISTENING_IP,
            AntennaTrackingController.LISTENING_PORT)
        self.uav.create_bind_socket()

        # Init servos
        self.yaw_servo = Servo(-180, 180, 1.1, 1.9, 1.5, 100, 0, 0.8)
        self.pitch_servo = Servo(0, 90, 1.1, 1.9, 1.5, 100, 1, 0.5)

        # Setup Antenna
        self.antenna = Antenna()

        self.antenna.lat = self.SATELLITE_DISH_DEFAULT_LATITUDE
        self.antenna.lon = self.SATELLITE_DISH_DEFAULT_LONGITUDE
        self.antenna.alt = self.SATELLITE_DISH_DEFAULT_ALTITUDE

        self.antenna.ReadImu(5)
        self.antenna.Orientationoffset(self.antenna.yaw)

        #
        old_ms_boot_time = 0

        # Setup IMU

        while True:
            data, addr = self.uav.receive_telemetry()

            drone_gps = json.loads(data)

            if drone_gps['packet_id'] != self.MAVLINK_GPS_ID:
                continue

            # Transfer UAV coordinates into the antenna

            print("Delta mavlink packets reception time: " +
                  str(drone_gps["time_boot_ms"] - old_ms_boot_time))
            old_ms_boot_time = drone_gps["time_boot_ms"]
            self.antenna.uav_alt = float(drone_gps["alt"]) / 1000
            self.antenna.uav_lat = float(drone_gps["lat"]) / 10000000
            self.antenna.uav_lon = float(drone_gps["lon"]) / 10000000

            # Get IMU data
            self.antenna.updateIMU()

            self.antenna.updateYawFromGPS()
            self.antenna.updatePitchFromGPS()

            self.antenna.angleoffsetcalc()

            # Update servos
            tick_yaw = self.yaw_servo.refresh(
                self.antenna.wyaw, self.antenna.yaw)

            self.pwm.set_pwm(self.yaw_servo.channel, 0, tick_yaw)

            tick_pitch = self.pitch_servo.refresh(
                self.antenna.wpitch, self.antenna.pitch)
            self.pwm.set_pwm(self.pitch_servo.channel, 0, tick_pitch)

            time.sleep(0.2)

            os.system("clear")

            print("[UAV]")
            print("\tLatitude\t" + str(self.antenna.uav_lat))
            print("\tLongitude\t" + str(self.antenna.uav_lon))
            print("\tAltitude\t" + str(self.antenna.uav_alt))

            print("[Antenna]")
            print("\tLatitude\t" + str(self.antenna.lat))
            print("\tLongitude\t" + str(self.antenna.lon))
            print("\tAltitude\t" + str(self.antenna.alt))

            print("[IMU]")
            print("\tYaw\t\t" + str(self.antenna.yaw))
            print("\tWanted yaw\t" + str(self.antenna.wyaw))
            print("\tPitch\t\t" + str(self.antenna.pitch))
            print("\tWanted pitch\t" + str(self.antenna.wpitch))

            print("[Servos]")
            print("\tYaw tick\t" + str(tick_yaw))
            print("\tPitch tick\t" + str(tick_pitch))

    #
    # Gracefully stop antenna tracking controller
    #
    def stop(self):
        logging.info('Closing antenna tracking system')
        self.antenna.close()

        tick_yaw = 614
        self.pwm.set_pwm(self.yaw_servo.channel, 0, tick_yaw)

        tick_pitch = 614
        self.pwm.set_pwm(self.pitch_servo.channel, 0, tick_pitch)

    def get_gpsdata(self):
        data, addr = sock.recvfrom(1024)
        print "gps_data:", data

    # def get_IMUdata(self):
    #    IMU_data, addr = sock.recvfrom(1024)
    #    pitch, yaw, roll = struct.unpack("ddd", IMU_data)

    def servo_move(pitch_drone, pitch_antenna, bearing_drone, bearing_antenna):
        delta_pitch = pitch_drone - pitch_antenna
        delta_bearing = bearing_drone - bearing_antenna

    def greeting(self):
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
