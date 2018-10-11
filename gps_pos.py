import GeneralSettings
from Utility.abstract_process import processAbstract
from Vehicle.uavInteraction import mavlinkHandler
from Utility.MultiprocessDataType import uav_shared_data
import time

uav_data = uav_shared_data()
uav = mavlinkHandler(uav_data)
uav.start()
# while True:
# print("Lat:",uav_data.getLat(),"Lon:",uav_data.getLon(),"Alt:",uav_data.getAlt())
#    time.sleep(1)
