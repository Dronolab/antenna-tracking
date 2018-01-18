import os
import time

from Utility.abstract_process import processAbstract

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')


class statusViewer(processAbstract):
    def __init__(self):
        processAbstract.__init__(self)

    def process(self):
        self.greeting()
        time.sleep(5)
        print("main process from Status Viewer")
        while self.kill_pill.empty():
            clear()
            print("is alive")
            time.sleep(0.1)

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


# Process is alive
# Antenna gps (lat, long,alt) fix ?
# antenna imuRaw(pitch,roll,yaw)x2
# Antenna imu (pitch, roll, yaw) total
# Uav status (connected ...)
#Uav pitch roll yaw
# uav gps (alt long lat)
# antenna desired angles (pitch yaw)




