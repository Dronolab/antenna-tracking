import json
import socket
import logging
import struct
import sys
import Adafruit_PCA9685
from antenna import Antenna
from unmanned_aerial_vehicule import UnmannedAerialVehicule


class AntennaTrackingController:

    # Constants
    LISTENING_IP = "0.0.0.0"
    LISTENING_PORT = 5008
    PMW_FREQUENCY = 60
    SERVO_MINIMUM_POSITIVE_PULSE_LENGTH = 200
    SERVO_MINIMUM_NEGATIVE_PULSE_LENGTH = 450
    SATELLITE_DISH_DEFAULT_LATITUDE = 45.4946761
    SATELLITE_DISH_DEFAULT_LONGITUDE = -73.5622961
    SATELLITE_DISH_DEFAULT_ALTITUDE = 14
    MAVLINK_GPS_ID = 33

    def __init__(self):
        self.greeting()
        # Setting up the pwm
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(self.PMW_FREQUENCY)

    def start(self):
        # Setup UAV
        self.uav = UnmannedAerialVehicule(
            AntennaTrackingController.LISTENING_IP,
            AntennaTrackingController.LISTENING_PORT)
        self.uav.create_bind_socket()

        # Antenna coordinates
        self.antenna_latitude = self.SATELLITE_DISH_DEFAULT_LATITUDE
        self.antenna_longitude = self.SATELLITE_DISH_DEFAULT_LONGITUDE
        self.antenna_altitude = self.SATELLITE_DISH_DEFAULT_ALTITUDE

        self.antenna = Antenna()

        while True:
            data, addr = self.uav.receive_telemetry()
            drone_gps = json.loads(data)

            if drone_gps['packet_id'] != self.MAVLINK_GPS_ID:
                continue

            lat_drone = drone_gps['lat']
            lon_drone = drone_gps['lon']
            alt_drone = drone_gps['alt']

    #
    # Gracefully stop antenna tracking controller
    #
    def stop(self):
        logging.info('Closing antenna tracking system')

    def get_gpsdata(self):
        data, addr = sock.recvfrom(1024)
        # print "gps_data:", data

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
