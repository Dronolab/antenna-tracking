import json
import math
import socket
import struct
import Adafruit_PCA9685


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
        # Setting up the pwm
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(self.PMW_FREQUENCY)

    def start(self):
        # Create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print "Socket created"
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print "Socket binded"
        self.sock.bind((self.LISTENING_IP, self.LISTENING_PORT))

        # Antenna coordinates

        #
        # TODO: Quand on aura du GPS, faire du handling pour ne pas prendre la
        # latitude et longitude par defaut
        #
        self.antenna_latitude = self.SATELLITE_DISH_DEFAULT_LATITUDE
        self.antenna_longitude = self.SATELLITE_DISH_DEFAULT_LONGITUDE
        self.antenna_altitude = self.SATELLITE_DISH_DEFAULT_ALTITUDE

        while True:
            data, addr = self.sock.recvfrom(1024)
            drone_gps = json.loads(data)
            if drone_gps['packet_id'] != self.MAVLINK_GPS_ID:
                continue

            lat_drone = float(drone_gps['lat'])
            lon_drone = float(drone_gps['lon'])
            alt_drone = float(drone_gps['alt'])

            self.bearing_diff = self.bearing(
                self.antenna_latitude,
                self.antenna_longitude,
                lat_drone, lon_drone
            )

            self.pitch_diff = self.pitch(
                self.antenna_latitude,
                self.antenna_longitude,
                self.antenna_altitude,
                lat_drone, lon_drone,
                alt_drone
            )

        print(self.bearing_diff)

    #
    # Gracefully stop antenna tracking controller
    #
    def stop(self):
        print("Antenna tracking stopped")
        self.sock.close()

    def get_gpsdata(self):
        data, addr = sock.recvfrom(1024)
        # print "gps_data:", data

    def get_IMUdata(self):
        IMU_data, addr = sock.recvfrom(1024)
        pitch, yaw, roll = struct.unpack("ddd", IMU_data)

    def servo_move(pitch_drone, pitch_antenna, bearing_drone, bearing_antenna):
        delta_pitch = pitch_drone - pitch_antenna
        delta_bearing = bearing_drone - bearing_antenna
