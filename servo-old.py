import math


class Servo():

    def __init__(self, minangle, maxangle, minpwm, maxpwm, holdpwm, servofreq,
                 channel, mul):
        self.delta = self.getDelta(maxangle,
                                   self.adafruitpwmvalue(maxpwm, servofreq),
                                   minangle,
                                   self.adafruitpwmvalue(minpwm, servofreq))

        self.init = adafruitpwmvalue(holdpwm, servofreq)
        self.currentangle = 0
        self.desireangle = 0
        self.minpwm = minpwm
        self.maxpwm = maxpwm
        self.holdpwm = holdpwm
        self.minangle = minangle
        self.maxangle = maxangle
        self.servofreq = servofreq
        self.Angletolerance = 5
        self.channel = channel
        self.multiplicator = mul

    # resposible to refresh the servo to a certain direction
    def Refresh(self, WantedAngle, CurrentAngle):
        AngleCorrection = (WantedAngle - CurrentAngle)
        if abs(AngleCorrection) >= self.Angletolerance:
            ticks = self.getY(self.init, self.delta,
                              AngleCorrection, self.multiplicator)
            servo.RefreshServo(ticks, self.channel)
        else:
            ticks = adafruitpwmvalue(self.holdpwm, self.servofreq)
            servo.RefreshServo(ticks, self.channel)
        return ticks

    def adafruitpwmvalue(pwmvalue, pwmfrequency):
        pulse = pwmvalue * 1000
        pulse = pulse / 1000000
        pulse = pulse * pwmfrequency
        pulse = pulse * 4096

        pulse = int(pulse)
        return pulse

    def getDelta(x1, y1, x2, y2):
        slope = float(y2 - y1) / float(x2 - x1)
        return slope

    def getY(initval, slope, xval, mul):
        y = 0
        y = (slope * mul) * xval
        y = y + initval
        y = math.fabs(y)
        return int(y)
