from multiprocessing import Value

class attitudeData:
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


class imuData(attitudeData):
   def __init__(self):
       attitudeData.__init__()
       self.unix = Value('d', 0)

   def setUnix(self, unix):
       self.unix.value = unix

   def getUnix(self):
       return self.unix.value


class gpsData:
   def __init__(self):
       self.alt = Value('d', 0)
       self.lon = Value('d', 0)
       self.lat = Value('d', 0)
       self.unix = Value('d', 0)

   def setUnix(self, unix):
       self.unix.value = unix

   def getUnix(self):
       return self.unix.value

   def setAlt(self, alt):
       self.alt.value = alt

   def setLon(self, lon):
       self.lon.value = lon

   def seLat(self, lat):
       self.lat.value = lat

   def getAlt(self):
       return self.alt.value

   def getLon(self):
       return self.lon.value

   def getLat(self):
       return self.lat.value