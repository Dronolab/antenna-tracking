from Actuator.PID import PID
from Actuator.abstract_servo import AbstractServo


class PitchServo(AbstractServo):

    def __init__(self):
        self.pid = PID()
        self.pid.setSetPoint(0)

    def refresh(self, WantedAngle, CurrentAngle):
        AngleCorrection = (WantedAngle - CurrentAngle)

        AngleCorrection = -AngleCorrection ## why??

        feed_back_value = AngleCorrection / 360 # convert the correction angle to -1 , 1

        command = self.pid.update(feed_back_value)

        if abs(AngleCorrection) >= self.angle_tolerance:
            ticks = self.get_y(self.init, self.delta,command)
        else:
            ticks = self.adafruitpwmvalue(self.hold_pwm, self.servo_frequency)

        return ticks
