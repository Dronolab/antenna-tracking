"""Main entry point"""

import logging
import sys

from Control.antenna_tracking_controller import AntennaTrackingController

if __name__ == '__main__':
    verbose_mode = True
    use_internal_gps = True

    # Setup log configuration
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s]: %(message)s',
        level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    # Initialize antenna
    atc = AntennaTrackingController()

    try:
        atc.start(verbose=verbose_mode, use_internal_gps=use_internal_gps)
    except KeyboardInterrupt:
        print('\r')
        atc.stop()
        logging.info('Antenna tracking system terminated.')
        sys.exit(0)
