from multiprocessing import Process, Queue
import time

from Utility.MultiprocessDataType import antenna_shared_data, uav_shared_data, setpoint_shared_data

from Utility.ZmqUtility.zmqBroker import zmqBroker
from Status.statusViewer import statusViewer
from Control.antennaControl import antennaControl
from Vehicle.uavInteraction import mavlinkHandler


# initialising the shared value
antenna_data= antenna_shared_data()
uav_data = uav_shared_data()
setpoint_data = setpoint_shared_data()




if __name__ == '__main__':
    print("Starting Antenna")

    status_viewer = statusViewer()
    zmq_broker = zmqBroker()
    antenna_control = antennaControl(antenna_data, uav_data, setpoint_data)
    uav = mavlinkHandler()

    zmq_broker.start()
    status_viewer.start()
    antenna_control.start()
    uav.start()


    while True:
        print("watch loop")
        time.sleep(0.5)


