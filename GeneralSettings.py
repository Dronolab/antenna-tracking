
# Activate fake sensors
FAKE_IMU = True
FAKE_GPS = True


#Hardcoded magnetic declination

#Not implemented in the code yet ##########################
MAGNETIC_DECLINATION = -14.46667

# ETS gps coordonates
default_lat = 45.494620
default_lon = -73.562725
default_rel_alt = 1



endpoint_sub = "tcp://127.0.0.1:5556"
endpoint_pub = "tcp://127.0.0.1:5555"

server_endpoint_sub = "tcp://*:5555"
server_endpoint_pub = "tcp://*:5556"



mavlink_endpoint = "udp:0.0.0.0:14555"


IMU_SETTINGS_FILE = "RTIMULib"