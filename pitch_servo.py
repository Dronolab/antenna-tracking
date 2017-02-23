from abstract_servo import AbstractServo


class PitchServo(AbstractServo):

    def refresh(self, WantedAngle, CurrentAngle):
        AngleCorrection = (WantedAngle - CurrentAngle)

        AngleCorrection = -AngleCorrection

        if abs(AngleCorrection) >= self.angle_tolerance:
            ticks = self.get_y(self.init, self.delta,
                               AngleCorrection, self.multiplicator)
        else:
            ticks = self.adafruitpwmvalue(self.hold_pwm, self.servo_frequency)

        return ticks
