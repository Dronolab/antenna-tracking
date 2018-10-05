
# Activate fake sensors
FAKE_IMU = True
FAKE_GPS = True


# Hardcoded magnetic declination

# Not implemented in the code yet ##########################
MAGNETIC_DECLINATION = -10
#MAGNETIC_DECLINATION = 14.46

# ETS gps coordonates
#default_lat = 45.494620
#default_lon = -73.562725
#default_rel_alt = 1

# Le Trou cochon mort
#default_lat = 45.4036299
#default_lon = -74.3962734
#default_rel_alt = 1

# Le Trou balcony
default_lat = 0
default_lon = 0
default_rel_alt = 0

endpoint_sub = "tcp://127.0.0.1:5556"
endpoint_pub = "tcp://127.0.0.1:5555"

server_endpoint_sub = "tcp://*:5555"
server_endpoint_pub = "tcp://*:5556"


mavlink_endpoint = "udp:0.0.0.0:14550"


IMU_SETTINGS_FILE = "RTIMULib"
IMU_YAW_FILE = "RTIMULibYaw"
IMU_PITCH_FILE = "RTIMULibPitch"

# servo_pwm_range = (1200, 1800)
servo_pwm_range = (150, 600)
servo_yaw_pin = 0
servo_pitch_pin = 1

yaw_kp = 2
yaw_ki = 0
yaw_kd = 0

pitch_kp = 4
pitch_ki = 0
pitch_kd = 0
