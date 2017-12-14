import math


class AbstractServo():

    def __init__(self, min_angle, max_angle, min_pwm, max_pwm,
                 servo_frequency, channel):

        self.delta = self._getDelta(
            1,
            self._pulse_from_pwm(max_pwm, servo_frequency),
            -1,
            self._pulse_from_pwm(min_pwm, servo_frequency))

        self.hold_pwm = (max_pwm - min_pwm) / 2.0 + min_pwm
        self.init = self._pulse_from_pwm(self.hold_pwm, servo_frequency)
        self.current_angle = 0
        self.desired_angle = 0
        self.min_pwm = min_pwm
        self.max_pwm = max_pwm
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.servo_frequency = servo_frequency
        self.angle_tolerance = 0
        self.channel = channel


    def _getDelta(self, x1, y1, x2, y2):
        slope = float(y2 - y1) / float(x2 - x1)
        return slope

    def _pulse_from_pwm(self, pwmvalue, pwmfrequency):
        pulse = pwmvalue * 1000
        pulse = pulse / 1000000
        pulse = pulse * pwmfrequency
        pulse = pulse * 4096
        pulse = int(pulse)
        return pulse

    def refresh(self, WantedAngle, CurrentAngle):
        """ This method must be implemented by extending this class """

        raise NotImplementedError()

    def get_y(self, initval, slope, xval):
        y = 0
        y = slope * xval
        y = y + initval
        y = math.fabs(y)
        return int(y)
