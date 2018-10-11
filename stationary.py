"""
Sends stationary PWM. Use it to configurate servo potentiometers
"""
from Adafruit_PCA9685 import *

servo = PCA9685()
servo.set_pwm_freq(60)


def stop_servo():
    servo.set_pwm(0, 0, 0)
    servo.set_pwm(14, 0, 0)
    servo.set_pwm(15, 0, 0)


def stationary():
    while True:
        # Yaw
        servo.set_pwm(0, 0, 375)
# Pitch
        servo.set_pwm(14, 0, 375)
        servo.set_pwm(15, 0, 375)


def main():
    try:
        stationary()
    except:
        stop_servo()


if __name__ == '__main__':
    main()
