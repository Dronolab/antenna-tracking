
class Antenna():

    def __init__(self):
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.wyaw = 0
        self.wpitch = 0
        self.bearingoffset = 0
        self.uavAlt = 0
        self.uavLon = 0
        self.uavLat = 0
        self.antennaAlt = 0
        self.antennaLon = 0
        self.antennaLat = 0
        self.declination = -14.52

    def arrow(self, arrow):
        if arrow == 0:
            self.wpitch += 5
        elif arrow == 1:
            self.wyaw += 5
        elif arrow == 2:
            self.wpitch -= 5
        elif arrow == 3:
            self.wyaw -= 5

    def Orientationoffset(self, bearingoffset):
        self.bearingoffset = bearingoffset

    def angleoffsetcalc(self):
        self.yaw = self.bearingoffset(self.yaw, self.bearingoffset)
        self.wyaw = self.bearingoffset(self.wyaw, self.bearingoffset)

    def updateYawFromGPS(self):
        self.wyaw = self.bearing(
            self.antennaLat, self.antennaLon, self.uavLat, self.uavLon)

    def updatePitchFromGPS(self):
        self.wpitch = self.pitch(
            self.antennaLat, self.antennaLon, self.antennaAlt, self.uavLat, self.uavLon, self.uavAlt)

    def magneticDeclinationUpdate(self):
        self.wyaw = self.wyaw - self.declination

    def pitch(self, lat_sat, long_sat, alt_sat, lat_drone, long_drone,
              alt_drone):

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

    def bearingoffset(self, angle, bearingangleoffset):
        newbearing = angle
        newbearing -= bearingangleoffset
        if newbearing > 180:
            newbearing -= 360
        if newbearing < -180:
            newbearing += 360

        return newbearing
