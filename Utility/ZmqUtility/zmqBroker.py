import sys
import zmq
from multiprocessing import Queue
import time
import GeneralSettings




def runBroker(killpil):
    context_sub = zmq.Context()
    socket_sub = context_sub.socket(zmq.SUB)

    context_pub = zmq.Context()
    socket_pub = context_pub.socket(zmq.PUB)

    socket_sub.bind(GeneralSettings.server_endpoint_sub)
    socket_pub.bind(GeneralSettings.server_endpoint_pub)

    topicfilter = ""
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    while killpil.empty():
        print(killpil.empty())
        time.sleep(1)
        print("Broker loop")
        # string = socket_sub.recv()
        # print(string)
        # socket_pub.send(string)