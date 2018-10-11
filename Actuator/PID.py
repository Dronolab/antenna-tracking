import time
import math
import GeneralSettings


class PID:

    def __init__(self, P=0.51, I=0.0, D=0.00, Ts=0.015):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.windup_guard = 5.0
        self.sample_time = Ts

        self.set_point = 0.0
        self.last_valid_output = 0.0

        self.current_time = time.time()
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        self.set_point = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0

        self.output = 0.0

    def update(self, feedback_value):

        self.current_time = time.time()
        delta_time = self.current_time - self.last_time

        if (delta_time >= self.sample_time):
            #error = self.set_point - feedback_value
            error = self._shortest_path_rad(feedback_value, self.set_point)
            delta_error = error - self.last_error

            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error
            #print("error" + str(error))
            output = self.PTerm + (self.Ki * self.ITerm) + \
                (self.Kd * self.DTerm)
            self.last_valid_output = output
            return output
        else:
            return self.last_valid_output

    def setKp(self, proportional_gain):
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        self.Kd = derivative_gain

    def setWindup(self, windup):
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        self.sample_time = sample_time

    def setSetPoint(self, set_point):
        self.set_point = set_point

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
        pid_range = (-math.pi, math.pi)
        #pid_range = (-1.0, 1.0)

        if pid_in < pid_range[0]:
            pid_in = pid_range[0]
        elif pid_in > pid_range[1]:
            pid_in = pid_range[1]

        # depends on servo used. experimental value.
        servo_range = GeneralSettings.servo_pwm_range
        #servo_range = (1300, 1700)
        pulse_w = self.scale(pid_in, pid_range, servo_range)
        # pulse width increment must be by 10us
        #pulse_w = int(round(pulse_w, -1))
        pulse_w = int(pulse_w)
        return pulse_w

    def _shortest_path_deg(self, dest, source):
        """
        Calculates shortest circular path in degrees given in -180 to 180 format.
        """
        dest += 180
        source += 180
        mod_diff = (dest - source) % 360
        distance = 180 - abs(mod_diff - 180)
        if mod_diff < 180:
            return -distance
        else:
            return distance

    def _shortest_path_rad(self, dest, source):
        """
        Calculates shortest circular path in radians given in -pi to pi format.
        """
        dest = math.degrees(dest)
        source = math.degrees(source)
        distance_deg = self._shortest_path_deg(dest, source)
        distance = math.radians(distance_deg)
        return distance
