import numpy as np, numpy.random

from mqtt import mqtt


class Agent:
    def __init__(self):
       # self.mqttclient = mqtt("127.0.0.1", 1883)
       # self.startAgentListener()
        dividers = np.random.dirichlet(np.ones(3), 1)
        self.LikeRates = [0, 0, 0]
        self.LikeRates[0] = dividers[0][0]
        self.LikeRates[1] = dividers[0][1]
        self.LikeRates[2] = dividers[0][2]
        self.LikeNeighborRates = [0, 0, 0, 0]
        for i in range(0, 3):
            self.LikeNeighborRates[i] = np.random.uniform(0, 1)

    def influence(self, LikeRate, n):
        m = max(LikeRate)
        pos = [i for i, j in enumerate(LikeRate) if j == m][0]
        Influence = (0.2 * LikeRate[pos] + 0.1 * np.random.uniform(0, 1)) * self.LikeNeighborRates[n]
        for i in range(0, 3):
            if i is pos:
                self.LikeRates[i] += Influence;
                if self.LikeRates[i] > 1:
                    self.LikeRates[i] = 1
            else:
                self.LikeRates[i] -= Influence * 0.5
                if self.LikeRates[i] < 0:
                    self.LikeRates[i] = 0

    def color(self):
        color = [0, 0, 0]
        for i in range(0, 3):
            color[i] = self.LikeRates[i] * 255
        return color

    def getLike(self, genre):
        love = [i for i, j in enumerate(self.LikeRates) if j == max(self.LikeRates)][0]
        if genre is "Rock" and love is 0:
            return "Like"
        elif genre is "Pop" and love is 1:
            return "Like"
        elif genre is "Techno" and love is 2:
            return "Like"
        else:
            return "Dislike"

    # Connecteer met Mqtt Host
    def startAgentListener(self):
        self.mqttclient.connect()
        self.mqttclient.add_listener_func(self.onDJMessage)

    # Wordt opgeroepen wanneer er een Mqtt bericht binnenkomt
    def onDJMessage(self, msg):
        self.mqttclient.notify_listeners(self.getLike(msg))
