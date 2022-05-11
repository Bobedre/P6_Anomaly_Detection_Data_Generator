import json
import logging
import time

from signalrcore.hub_connection_builder import HubConnectionBuilder
from DataGenerator.DataGenerator import DataGenerator

class Interface:
    hub_connection = None
    end = False
    connectionId = None

    def __init__(self):
        self.connectToHub()
        self.generate = True

    def connectToHub(self):
        self.hub_connection = HubConnectionBuilder() \
            .with_url("http://localhost:8081/Hub") \
            .with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
        }) \
            .configure_logging(logging.DEBUG) \
            .build()
        self.hub_connection.on_open(lambda: self.onConnection())
        self.hub_connection.on_close(lambda: print("connection closed"))
        self.hub_connection.start()

        while not self.end:
            time.sleep(1)

        self.hub_connection.stop()

    def onConnection(self):
        self.generatorStart()

    def generatorStart(self):
        while True:
            result = DataGenerator.generateData()
            self.sendResultToHub(result)

    def sendResultToHub(self, result):
        jsonDump = json.dumps(result)
        self.hub_connection.send("SendMessage", ["", "ProbeReading", jsonDump])
