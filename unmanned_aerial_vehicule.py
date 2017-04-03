import threading
import socket
import logging
import json


class UnmannedAerialVehicule(threading.Thread):

    TELEMETRY_BUFFER_SIZE = 1024
    LISTENING_IP = "0.0.0.0"
    LISTENING_PORT = 5008

    def __init__(self):
        """ Constructor """
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

        self.ready = True

        self.connection_failure = False

        # Bind socket
        try:
            self.telemetry_socket = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM)
            self.telemetry_socket.settimeout(10)
            self.telemetry_socket.bind(
                (self.LISTENING_IP, self.LISTENING_PORT))

            self.data, addr = self.telemetry_socket.recvfrom(
                self.TELEMETRY_BUFFER_SIZE)

            logging.info("UAV Socket binded")
        except socket.error:
            logging.error(
                "UAV connection failed to initialize. Please check MAVProxy or your network connection")
            self.ready = False

    def run(self):
        """ Thread callback. Will fetch UAV GPS coordinates """
        try:
            while self.ready:

                # Get telemetry data
                try:
                    self.data, addr = self.telemetry_socket.recvfrom(
                        self.TELEMETRY_BUFFER_SIZE)

                    if self.connection_failure:
                        self.connection_failure = False
                        logging.info("Connection regained")
                except socket.error:
                    self.connection_failure = True
                    logging.error("Connection loss")

                # Format into json
                telemetry_json = json.loads(self.data)
                if float(telemetry_json['packet_id']) == 33:
                    self.alt = float(telemetry_json['relative_alt']) / 1000
                    self.lat = float(telemetry_json['lat']) / 10000000
                    self.lon = float(telemetry_json['lon']) / 10000000

                    self.latency = telemetry_json['time_boot_ms'] - self.delta
                    self.delta = telemetry_json['time_boot_ms']
                if self.kill:
                    self.telemetry_socket.close()
                    break
        except KeyboardInterrupt:
            self.kill = True

    def close(self):
        """ Trigger thread closure """
        self.kill = True
