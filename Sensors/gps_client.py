import threading
import gps
import os


class GPSClient():

    def __init__(self):
        self.gpssession = gps.gps("localhost", "2947")
        self.gpssession.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        self.lat = 0
        self.alt = 0
        self.lon = 0

    def update_GPS_coordinates(self):
        try:
            report = self.gpssession.next()
            if report['class'] == 'TPV':
                if hasattr(report, 'alt'):
                    self.alt = report.alt
                if hasattr(report, 'lon'):
                    self.lon = report.lon
                if hasattr(report, 'lat'):
                    self.lat = report.lat

        except KeyError:
            pass
        except StopIteration:
            self.gpssession = None
            print("GPS has terminated")

    def GPS_coordinate_avg(self, nb_iterations):
        alt_nb_value = 0
        lon_nb_value = 0
        lat_nb_value = 0
        alt_temp = 0
        lon_temp = 0
        lat_temp = 0
        i = 0
        while i < nb_iterations:
            try:

                report = self.gpssession.next()
                # print(report)

                if report['class'] == 'TPV':
                    if hasattr(report, 'alt'):
                        alt_temp += report.alt
                        alt_nb_value += 1

                    if hasattr(report, 'lon'):
                        lon_temp += report.lon
                        lon_nb_value += 1
                    if hasattr(report, 'lat'):
                        lat_temp += report.lat
                        lat_nb_value += 1
                    i += 1
                print "GPS Progress", i, "/", nb_iterations

                # print(lat_nb_value)
                # print(alt_nb_value)
                # print(lon_nb_value)

            except KeyError:
                print("keyerror")
                pass
            except StopIteration:
                self.gpssession = None
                print("GPS has terminated")

        try:
            self.lat = lat_temp / lat_nb_value
        except ZeroDivisionError:
            print("Lat_div_0")
        try:
            self.lon = lon_temp / lon_nb_value
        except ZeroDivisionError:
            print("Lon_div_0")
        try:
            self.alt = alt_temp / alt_nb_value
        except ZeroDivisionError:
            print("alt_div_0")
