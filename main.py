"""Main entry point"""

import sys
import logging
from antenna_tracking_controller import AntennaTrackingController

if __name__ == '__main__':

    # Setup log configuration
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s]: %(message)s',
        level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    # Initialize antenna
    atc = AntennaTrackingController()

    try:
        atc.start()
    except KeyboardInterrupt:
        print('\r')
        atc.stop()
        logging.info('Antenna tracking system terminated.')
        sys.exit(0)
