import json
import socket
import logging
import struct
import sys
from antenna import Antenna
import time
import imu_client


class AntennaTrackingController:
    """ This class will controll all antenna calculation loop.

        It has the responsability to ensure we can fetch all neccessary data in
        order to make the system working properly
    """

    # MAVLink packet id for GPS. See:
    # https://pixhawk.ethz.ch/mavlink/#GLOBAL_POSITION_INT
    MAVLINK_GPS_ID = 33

    def __init__(self):
        """ Constructor """

    def start(self, verbose=True):
        """ Start execution of the main loop

            This is the central point of the antenna tracking system. It put
            all together the data and trigger calculations. Then a nice
            output is given to STDOUT.
        """

        # Display some funky ascii
        self.greeting()

        # Setup antenna tracking system
        self.antenna = Antenna()

        if self.antenna.ready:
            while True:
                # Apply a pwm according to the calculations
                self.antenna.update_target_orientation()

                time.sleep(0.2)

                if verbose:
                    self.antenna.print_current_data()

        else:
            logging.error(
                'Initialization aborted due to unmet startup conditions for one or more module.')

        self.stop()

    def stop(self):
        """ Gracefully stop antenna tracking controller """

        logging.info('Closing antenna tracking system')

        # Close threads
        self.antenna.close()

    def greeting(self):
        """ Welcome message """

        print("""
  ___        _                           _                  _    _
 / _ \      | |                         | |                | |  (_)
/ /_\ \_ __ | |_ ___ _ __  _ __   __ _  | |_ _ __ __ _  ___| | ___ _ __   __ _
|  _  | '_ \| __/ _ \ '_ \| '_ \ / _` | | __| '__/ _` |/ __| |/ / | '_ \ / _` |
| | | | | | | ||  __/ | | | | | | (_| | | |_| | | (_| | (__|   <| | | | | (_| |
\_| |_/_| |_|\__\___|_| |_|_| |_|\__,_|  \__|_|  \__,_|\___|_|\_\_|_| |_|\__, |
                                                                          __/ |
        _.--l--._                                                        |___/
     .`    |     `.
   .` `.    |    .` `.
 .`     `   |  .`     `.     POWERED BY DRONOLAB
/ __       .|.`      __ \    Source code: github.com/dronolab/antenna_tracking
|   ''--._  V  _.--''   |    License: MIT
|        _ (") _        |
| __..--'   ^   '--..__ | _
\\         .`|`.         /-.)
 `.     .`  |  `.     .`
   `. .`    |    `. .`
     `._    |    _.`|
         `--l--` |  |
                 / . \\
                / / \\ \\
               / /   \\ \\
        """)
