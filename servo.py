class Servo():

    def __init__(self, min_angle, max_angle, min_pwm, max_pwm, hold_pwm,
                 servo_frequency, channel, mul):

        self.delta = self.getDelta(
            max_angle,
            self.pulse_from_pwm(max_pwm, servo_frequency),
            min_angle,
            self.pulse_from_pwm(min_pwm, servo_frequency))

        self.init = self.pulse_from_pwm(hold_pwm, servo_frequency)
        self.current_angle = 0
        self.desired_angle = 0
        self.min_pwm = min_pwm
        self.max_pwm = max_pwm
        self.hold_pwm = hold_pwm
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.servo_frequency = servo_frequency
        self.angle_tolerance = 5
        self.channel = channel
        self.multiplicator = mul

    def getDelta(self, x1, y1, x2, y2):
        slope = float(y2 - y1) / float(x2 - x1)
        return slope

    def pulse_from_pwm(self, pwmvalue, pwmfrequency):
        pulse = pwmvalue * 1000
        pulse = pulse / 1000000
        pulse = pulse * pwmfrequency
        pulse = pulse * 4096

        pulse = int(pulse)
        return pulse
