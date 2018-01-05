from multiprocessing import Process, Queue
import time
from Utility.ZmqUtility import zmqBroker
from Status import statusViewer


zmqBroker_KillPill = Queue()
statusViewer_KillPill = Queue()


# The main goal of this test script is make sure the process status viewers is working properly
if __name__ == '__main__':

    proc_ZMQ_Broker = Process(target=zmqBroker.runBroker, args=(zmqBroker_KillPill,))
    proc_ZMQ_Broker.daemon = True

    proc_status_viewer = Process(target=statusViewer.mainStatusViewer, args=(statusViewer_KillPill,))
    proc_status_viewer.daemon = True

    # Starting All process
    proc_ZMQ_Broker.start()
    proc_status_viewer.start()
    print("started")

    # Dosent work without a delay here
    time.sleep(0.1)

    # Wait for a keyboard input to kill the main process
    input("Press enter to continue")

    zmqBroker_KillPill.put(None)
    statusViewer_KillPill.put(None)
    print("All process killed")


