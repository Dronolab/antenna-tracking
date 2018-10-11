from Actuator import PID
import Adafruit_PCA9685
from Utility.abstract_process import processAbstract
# temporary solution for path
#sys.path.append(os.getcwd() + "/../")
import time


class AbstractServo(processAbstract):

    def __init__(self, antenna_shared_data, setpoint_shared_data, pin_number):
        processAbstract.__init__(self)
        self.pid = PID.PID()
        self.pid.setSetPoint(0)
        self.antenna_data = antenna_shared_data
        self.setpoint_data = setpoint_shared_data
        self.pin_number = pin_number
#        self.servo = PWM.Servo()
        self.servo = Adafruit_PCA9685.PCA9685()
        self.servo.set_pwm_freq(60)

    def process(self):
        #self.servo = PWM.Servo()
        # time.sleep(1)
        while self.kill_pill.empty():
            #            schedule.run_pending()
            self.job()
            time.sleep(0.01)

    def job(self):
        """ abstract method"""
        raise

    def set_servo_pulse(channel, pulse):
        pulse_length = 1000000    # 1,000,000 us per second
        pulse_length //= 60       # 60 Hz
        #print('{0}us per period'.format(pulse_length))
        pulse_length //= 4096     # 12 bits of resolution
        #print('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        self.servo.set_pwm(channel, 0, pulse)


"""
Example:
    def job(self):
    self.pid.setSetPoint(setpoint_shared_data.getYaw())
    up = self.pid.update(self.antenna_data.getYaw())
    pulse_width = self.pid.pidscale(up)
    self.servo.set_servo(self.pin_number, pulse_width)

"""
#       usage
#   if __name__ == "__main__":
#    ant = antenna_shared_data()
#    point = setpoint_shared_data()
#    s = ServoYaw(ant, point, [pin], [min_angle], [max_angle])
#    s.start()
#    print(scale(200, (0,360), (-180,180)))
