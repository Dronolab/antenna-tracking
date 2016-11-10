import sys
import getopt

from antenna_tracking_controller import AntennaTrackingController

if __name__ == '__main__':
    atc = AntennaTrackingController()
    try:
        atc.start()
    except KeyboardInterrupt:
        print 'Interrupted'
        atc.stop()
        sys.exit(0)
