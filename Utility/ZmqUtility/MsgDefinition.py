import json


#abstract class for message generation
class BaseMsg:
    TOPIC = ""
    def generateMsg(self):
        data = json.dumps(self.__dict__)
        msg = "%s %s" %(self.TOPIC, data)
        return msg

    #decode a json msg with from  topic
    def decodeMSG(self, msg):
        # print(msg)
        topic = msg.split()[0]
        msg = str(msg)
        msg = msg.replace(topic, "")
        messagedata = json.loads(msg)
        if topic == self.TOPIC:
            keys = self.__dict__.keys()
            for key in keys:
                if key is not "message_type":
                    setattr(self, key,messagedata.get(key, None))
        return messagedata.get("message_type", None)

