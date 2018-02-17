import time
import math

from Utility.abstract_process import processAbstract
import GeneralSettings


class antennaControl(processAbstract):
    def __init__(self, antenna_data, uav_data, actuator_setpoint):
        processAbstract.__init__(self)

        # classes for shared data across multiprocess
        # compre from utility.multiprocessDataType
        self.antenna_data = antenna_data
        self.uav_data = uav_data
        self.actuator_setpoint = actuator_setpoint
        self.period = 0.2  #  200 ms of period might not be optimal
        self.declination = GeneralSettings.MAGNETIC_DECLINATION

    def process(self):
        while self.kill_pill.empty():
            print("antennaControl main process loop")
            start_time = time.time()

            self.get_bearing_from_position()
            self.get_elevation_from_position()

            # this methode is were the main control algorithmes can be implemented,
            # if we dont want to do multiple turns
            self.bearing_get_shortest_path()

            self.update_setpoints()

            time.sleep(self.period)

        self.gracefull_shutdown()

    def gracefull_shutdown(self):
        print("gracefull shutdown")



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

        #pitch_angle = math.degrees(pitch_angle)

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

    def _shortest_path(dest, source):
        """ Calculates shortest circular path in radians.
        """
        dest = math.degrees(dest) + 180
        source = math.degrees(source) + 180
        mod_diff = (dest - source) % m360
        distance = 180 - abs(mod_diff - 180)
        if mod_diff < 180:
            return math.radians(distance)*-1
        else:
            return math.radians(distance)
