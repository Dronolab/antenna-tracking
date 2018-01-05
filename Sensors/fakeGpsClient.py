from multiprocessing import Queue
import os
import random
import time

from Utility.MultiprocessDataType import gpsData
import GeneralSettings

class GPSClient():

    def __init__(self, antennaGpsData):
        self.poll_interval = 0.1 # 100 ms of poll interval
        self.gpsData = antennaGpsData


    def mainProcess(self, killpill):
        tot_lat = 0
        tot_alt = 0
        tot_lon = 0
        nb_value = 0

        while killpill.empty():
            tmp_lat, tmp_lon, tmp_alt = self.getGpsCoordinates()
            nb_value = nb_value + 1
            tot_lat = tot_lat + tmp_lat
            tot_alt = tot_alt + tmp_alt
            tot_lon = tot_lon + tmp_lon

            # print("total values %lf , %lf, %lf" % (tot_lat, tot_lon, tot_alt))
            if(nb_value > 0):
                self.gpsData.setAlt(float(tot_alt/nb_value))
                self.gpsData.setLon(float(tot_lon/nb_value))
                self.gpsData.setLat(float(tot_lat/nb_value))

            print("total values %lf , %lf, %lf" % (self.gpsData.getLat(), self.gpsData.getLon(), self.gpsData.getAlt()))
            time.sleep(self.poll_interval)


    def getGpsCoordinates(self):
        # the random match the inprecision of the gps
        alt = GeneralSettings.default_rel_alt * (1 + random.uniform(-10, 10))
        lon = GeneralSettings.default_lon * (1 + random.uniform(-0.00001, 0.00001))
        lat = GeneralSettings.default_lat * (1 + random.uniform(-0.00001, 0.00001))
        return lat, lon, alt


x = GPSClient(gpsData())
x.mainProcess(Queue())

