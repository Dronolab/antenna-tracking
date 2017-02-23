import math
import logging
from imu_client import ImuClient


class Antenna():

    # Hardcoded antenna position. Useful when GPS is unavailable
    SATELLITE_DISH_DEFAULT_LATITUDE = 45.4939087
    SATELLITE_DISH_DEFAULT_LONGITUDE = -73.5630330
    SATELLITE_DISH_DEFAULT_ALTITUDE = 14.0

    # Hardcoded magnetic declination
    MAGNETIC_DECLINATION = -14.52

    def __init__(self):
        """ Constructor """

        # Initialize magnetic declination
        self.declination = self.MAGNETIC_DECLINATION

        # Initialize GPS values
        self.alt = self.SATELLITE_DISH_DEFAULT_ALTITUDE
        self.lat = self.SATELLITE_DISH_DEFAULT_LATITUDE
        self.lon = self.SATELLITE_DISH_DEFAULT_LONGITUDE

        # Initialize UAV values
        self.uav_alt = 0
        self.uav_lon = 0
        self.uav_lat = 0

        # Initialize inertial measurement values
        self.roll = 0
        self.pitch = 0
        self.yaw = 0

        # Initialize target values
        self.wyaw = 0
        self.wpitch = 0

        # Initialize IMU
        self.imu = ImuClient()
        self.imu.start()
        self.imu_latency = 0

        # Initialize deadzone
        self._read_imu(5)
        self._bearing_offset = self.yaw

    def update_imu(self):
        """ Get newest values from imu module """

        self.pitch = self.imu.pitch
        self.yaw = self.imu.yaw
        self.imu_latency = self.imu.latency

    def _read_imu(self, n):
        """ Get average next nth values from imu """

        self.imu.read_imu_n_time(n)

    def close(self):
        """ Stop IMU module thread """

        self.imu.kill = True

    def update_angle_offset(self):
        """ Update yaw and wanted yaw with bearing offset angle """

        self.yaw = self._calculate_bearing_offset(
            self.yaw, self._bearing_offset)
        self.wyaw = self._calculate_bearing_offset(
            self.wyaw, self._bearing_offset)

    def update_yaw_from_gps(self):
        """ Update wanted yaw """

        self.wyaw = self._calculate_bearing(
            self.lat, self.lon, self.uav_lat, self.uav_lon)

        # Apply correction using magnetic declination angle
        self.wyaw = self.wyaw - self.declination

    def update_pitch_from_gps(self):
        """ Update wanted pitch """

        self.wpitch = self._calculate_pitch(
            self.lat, self.lon, self.alt, self.uav_lat, self.uav_lon, self.uav_alt)

    def _calculate_pitch(self, lat_sat, long_sat, alt_sat, lat_drone, long_drone, alt_drone):
        """ Calculate the pitch using haversine formula """

        R = 6371000
        lat_sat = math.radians(lat_sat)
        lat_drone = math.radians(lat_drone)
        long_sat = math.radians(long_sat)
        long_drone = math.radians(long_drone)

        delta_long = long_drone - long_sat
        delta_lat = lat_drone - lat_sat

        delta_alt = alt_drone - alt_sat
        a = math.pow(math.sin(delta_lat / 2), 2) + math.cos(lat_sat) * \
            math.cos(lat_drone) * math.pow(math.sin(delta_long / 2), 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        pitch_angle = math.atan2(delta_alt, d)

        pitch_angle = math.degrees(pitch_angle)

        return pitch_angle

    def _calculate_bearing(self, lat_sat, long_sat, lat_drone, long_drone):
        """ Calculate the bearing based on antenna and uav gps coordinates"""

        lat_sat = math.radians(lat_sat)
        lat_drone = math.radians(lat_drone)
        long_sat = math.radians(long_sat)
        long_drone = math.radians(long_drone)
        delta_long = long_drone - long_sat
        delta_lat = lat_drone - lat_sat
        y = math.sin(delta_long) * math.cos(lat_drone)
        x = math.cos(lat_sat) * math.sin(lat_drone) - \
            math.sin(lat_sat) * math.cos(lat_drone) * math.cos(delta_long)
        bearing_initial = math.degrees(math.atan2(y, x))
        return bearing_initial

    def _calculate_bearing_offset(self, angle, bearingangleoffset):
        """ Calculate the bearing offset used to apply a deadzone.

            It makes the antenna easier to operate because we don't
            have to deal with tangled wires.
        """

        newbearing = angle
        newbearing -= bearingangleoffset
        if newbearing > 180:
            newbearing -= 360
        if newbearing < -180:
            newbearing += 360

        return newbearing
