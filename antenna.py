import math
import os
import logging
import Adafruit_PCA9685
from imu_client import ImuClient
from unmanned_aerial_vehicule import UnmannedAerialVehicule
from yaw_servo import YawServo
from pitch_servo import PitchServo


class Antenna():

    # Hardcoded antenna position. Useful when GPS is unavailable
    SATELLITE_DISH_DEFAULT_LATITUDE = 45.4939087
    SATELLITE_DISH_DEFAULT_LONGITUDE = -73.5630330
    SATELLITE_DISH_DEFAULT_ALTITUDE = 14.0

    # Usually it's 60Hz but in this case we want it to go to 100Hz
    PMW_FREQUENCY = 100  # Hz

    # Hardcoded magnetic declination
    MAGNETIC_DECLINATION = -14.52

    def __init__(self):
        """ Constructor """

        logging.info(
            'Started Antenna tracking system. Beginning initialization...')

        self.ready = False

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

        # Setup UAV
        self.uav = UnmannedAerialVehicule()
        self.uav.start()

        self.is_pwm_ready = False

        # Setup pwm
        try:
            self._pwm = Adafruit_PCA9685.PCA9685()
            self._pwm.set_pwm_freq(self.PMW_FREQUENCY)
            self.is_pwm_ready = True
        except IOError:
            logging.error(
                "PWM module failed to initialize. Please check if the adafruit hat is plugged in the Raspberry Pi GPIO pins.")

        # Init servos
        self.yaw_servo = YawServo(-180, 180, 1.1, 1.9, 100, 0, 0.8)
        self.pitch_servo = PitchServo(0, 90, 1.1, 1.9, 100, 1, 0.5)

        # Health check on every component
        if self.imu.ready and self.uav.ready and self.is_pwm_ready:
            self.ready = True

        if self.ready:
            logging.info(
                'Antenna tracking system successfully started. Ctrl-C to stop...')

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

        self.uav.close()

        if not self.is_pwm_ready:
            return

        # Set yaw servo to neutral position (will stop the servo movement)
        self.tick_yaw = 614
        self._pwm.set_pwm(self.yaw_servo.channel, 0, self.tick_yaw)

        # Set pitch servo to neutral position (will stop the servo movement)
        self.tick_pitch = 614
        self._pwm.set_pwm(self.pitch_servo.channel, 0, self.tick_pitch)

    def update_target_orientation(self):
        # Transfer UAV coordinates into the antenna
        self.uav_alt = self.uav.alt
        self.uav_lat = self.uav.lat
        self.uav_lon = self.uav.lon

        self.update_imu()
        self.update_yaw_from_gps()
        self.update_pitch_from_gps()
        self.update_angle_offset()

        # Update yaw servo
        self.tick_yaw = self.yaw_servo.refresh(
            self.wyaw, self.yaw)
        self._pwm.set_pwm(self.yaw_servo.channel, 0, self.tick_yaw)

        # Update pitch servo
        self.tick_pitch = self.pitch_servo.refresh(
            self.wpitch, self.pitch)
        self._pwm.set_pwm(self.pitch_servo.channel, 0, self.tick_pitch)

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

    def print_current_data(self):
        os.system("clear")

        print("[UAV]")
        print("\tLatitude\t" + str(self.uav_lat))
        print("\tLongitude\t" + str(self.uav_lon))
        print("\tAltitude\t" + str(self.uav_alt))
        print("\tLatency\t\t" + str(self.uav.latency) + "ms")

        print("[Antenna]")
        print("\tLatitude\t" + str(self.lat))
        print("\tLongitude\t" + str(self.lon))
        print("\tAltitude\t" + str(self.alt) + "m")

        print("[IMU]")
        print("\tYaw\t\t" + str(self.yaw))
        print("\tWanted yaw\t" + str(self.wyaw))
        print("\tPitch\t\t" + str(self.pitch))
        print("\tWanted pitch\t" + str(self.wpitch))
        print("\tLatency\t\t" +
              "{0:.2f}".format(round(self.imu_latency, 2)) + "ms")

        print("[Servos]")
        print("\tYaw tick\t" + str(self.tick_yaw))
        print("\tPitch tick\t" + str(self.tick_pitch))
