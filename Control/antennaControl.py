import GeneralSettings
from Utility.abstract_process import processAbstract
from Actuator.pitch_servo import PitchServo
from Actuator.yaw_servo import YawServo
from Sensors.imuYaw import imuYaw
from Sensors.imuPitch import imuPitch
from Vehicle.uavInteraction import mavlinkHandler
#from debugger import Debugger
from Sensors.gps import GPSClient
import time
import math
import sys
from multiprocessing import Value


class antennaControl(processAbstract):
    def __init__(self, antenna_data, uav_data, actuator_setpoint):
        processAbstract.__init__(self)
        # classes for shared data across multiprocess
        # compre from utility.multiprocessDataType
        self.antenna_data = antenna_data
        self.uav_data = uav_data
        self.actuator_setpoint = actuator_setpoint
#        self.period = 0.2  #  200 ms of period might not be optimal
        self.antenna_data.setYawOffset(math.radians(
            GeneralSettings.MAGNETIC_DECLINATION))
        self.yaw = YawServo(
            self.antenna_data,
            self.actuator_setpoint,
            GeneralSettings.servo_yaw_pin,
            0, 0)
        self.pitch = PitchServo(  # processAbstract):
            self.antenna_data,
            self.actuator_setpoint,
            GeneralSettings.servo_yaw_pin,
            math.radians(10), math.radians(70))
        self.imuYaw = imuYaw(self.antenna_data)
        self.imuPitch = imuPitch(self.antenna_data)
        self.uav = mavlinkHandler(self.uav_data)
        self.antenna_data.setLon(GeneralSettings.default_lon)
        self.antenna_data.setLat(GeneralSettings.default_lat)
        self.antenna_data.setAlt(GeneralSettings.default_rel_alt)
        #self.debugger = Debugger(self.antenna_data, self.uav_data, self.actuator_setpoint)
        self.gps = GPSClient(self.antenna_data)
        self.running = False

    def process(self):
        if not self.running:
            self.gps.start()
            self.imuYaw.start()
            self.imuPitch.start()
            self.uav.start()
            self.yaw.start()
            self.pitch.start()
        self.running = True

        while self.running:
            self.actuator_setpoint.setPitch(self._calculate_pitch(
                self.antenna_data.getLat(),
                self.antenna_data.getLon(),
                self.antenna_data.getAlt(),
                self.uav_data.getLat(),
                self.uav_data.getLon(),
                self.uav_data.getAlt()))

            _bearing = self._calculate_bearing(
                self.antenna_data.getLat(),
                self.antenna_data.getLon(),
                self.uav_data.getLat(),
                self.uav_data.getLon())

            self.actuator_setpoint.setYaw(
                _bearing + self.antenna_data.getYawOffset())
            time.sleep(0.1)

    def stop(self):
        self.running = False

    def soft_stop_everything(self):
        self.running = False
        self.yaw.soft_process_stop()
        self.pitch.soft_process_stop()
        self.gps.soft_process_stop()
        self.imuYaw.soft_process_stop()
        self.imuPitch.soft_process_stop()
        self.uav.soft_process_stop()
        # time.sleep(1)
#        self.start()

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
        bearing_initial = math.atan2(y, x)

        return bearing_initial
