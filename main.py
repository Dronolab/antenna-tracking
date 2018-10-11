from Utility.MultiprocessDataType import antenna_shared_data, uav_shared_data, setpoint_shared_data
#from Control.antennaControl import antennaControl
import sys
import math
#from stationary import stop_servo
import time
from flasky import Flasky
# initialising the shared value
antenna_data = antenna_shared_data()
uav_data = uav_shared_data()
setpoint_data = setpoint_shared_data()


def main():
    #    antenna_control = antennaControl(antenna_data, uav_data, setpoint_data)
    flasky = Flasky(antenna_data, uav_data, setpoint_data)
    flasky.start()
#    antenna_control.start()


if __name__ == '__main__':
    print("Starting Antenna", time.ctime())
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping")
        stop_servo()
