
import time

class PID:

    def __init__(self, P=0.51, I=0.0, D=0.00, Ts = 0.015):

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
            error = self.set_point - feedback_value
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
            print("error" + str(error))
            output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)
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

p = PID()
p.set_point = 1
x = 0

while not x == 1:
    time.sleep(0.01)

    x += p.update(x)
    print(x)
