# import os
# import time
#
# clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
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

from multiprocessing.managers import BaseManager
from multiprocessing import Process, Value, Array
import time



def func(l):
    while l.v.value:
        # print(l.v.value)
        l.get()
        time.sleep(1)

class g:
    def __init__(self):
        self.v = Value('b', True)

    def get(self):
        print(self.v.value)


if __name__ == '__main__':
    l = g()
    proc = Process(target=func, args=(l,))
    # proc.daemon = True
    proc.start()
    time.sleep(2)
    l.v.value = False
    time.sleep(2)
    print("final")
    l.get()

# Process is alive
# Antenna gps (lat, long,alt) fix ?
# antenna imuRaw(pitch,roll,yaw)x2
# Antenna imu (pitch, roll, yaw) total
# Uav status (connected ...)
#Uav pitch roll yaw
# uav gps (alt long lat)
# antenna desired angles (pitch yaw)




