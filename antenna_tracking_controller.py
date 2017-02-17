import json
import socket
import logging
import struct
import sys
import Adafruit_PCA9685
from antenna import Antenna
from unmanned_aerial_vehicule import UnmannedAerialVehicule
from servo import Servo
import time
import os


class AntennaTrackingController:

    # Constants
    LISTENING_IP = "0.0.0.0"
    LISTENING_PORT = 5008
    PMW_FREQUENCY = 60
    SERVO_MIN = 150
    SERVO_MAX = 600
    SATELLITE_DISH_DEFAULT_LATITUDE = 45.4946761
    SATELLITE_DISH_DEFAULT_LONGITUDE = -73.5622961
    SATELLITE_DISH_DEFAULT_ALTITUDE = 14000
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

        # Setup antenna
        self.antenna = Antenna()

        # Antenna GPS coordinates (hardcoded at this moment)
        self.antenna.lat = self.SATELLITE_DISH_DEFAULT_LATITUDE
        self.antenna.lon = self.SATELLITE_DISH_DEFAULT_LONGITUDE
        self.antenna.alt = self.SATELLITE_DISH_DEFAULT_ALTITUDE

        # Init servo
        self.yaw_servo = Servo(-180, 180, 1.1, 1.9, 1.5, 100, 0, 0.8)
        self.pitch_servo = Servo(0, 90, 1.1, 1.9, 1.5, 100, 1, 0.5)

        # Read current position
        while True:

            # Update antenna
            self.antenna.updateIMU()

            # Update UAV
            data, addr = self.uav.receive_telemetry()
            drone_gps = json.loads(data)

            if drone_gps['packet_id'] != self.MAVLINK_GPS_ID:
                continue

            drone_gps["alt"] = drone_gps["alt"]

            self.antenna.uav_alt = drone_gps["alt"]
            self.antenna.uav_lat = drone_gps["lat"]
            self.antenna.uav_lon = drone_gps["lon"]
            self.antenna.update_yaw_from_gps()
            self.antenna.update_pitch_from_gps()
            self.antenna.update_magnetic_declination()

            tick_yaw = self.yaw_servo.refresh(
                self.antenna.wyaw, self.antenna.yaw)
            self.pwm.set_pwm(self.yaw_servo.channel, 0, tick_yaw)

            tick_pitch = self.pitch_servo.refresh(
                self.antenna.wpitch, self.antenna.pitch)
            self.pwm.set_pwm(self.pitch_servo.channel, 0, tick_pitch)

            time.sleep(0.2)

            os.system("clear")

            print("[UAV]")
            print("\tLatitude\t" + str(drone_gps["lat"]))
            print("\tLongitude\t" + str(drone_gps["lon"]))
            print("\tAltitude\t" + str(drone_gps["alt"]))

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
        self.pwm.set_pwm(self.yaw_servo.channel, 0,
                         (self.SERVO_MAX - self.SERVO_MIN) / 2.0 + self.SERVO_MIN)
        self.pwm.set_pwm(self.pitch_servo.channel, 0,
                         (self.SERVO_MAX - self.SERVO_MIN) / 2.0 + self.SERVO_MIN)

    def get_gpsdata(self):
        data, addr = sock.recvfrom(1024)
        print "gps_data:", data

    def get_IMUdata(self):
        IMU_data, addr = sock.recvfrom(1024)
        pitch, yaw, roll = struct.unpack("ddd", IMU_data)

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
