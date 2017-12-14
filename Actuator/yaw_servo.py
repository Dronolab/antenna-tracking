from Actuator.PID import PID
from Actuator.abstract_servo import AbstractServo


class YawServo(AbstractServo):

    def __init__(self):
        self.pid = PID()
        self.pid.setSetPoint(0)


    def refresh(self, WantedAngle, CurrentAngle):

        AngleCorrection = (WantedAngle - CurrentAngle)

        feed_back_value = AngleCorrection / 360 # convert the correction angle to -1 , 1


        command = self.pid.update(feed_back_value)

        if abs(AngleCorrection) >= self.angle_tolerance:
            ticks = self.get_y(self.init, self.delta,command)
        else:
            ticks = self._pulse_from_pwm(self.hold_pwm, self.servo_frequency)

        return ticks
