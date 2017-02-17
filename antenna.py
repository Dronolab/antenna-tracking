import math
import logging
from servo import Servo
from imu_client import ImuClient

class Antenna():

    def __init__(self):
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.wyaw = 0
        self.wpitch = 0
        self.bearing_offset = 0
        self.uav_alt = 0
        self.uav_lon = 0
        self.uav_lat = 0
        self.alt = 0
        self.lon = 0
        self.lat = 0
        self.declination = -14.52

        self.yaw_servo = Servo(-180, 180, 1.1, 1.9, 1.5, 100, 0, 0.8)
        self.pitch_Servo = Servo(0, 90, 1.1, 1.9, 1.5, 100, 1, 0.5)

        self.imu = ImuClient()
        self.imu.start()

    def updateIMU(self):
        self.pitch = self.imu.pitch
        self.yaw = self.imu.yaw

    def close(self):
        self.imu.kill = True

    def arrow(self, arrow):
        if arrow == 0:
            self.wpitch += 5
        elif arrow == 1:
            self.wyaw += 5
        elif arrow == 2:
            self.wpitch -= 5
        elif arrow == 3:
            self.wyaw -= 5

    def Orientationoffset(self, bearing_offset):
        self.bearing_offset = bearing_offset

    def angleoffsetcalc(self):
        self.yaw = self.bearing_offset(self.yaw, self.bearing_offset)
        self.wyaw = self.bearing_offset(self.wyaw, self.bearing_offset)

    def update_yaw_from_gps(self):
        self.wyaw = self.bearing(
            self.lat, self.lon, self.uav_lat, self.uav_lon)

    def update_pitch_from_gps(self):
        self.wpitch = self.wanted_pitch(
            self.lat, self.lon, self.alt, self.uav_lat, self.uav_lon, self.uav_alt)

    def update_magnetic_declination(self):
        self.wyaw = self.wyaw - self.declination

    def wanted_pitch(self, lat_sat, long_sat, alt_sat, lat_drone, long_drone, alt_drone):
        EARTH_RADIUS = 6371000

=======
    def updateYawFromGPS(self):
        self.wyaw = self.bearing(
            self.lat, self.lon, self.uav_lat, self.uav_lon)

    def updatePitchFromGPS(self):
        self.wpitch = self.pitch(
            self.lat, self.lon, self.alt, self.uav_lat, self.uav_lon, self.uav_alt)

    def magneticDeclinationUpdate(self):
        self.wyaw = self.wyaw - self.declination

    def pitch(self, lat_sat, long_sat, alt_sat, lat_drone, long_drone, alt_drone):
        R = 6371000
        lat_sat = math.radians(lat_sat)
        lat_drone = math.radians(lat_drone)
        long_sat = math.radians(long_sat)
        long_drone = math.radians(long_drone)

        delta_long = long_drone - long_sat
        delta_lat = lat_drone - lat_sat
        delta_alt = alt_drone - alt_sat

        print(alt_drone)
        print(alt_sat)

        a = math.pow(math.sin(delta_lat / 2.0), 2) + math.cos(lat_sat) * \
            math.cos(lat_drone) * math.pow(math.sin(delta_long / 2.0), 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Haversine formula
        d = EARTH_RADIUS * c

        pitch_angle = math.atan2(delta_alt, d)

        pitch_angle = math.degrees(pitch_angle)

        return pitch_angle

    def pitchoffset(self, angle, pitchangleoffset):
        newpitch = angle
        newpitch -= bearingangleoffset
        if newpitch > 180:
            newpitch -= 360
        if newbearing < -180:
            newpitch += 360

        return newbearing

    def bearing(self, lat_sat, long_sat, lat_drone, long_drone):
        lat_sat = math.radians(lat_sat)
        lat_drone = math.radians(lat_drone)
        long_sat = math.radians(long_sat)
        long_drone = math.radians(long_drone)
        delta_long = long_drone - long_sat
        delta_lat = lat_drone - lat_sat
        y = math.sin(delta_long) * math.cos(lat_drone)
        x = math.cos(lat_sat) * math.sin(lat_drone) - \
            math.sin(lat_sat) * math.cos(lat_drone) * math.cos(delta_long)
        # plage de -180 a 180
        bearing_initial = math.degrees(math.atan2(y, x))
        # Pour le mettre dans le plage de 0 a 360
        # bearing_360=(bearing_initial+360)%360
        return bearing_initial

    def bearing_offset(self, angle, bearingangleoffset):
        newbearing = angle
        newbearing -= bearingangleoffset
        if newbearing > 180:
            newbearing -= 360
        if newbearing < -180:
            newbearing += 360

        return newbearing
