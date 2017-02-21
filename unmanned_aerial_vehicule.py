import threading
import socket
import logging
import json

class UnmannedAerialVehicule(threading.Thread):

    TELEMETRY_BUFFER_SIZE = 1024

    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.lat = 0
        self.alt = 0
        self.lon = 0
        self.data = None
        self.ip = ip
        self.port = port
        self.telemetry_socket = None
        self.time_boot_ms = 0
        self.pitch = 0
        self.yaw = 0
        self.roll = 0
        self.kill = False

    def uav_altitude(self):
        return self.alt

    def uav_latitude(self):
        return self.lat

    def uav_longitude(self):
        return self.lon

    def update_UAVgps(self):
        jsonStr = json.loads(self.data)
        if float(jsonStr['packet_id']) == 33:
            self.alt = float(jsonStr['alt']) / 1000
            self.lat = float(jsonStr['lat']) / 10000000
            self.lon = float(jsonStr['lon']) / 10000000

    def update_UAVAttitude(self):
        jsonStr = json.loads(self.data)
        if float(jsonStr['packet_id']) == 30:
            self.time_boot_ms = float(jsonStr['time_boot_ms'])
            self.pitch = math.degrees(float(jsonStr['pitch']))
            self.yaw = math.degrees(float(jsonStr['yaw']))
            self.roll = math.degrees(float(jsonStr['roll']))

    def set_telemetry_IP(self, host_IP):
        self.ip = host_IP

    def set_port(self, hostPort):
        self.port = hostPort

    def create_bind_socket(self):
        self.telemetry_socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)
        self.telemetry_socket.bind((self.ip, self.port))
        logging.info("UAV Socket binded")

    def receive_telemetry(self):
        return self.telemetry_socket.recvfrom(
            UnmannedAerialVehicule.TELEMETRY_BUFFER_SIZE)

    def run(self):
        try:
            while True:
                print("yolo")
                self.receive_telemetry()
                self.update_UAVgps()
                #self.update_UAVAttitude()
                if self.kill:
                    break
        except KeyboardInterrupt:
            self.kill = True

    def __del__(self):
        self.telemetry_socket.close()
