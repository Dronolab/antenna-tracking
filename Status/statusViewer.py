import os
import time

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
#
#
# i=0
# print("start")
# while True:
#     clear()
#
#     print()
#     print("Iteration %i" %i)
#
#     print("StatusViewer Console Mode")
#     print("Status to be shown");
#     time.sleep(1)
#     i +=1


def mainStatusViewer(killpill):
    while killpill.empty():
        clear()
        print("is alive")
        time.sleep(0.1)

# Process is alive
# Antenna gps (lat, long,alt) fix ?
# antenna imuRaw(pitch,roll,yaw)x2
# Antenna imu (pitch, roll, yaw) total
# Uav status (connected ...)
#Uav pitch roll yaw
# uav gps (alt long lat)
# antenna desired angles (pitch yaw)




