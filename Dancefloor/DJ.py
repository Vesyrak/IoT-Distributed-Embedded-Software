from mqtt import mqtt


class DJ:
    def __init__(self):
        self.mqttclient = mqtt("127.0.0.1", 1883)

    def addListener(self):
        self.mqttclient.add_listener_func()
