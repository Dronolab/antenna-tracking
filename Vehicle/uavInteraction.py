import os
import sys
sys.path.append(os.getcwd() + "/../")

import time
from multiprocessing import Process

from Utility.abstract_process import processAbstract
from pymavlink import mavutil
from Utility.MultiprocessDataType import *
import GeneralSettings


class mavlinkHandler(processAbstract):
    def __init__(self, uav_data):
        processAbstract.__init__(self)
        self.mavs = mavutil.mavlink_connection(
            GeneralSettings.mavlink_endpoint, input=True)
        self.uav_data = uav_data

    def process(self):
        while self.kill_pill.empty():
            msg = self.mavs.recv_match(blocking=True)
            msg_type = msg.get_type()

            if (msg_type == "HEARTBEAT"):
                # print("HEARTBEAT")
                pass

            if (msg_type == "GLOBAL_POSITION_INT"):
                self.globalPositionMsgHandler(msg)

    def globalPositionMsgHandler(self, msg):
        unix = time.time()
        lat = (msg.lat / 10000000.0)
        lon = (msg.lon / 10000000.0)
        alt = (msg.alt / 1000.0)
        rel_alt = (msg.relative_alt / 1000.0)
        hdg = msg.hdg
        # print("GPS:",lat,lon,alt,rel_alt)
        self.uav_data.setLat(lat)
        self.uav_data.setLon(lon)
        self.uav_data.setAlt(rel_alt)


"""
def main():
    mav = mavlinkHandler(uav_shared_data())
    mav.start()
    time.sleep(1000)
if __name__== "__main__":
    main()
"""
