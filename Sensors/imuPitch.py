from Sensors.imuAbstract import imuHandler
import GeneralSettings


class imuPitch(imuHandler):
    def __init__(self, antenna_data):
        imuHandler.__init__(self, antenna_data)
        self.SETTINGS_FILE = GeneralSettings.IMU_PITCH_FILE

    def job(self):
        if self.imu.IMURead():
            roll, pitch, yaw = self.imu.getFusionData()
            self.antenna_data.setPitch(pitch)
