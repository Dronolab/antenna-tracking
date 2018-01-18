import sys
import zmq
from multiprocessing import Queue
import time

from Utility.abstract_process import processAbstract
import GeneralSettings


class zmqBroker(processAbstract):
    def __init__(self):
        processAbstract.__init__(self)


    def init_broker_socket(self):
        context_sub = zmq.Context()
        self.socket_sub = context_sub.socket(zmq.SUB)

        context_pub = zmq.Context()
        self.socket_pub = context_pub.socket(zmq.PUB)

        self.socket_sub.bind(GeneralSettings.server_endpoint_sub)
        self.socket_pub.bind(GeneralSettings.server_endpoint_pub)

        self.topicfilter = ""

    def process(self):
        self.init_broker_socket()
        self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, self.topicfilter)
        while self.kill_pill.empty():
            print(self.kill_pill.empty())
            time.sleep(1)
            print("Broker loop")
            string = self.socket_sub.recv()
            print(string)
            self.socket_pub.send(string)