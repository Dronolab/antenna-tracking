import sys
import getopt
import logging

from antenna_tracking_controller import AntennaTrackingController

if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s]: %(message)s',
        level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    atc = AntennaTrackingController()
    try:
        logging.info('Started Antenna tracking system')
        atc.start()
    except KeyboardInterrupt:
        print('\r')
        atc.stop()
        logging.info('Antenna tracking system terminated.')
        sys.exit(0)
