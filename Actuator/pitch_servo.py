from Actuator.PID import PID
from Actuator.abstract_servo import AbstractServo
import GeneralSettings
import math


class PitchServo(AbstractServo):

    def __init__(self, antenna_shared_data, setpoint_shared_data, pin_number, min_angle, max_angle):
        AbstractServo.__init__(self, antenna_shared_data,
                               setpoint_shared_data, pin_number)
        self.pid = PID()
        self.pid.setSetPoint(antenna_shared_data.getPitch())
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.pid.setKp(GeneralSettings.pitch_kp)
        self.pid.setKi(GeneralSettings.pitch_ki)
        self.pid.setKd(GeneralSettings.pitch_kd)

    def job(self):

        if self.min_angle >= self.setpoint_data.getPitch():
            _set_point = self.min_angle
        elif self.max_angle <= self.setpoint_data.getPitch():
            _set_point = self.max_angle
        else:
            _set_point = self.setpoint_data.getPitch()

        self.pid.setSetPoint(self.setpoint_data.getPitch())
        up = self.pid.update(self.antenna_data.getPitch())
        pulse_width = self.pid.pidscale(-up)
    #    if self.min_angle >= self.antenna_data.getPitch():
    #        pulse_width = sum(GeneralSettings.servo_pwm_range)/2
        #    x = True
        # else:
        #    x = False
        #print("min or max")
        self.servo.set_pwm(14, 0, pulse_width)
        self.servo.set_pwm(15, 0, pulse_width)
#        print("Pitch: angle",math.degrees(self.antenna_data.getPitch()),
#            "goal", math.degrees(self.setpoint_data.getPitch()),
#            "pulse", pulse_width)
