from multiprocessing import Value


class antenna_shared_data:
    def __init__(self):
        self.alt = Value('d', 0)
        self.lon = Value('d', 0)
        self.lat = Value('d', 0)
        self.pitch = Value('d', 0)
        self.roll = Value('d', 0)
        self.yaw = Value('d', 0)
        self.roll_offset = Value('d', 0)
        self.yaw_offset = Value('d', 0)

    def setAlt(self, alt):
        self.alt.value = alt

    def setLon(self, lon):
        self.lon.value = lon

    def setLat(self, lat):
        self.lat.value = lat

    def getAlt(self):
        return self.alt.value

    def getLon(self):
        return self.lon.value

    def getLat(self):
        return self.lat.value

    def setPitch(self, pitch):
        self.pitch.value = pitch

    def setRoll(self, roll):
        self.roll.value = roll

    def setYaw(self, yaw):
        self.yaw.value = yaw

    def getPitch(self):
        return self.pitch.value

    def getRoll(self):
        return self.roll.value

    def getYaw(self):
        return self.yaw.value

    def getYawOffset(self):
        return self.yaw_offset.value

    def setYawOffset(self, yaw_offset):
        self.yaw_offset.value = yaw_offset

    def getPitchOffset(self):
        return self.pitch_offset.value

    def setPitchOffset(self, pitch_offset):
        self.pitch_offset.value = pitch_offset


class uav_shared_data:
    def __init__(self):
        self.alt = Value('d', 0)
        self.lon = Value('d', 0)
        self.lat = Value('d', 0)

    def setAlt(self, alt):
        self.alt.value = alt

    def setLon(self, lon):
        self.lon.value = lon

    def setLat(self, lat):
        self.lat.value = lat

    def getAlt(self):
        return self.alt.value

    def getLon(self):
        return self.lon.value

    def getLat(self):
        return self.lat.value


class setpoint_shared_data:
    def __init__(self):
        self.pitch = Value('d', 0)
        self.roll = Value('d', 0)
        self.yaw = Value('d', 0)

    def setPitch(self, pitch):
        self.pitch.value = pitch

    def setRoll(self, roll):
        self.roll.value = roll

    def setYaw(self, yaw):
        self.yaw.value = yaw

    def getPitch(self):
        return self.pitch.value

    def getRoll(self):
        return self.roll.value

    def getYaw(self):
        return self.yaw.value
