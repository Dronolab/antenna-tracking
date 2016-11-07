import socket
import struct
import math
import Adafruit_PCA9685
import json

class AntennaTrackingController:
    
    # Constants
    LISTENING_IP = "0.0.0.0"
    LISTENING_PORT = 5008
    PMW_FREQUENCY = 60
    SERVO_MINIMUM_POSITIVE_PULSE_LENGTH = 200
    SERVO_MINIMUM_NEGATIVE_PULSE_LENGTH = 450
    SATELLITE_DISH_DEFAULT_LATITUDE = 45.4946761
    SATELLITE_DISH_DEFAULT_LONGITUDE = -73.5622961
    SATELLITE_DISH_DEFAULT_ALTITUDE = 14
    MAVLINK_GPS_ID = 33

    def __init__(self):
        # Setting up the pwm
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(self.PMW_FREQUENCY)

    def start(self):
        #Create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print "Socket created"
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print "Socket binded"
        self.sock.bind((self.LISTENING_IP, self.LISTENING_PORT))
        
        # Antenna coordinates

        #
        # TODO: Quand on aura du GPS, faire du handling pour ne pas prendre la latitude et longitude par defaut
        #
        self.antenna_latitude = self.SATELLITE_DISH_DEFAULT_LATITUDE
        self.antenna_longitude = self.SATELLITE_DISH_DEFAULT_LONGITUDE
        self.antenna_altitude = self.SATELLITE_DISH_DEFAULT_ALTITUDE

        while True:
            data, addr = self.sock.recvfrom(1024)
            drone_gps = json.loads(data)
            if drone_gps['packet_id'] != self.MAVLINK_GPS_ID:
                continue

            lat_drone = float(drone_gps['lat'])
            lon_drone = float(drone_gps['lon'])
            alt_drone = float(drone_gps['alt'])
            
            self.bearing_diff = self.bearing(self.antenna_latitude, self.antenna_longitude, lat_drone, lon_drone)
            self.pitch_diff = self.pitch(self.antenna_latitude, self.antenna_longitude, self.antenna_altitude, lat_drone, lon_drone, alt_drone)

	    print(self.bearing_diff)    
    #
    # Gracefully stop antenna tracking controller 
    #
    def stop(self):
        print("Antenna tracking stopped")
        self.sock.close()

    def get_gpsdata(self):
        data, addr = sock.recvfrom(1024)
        #print "gps_data:", data

    def get_IMUdata(self):
        IMU_data, addr = sock.recvfrom(1024)
        pitch,yaw,roll  = struct.unpack("ddd",IMU_data)

    def bearing(self, lat_sat, long_sat, lat_drone, long_drone):
        lat_sat = math.radians(lat_sat)
        lat_drone = math.radians(lat_drone)
        long_sat = math.radians(long_sat)
        long_drone = math.radians(long_drone)
        delta_long = long_drone - long_sat
        delta_lat = lat_drone - lat_sat
        y = math.sin(delta_long)*math.cos(lat_drone)
        x = math.cos(lat_sat)*math.sin(lat_drone) - \
        math.sin(lat_sat)*math.cos(lat_drone)*math.cos(delta_long)
        #plage de -180 a 180
        bearing_initial = math.degrees(math.atan2(y, x))
        #Pour le mettre dans le plage de 0 a 360
        #bearing_360=(bearing_initial+360)%360
        return bearing_initial
        
    def pitch(self, lat_sat, long_sat,alt_sat, lat_drone, long_drone, alt_drone):
        R = 6371000
        lat_sat = math.radians(lat_sat)
        lat_drone = math.radians(lat_drone)
        long_sat = math.radians(long_sat)
        long_drone = math.radians(long_drone)
        delta_long = long_drone - long_sat
        delta_lat = lat_drone - lat_sat
        delta_alt = alt_drone-alt_sat
        a = math.pow(math.sin(delta_lat/2),2) + math.cos(lat_sat) * math.cos(lat_drone) * math.pow(math.sin(delta_long/2),2)
        c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
        d = R * c
        pitch_angle = math.atan2(delta_alt,d)
        pitch_angle = math.degrees(pitch_angle)

        return pitch_angle    

    def bearingoffset(self, angle, bearingangleoffset):
        newbearing = angle
        newbearing -= bearingangleoffset
        if newbearing > 180 :
            newbearing -= 360
        if newbearing < -180:
            newbearing +=360

        return newbearing

    def pitchoffset(self, angle, pitchangleoffset):
        newpitch = angle
        newpitch -= bearingangleoffset
        if newpitch > 180 :
       	    newpitch -= 360
        if newbearing < -180:
            newpitch +=360

        return newbearing

    def servo_move(pitch_drone, pitch_antenna, bearing_drone, bearing_antenna):
        delta_pitch = pitch_drone - pitch_antenna
        delta_bearing = bearing_drone - bearing_antenna
