from Sensors.imuAbstract import imuHandler
import GeneralSettings


class imuYaw(imuHandler):
    def __init__(self, antenna_data):
        imuHandler.__init__(self, antenna_data)
        self.SETTINGS_FILE = GeneralSettings.IMU_YAW_FILE

    def job(self):
        if self.imu.IMURead():
            roll, pitch, yaw = self.imu.getFusionData()
            self.antenna_data.setYaw(yaw)
