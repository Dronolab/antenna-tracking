import threading
import socket
import logging
import json


class UnmannedAerialVehicule(threading.Thread):

    TELEMETRY_BUFFER_SIZE = 1024
    LISTENING_IP = "0.0.0.0"
    LISTENING_PORT = 5008

    def __init__(self):
        threading.Thread.__init__(self)
        self.lat = 0
        self.alt = 0
        self.lon = 0
        self.data = None
        self.telemetry_socket = None
        self.time_boot_ms = 0
        self.pitch = 0
        self.yaw = 0
        self.roll = 0
        self.kill = False

        self.delta = 0
        self.latency = 0

    def run(self):
        try:
            # Bind socket
            self.telemetry_socket = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM)
            self.telemetry_socket.bind(
                (self.LISTENING_IP, self.LISTENING_PORT))
            logging.info("UAV Socket binded")

            while True:

                # Get telemetry data
                self.data, addr = self.telemetry_socket.recvfrom(
                    self.TELEMETRY_BUFFER_SIZE)

                # Format into json
                telemetry_json = json.loads(self.data)
                if float(telemetry_json['packet_id']) == 33:
                    self.alt = float(telemetry_json['alt']) / 1000
                    self.lat = float(telemetry_json['lat']) / 10000000
                    self.lon = float(telemetry_json['lon']) / 10000000

                    self.latency = telemetry_json['time_boot_ms'] - self.delta
                    self.delta = telemetry_json['time_boot_ms']
                if self.kill:
                    break
        except KeyboardInterrupt:
            self.kill = True

    def close(self):
        self.telemetry_socket.close()
