import RTIMU
import time
import sys

yaw_file = "RTIMULibYaw.ini"
pitch_file = "RTIMULibPitch.ini"

yaw_set = RTIMU.Settings(yaw_file)
pitch_set = RTIMU.Settings(pitch_file)

imu_yaw = RTIMU.RTIMU(yaw_set)
imu_pitch = RTIMU.RTIMU(pitch_set)

imu_yaw.setSlerpPower(0.02)
imu_yaw.setGyroEnable(True)
imu_yaw.setAccelEnable(True)
imu_yaw.setCompassEnable(True)
"""
imu_pitch.setSlerpPower(0.02)
imu_pitch.setGyroEnable(True)
imu_pitch.setAccelEnable(True)
imu_pitch.setCompassEnable(True)
"""
poll_interval_yaw = imu_yaw.IMUGetPollInterval()
poll_interval_pitch = imu_pitch.IMUGetPollInterval()

while True:
    if imu_yaw.IMURead():
        data_y = imu_yaw.getFusionData()
        fusionPose_y = data_y["fusionPose"]
        print("Yaw:" + math.degrees(fusionPose_y[2]))

    if imu_pitch.IMURead():
        data_p = imu_pitch.getFusionData()
        fusionPose_p = data_p["fusionPose"]
        print("Pitch:" + math.degrees(fusionPose[1]))

    time.sleep(poll_interval_yaw / 1000)
