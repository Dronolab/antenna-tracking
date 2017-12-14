import zmq
import GeneralSettings
import json
from abc import abstractmethod
import time

def createPubSocket():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect(GeneralSettings.endpoint_pub)
    time.sleep(0.01)
    return socket

def createSubSocket(topic_filter):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(GeneralSettings.endpoint_sub)
    socket.setsockopt_string(zmq.SUBSCRIBE, topic_filter)
    time.sleep(0.01)
    return socket

def publishMsg(socket, msg):
    socket.send_string(msg)


def subReadMsg(socket):
    string = socket.recv()
    return string