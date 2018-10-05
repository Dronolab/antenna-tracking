import GeneralSettings
import gpsd
from Utility.abstract_process import processAbstract
import schedule
import time


class GPSClient(processAbstract):

    def __init__(self, antenna_data):
        self.lat = GeneralSettings.default_lat
        self.lon = GeneralSettings.default_lon
        self.alt = GeneralSettings.default_rel_alt
        processAbstract.__init__(self)
        self.antenna_data = antenna_data
        self.antenna_data.setLat(self.lat)
        self.antenna_data.setLon(self.lon)
        self.antenna_data.setAlt(self.alt)
        gpsd.connect()
#        self.positions = [(self.lat, self.lon, self.alt)]
        self.positions = []
        self.ready = False

    def job(self):
        packet = gpsd.get_current()
        if packet.mode == 3:
            position = packet.position()
            _lat = position[0]
            _lon = position[1]
            #_alt = packet.altitude()
            self.positions.append((_lat, _lon))  # , _alt))
            self.ready = True

        if len(self.positions) == 1000:
            self.positions.pop(0)

        if self.ready:
            _average = tuple(
                map(lambda y: sum(y) / float(len(y)), zip(*self.positions)))
            self.antenna_data.setLat(_average[0])  # lat
            self.antenna_data.setLon(_average[1])  # lon
        # self.antenna_data.setAlt(average[2]) #alt

    def process(self):
        while self.kill_pill.empty():
            # schedule.run_pending()
            self.job()
            time.sleep(0.1)
