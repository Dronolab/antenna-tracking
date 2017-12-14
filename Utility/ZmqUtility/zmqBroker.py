import sys
import zmq
import GeneralSettings


context_sub = zmq.Context()
socket_sub = context_sub.socket(zmq.SUB)

context_pub = zmq.Context()
socket_pub = context_pub.socket(zmq.PUB)

socket_sub.bind(GeneralSettings.server_endpoint_sub)
socket_pub.bind(GeneralSettings.server_endpoint_pub)

topicfilter = ""
socket_sub.setsockopt_string(zmq.SUBSCRIBE, topicfilter)


while True:
    print("Broker loop")
    string = socket_sub.recv()
    print(string)
    socket_pub.send(string)