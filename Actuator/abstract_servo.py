import os
import sys
sys.path.append(os.getcwd()+"/../") #temporary solution for path
from PID import PID
import schedule
import math
from RPIO import PWM
from Utility.abstract_process import processAbstract
from Utility.MultiprocessDataType import *


class AbstractServo(processAbstract):

    def __init__(self, antenna_shared_data, setpoint_shared_data, pin_number, min_angle, max_angle):
        self.pid = PID()
        self.pid.setSetPoint(0)
        self.antenna_data = antenna_shared_data
        self.setpoint_data = setpoint_shared_data
        processAbstract.__init__(self)
        self.pin_number = pin_number
        self.max_angle = max_angle
        self.min_angle = min_angle
        #self.servo = PWM.Servo()

    def refresh(self, delta):
        feed_back_value = self.scale(delta, (-1*math.pi, math.pi), (-1, 1))
        command = self.pid.update(feed_back_value)
        pulse_width = self.pidscale(command)
        self.servo.set_servo(self.pin_number, pulse_width)

    def process(self):
        self.servo = PWM.Servo()
        schedule.every(0.015).seconds.do(self.job)
        while True:
            schedule.run_pending()

    def job(self):
        deltaYaw = self.setpoint_data.getYaw() - self.antenna_data.getYaw()
        self.refresh(deltaYaw)

    # scale value of in_range to out_range.

    def scale(self, in_value, in_range, out_range):
        if in_range[1] < in_range[0]:
            in_max = in_range[0]
            in_min = in_range[1]
        else:
            in_max = in_range[1]
            in_min = in_range[0]
        din = in_max - in_min

        if out_range[1] < out_range[0]:
            out_max = out_range[0]
            out_min = out_range[1]
        else:
            out_max = out_range[1]
            out_min = out_range[0]
        dout = out_max - out_min

        if in_value > in_max:
            in_value = in_max
        if in_value < in_min:
            in_value = in_min
        out_value = (((in_value - in_min) * dout) / din) + out_min
        return out_value


    def pidscale(self, pid_in):
        # object to change
        if pid_in < -1:
            pid_in = -1
        elif pid_in > 1:
            pid_in = 1

        pid_range = (-1.0, 1.0)
        # depends on servo used. experimental value.
        servo_range = (1300, 1700)
        pulse_w = self.scale(pid_in, pid_range, servo_range)
        # pulse width increment must be by 10us
        pulse_w = int(round(pulse_w, -1))
        return pulse_w

#usage
#if __name__ == "__main__":
#    ant = antenna_shared_data()
#    point = setpoint_shared_data()
#    s = ServoYaw(ant, point, [pin], [min_angle], [max_angle])
#    s.start()
