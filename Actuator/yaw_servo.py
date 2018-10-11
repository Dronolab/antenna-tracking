from Actuator.PID import PID
from Actuator.abstract_servo import AbstractServo
import GeneralSettings
import math


class YawServo(AbstractServo):

    def __init__(self, antenna_shared_data, setpoint_shared_data, pin_number, min_angle, max_angle):
        AbstractServo.__init__(self, antenna_shared_data,
                               setpoint_shared_data, pin_number)
        self.pid = PID()
        self.pid.setSetPoint(antenna_shared_data.getYaw())
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.pid.setKp(GeneralSettings.yaw_kp)
        self.pid.setKi(GeneralSettings.yaw_ki)
        self.pid.setKd(GeneralSettings.yaw_kd)

    def job(self):
        """
        if self.min_angle >= self.setpoint_data.getYaw():
            _set_point = self.min_angle
        elif self.max_angle <= self.setpoint_data.getYaw():
            _set_point = self.max_angle
        else:
            _set_point = self.setpoint_data.getYaw()
        """
        _set_point = self.setpoint_data.getYaw()
        self.pid.setSetPoint(_set_point)
        up = self.pid.update(self.antenna_data.getYaw())
        pulse_width = self.pid.pidscale(up)
        pulse_width = int(pulse_width)
        self.servo.set_pwm(0, 0, pulse_width)
#        print("Yaw: angle",math.degrees(self.antenna_data.getYaw()),
#            "goal", math.degrees(self.setpoint_data.getYaw()),
#            "pulse", pulse_width)
